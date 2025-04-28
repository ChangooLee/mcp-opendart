import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def parse_response_table(soup):
    tables = soup.find_all('table', class_='tb02')
    target_table = None
    for table in tables:
        caption = table.find('caption')
        if caption and '응답 결과' in caption.get_text():
            target_table = table
            break
    if not target_table:
        print("❗ '응답 결과' 테이블을 못 찾았습니다.")
        return None

    tbody = target_table.find('tbody')
    if not tbody:
        print("❗ 테이블에는 tbody가 없습니다.")
        return None

    rows = tbody.find_all('tr')
    if not rows:
        print("❗ 테이블에는 데이터 행이 없습니다.")
        return None

    print('rows:', rows)

    result = {}
    parents = {0: result}
    prev_level = 0
    prev_key = None
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 3:
            continue  # 컬럼이 충분하지 않으면 무시

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
            # 새로운 level이 등장하면 parents에 추가
            if level not in parents:
                # prev_key가 None이면 root로 연결
                if prev_key is not None:
                    parents[level] = parents[prev_level][prev_key]
                else:
                    parents[level] = result

            parents[level][key] = {'name': name, 'description': desc}
            prev_level = level
            prev_key = key

        print('parents:', parents)
        print('접근하려는 키:', level)
        # KeyError 방지용 체크 (디버깅용)
        if level in parents:
            pass
        else:
            print(f'경고: parents에 {level} 키 없음')

    return result


def save_structure_from_urls(json_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    JSON_PATH = os.path.join(BASE_DIR, json_path)

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        url_dict = json.load(f)

    result = {}

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)

    for url in url_dict.keys():
        print(f"[URL] {url}")
        try:
            driver.get(url)

            try:
                WebDriverWait(driver, 20).until(  # 🔥 대기 시간 20초로 늘림
                    EC.presence_of_element_located((By.CLASS_NAME, 'tb02'))
                )
            except TimeoutException:
                print(f"TimeoutException: 테이블 로딩 실패 ➔ HTML 저장")
                with open('debug_page.html', 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                raise Exception("테이블이 로딩되지 않았습니다.")

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            structure = parse_response_table(soup)

            if structure is not None:
                result[url] = structure
                print(json.dumps(structure, ensure_ascii=False, indent=2))
            else:
                print("응답 결과 테이블을 찾지 못함")
                result[url] = {}

        except Exception as e:
            print(f"Error: {type(e).__name__} - {e}")
            result[url] = {}

    driver.quit()

    output_path = os.path.join(BASE_DIR, 'parsed_response_structures.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"모든 URL의 응답 결과 구조를 저장 완료: {output_path}")

if __name__ == "__main__":
    save_structure_from_urls('opendart_reference_urls.json')
