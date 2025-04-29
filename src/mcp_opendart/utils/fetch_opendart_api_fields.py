import os
import json
import time
import ast
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def parse_response_table(soup) -> Dict[str, Any]:
    """BeautifulSoup으로 응답 결과 테이블 파싱"""
    tables = soup.find_all('table', class_='tb02')
    target_table = None
    for table in tables:
        caption = table.find('caption')
        if caption and '응답 결과' in caption.get_text():
            target_table = table
            break
    if not target_table:
        return {}

    tbody = target_table.find('tbody')
    if not tbody:
        return {}

    rows = tbody.find_all('tr')
    if not rows:
        return {}

    result: Dict[str, Any] = {}
    parents: Dict[int, Dict[str, Any]] = {0: result}
    prev_level = 0
    prev_key: Optional[str] = None

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 3:
            continue

        key_cell = cols[0]
        name = cols[1].get_text(strip=True)
        desc = cols[2].get_text(strip=True)

        span = key_cell.find('span')
        indent = 0
        if span and span.get('class'):
            for cls in span['class']:
                if cls.startswith('mgl'):
                    indent = int(cls[3:])
                    break

        key = key_cell.get_text(strip=True)
        if not key:
            continue

        level = indent // 20
        if key == 'list':
            parents[level][key] = {}
            parents[level + 1] = parents[level][key]
        else:
            if level not in parents:
                if prev_key is not None:
                    parents[level] = parents[prev_level][prev_key]
                else:
                    parents[level] = result

            parents[level][key] = {'name': name, 'description': desc}
            prev_level = level
            prev_key = key

    return result

def extract_tool_info(file_path: str) -> list[dict[str, str]]:
    """tools/*.py 파일에서 tool_name, function_name, description, 참고 url 추출"""
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)
    results: list[dict[str, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            description = ast.get_docstring(node) or ""

            tool_name = ""
            tool_desc = ""
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and getattr(decorator.func, 'attr', '') == 'tool':
                    for keyword in decorator.keywords:
                        if keyword.arg == 'name':
                            tool_name = ast.literal_eval(keyword.value)
                        if keyword.arg == 'description':
                            tool_desc = ast.literal_eval(keyword.value)

            # docstring 안에서 "참고:" URL 찾기
            url = ""
            for line in (description.splitlines() if description else []):
                line = line.strip()
                if line.startswith("참고:"):
                    url = line.replace("참고:", "").strip()
                    break

            if url:
                results.append({
                    "tool_name": tool_name,
                    "function_name": function_name,
                    "description": tool_desc,
                    "url": url
                })

    return results

def fetch_fields_for_urls(url_list) -> Dict[str, Dict[str, Any]]:
    """각 URL에 대해 Selenium으로 fields 크롤링"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    fields_result: Dict[str, Dict[str, Any]] = {}

    for url in url_list:
        print(f"[URL] {url}")
        try:
            driver.get(url)

            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'tb02'))
                )
            except TimeoutException:
                print(f"⚠️ {url} 에서 테이블을 찾지 못했습니다. (타임아웃)")
                fields_result[url] = {}
                continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            structure = parse_response_table(soup)
            fields_result[url] = structure

        except Exception as e:
            print(f"⚠️ Error: {type(e).__name__} - {e}")
            fields_result[url] = {}
        
        time.sleep(2)

    driver.quit()
    return fields_result

def main() -> None:
    """메인 함수"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TOOLS_DIR = os.path.join(BASE_DIR, '../tools')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'data')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    OUTPUT_JSON_PATH = os.path.join(OUTPUT_DIR, 'parsed_response_structures.json')

    # 1. tools 폴더 읽기
    tool_infos: list[dict[str, str]] = []
    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith('.py'):
            file_path = os.path.join(TOOLS_DIR, filename)
            extracted = extract_tool_info(file_path)
            tool_infos.extend(extracted)

    # 2. URL 목록 만들기
    urls = [info['url'] for info in tool_infos]

    # 3. URL별 fields 크롤링
    fields_per_url = fetch_fields_for_urls(urls)

    # 4. 결과 병합
    merged_result: Dict[str, Dict[str, Any]] = {}
    for info in tool_infos:
        url = info['url']
        merged_result[url] = {
            "tool_name": info['tool_name'],
            "function_name": info['function_name'],
            "description": info['description'],
            "fields": fields_per_url.get(url, {})
        }

    # 5. 저장
    try:
        with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(merged_result, f, ensure_ascii=False, indent=2)
        print(f"✅ 최종 결과 저장 완료: {OUTPUT_JSON_PATH}")
    except Exception as e:
        print(f"❌ 결과 저장 실패: {type(e).__name__} - {e}")

if __name__ == "__main__":
    main()
