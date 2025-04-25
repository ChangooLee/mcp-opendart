한국어 | [English](README_en.md)

# MCP OpenDART

![License](https://img.shields.io/github/license/ChangooLee/mcp-opendart)
![PyPI Version](https://img.shields.io/pypi/v/mcp-opendart)
![PyPI Downloads](https://img.shields.io/pypi/dm/mcp-opendart)

OpenDART(금융감독원 전자공시시스템)를 위한 Model Context Protocol(MCP) 서버입니다. 이 통합은 데이터 프라이버시와 보안을 유지하면서 OpenDART와의 안전하고 맥락적인 AI 상호작용을 가능하게 합니다.

## 사용 예시

AI 어시스턴트에게 다음과 같은 요청을 할 수 있습니다:

- **📊 재무 보고서** - "삼성전자의 최신 분기 보고서를 가져와주세요"
- **🔍 공시 검색** - "지난달 코스피 기업들의 주요 지분 변동을 찾아주세요"
- **📈 기업 분석** - "현대자동차의 지난 3년간의 재무제표를 보여주세요"
- **⚡ 실시간 업데이트** - "오늘의 기술 섹터 중요 공시를 가져와주세요"

### 기능 데모

[데모 영상이 추가될 예정입니다]

### 지원 기능

| 기능 | 지원 상태 | 설명 |
|---------|---------------|-------------|
| **공시정보** | ✅ 완전 지원 | 기업 정보, 공시 문서 조회 |
| **정기보고서 주요정보** | ✅ 완전 지원 | 사업보고서, 분기/반기보고서 주요 정보 |
| **정기보고서 재무정보** | ✅ 완전 지원 | 재무제표, XBRL 데이터 |
| **지분공시 종합정보** | ✅ 완전 지원 | 주요 주주 및 임원 지분 현황 |
| **주요사항보고서 주요정보** | ✅ 완전 지원 | 주요사항보고서 핵심 정보 |
| **증권신고서 주요정보** | ✅ 완전 지원 | 증권발행 신고 주요 정보 |

## 빠른 시작 가이드

### 1. 인증 설정

먼저 OpenDART API 키를 얻으세요:

1. [OpenDART](https://opendart.fss.or.kr/)에 접속
2. 회원가입 후 API 키 신청


### 2. 설치

```bash
# 저장소 복제
git clone https://github.com/ChangooLee/mcp-opendart.git
cd mcp-opendart

# 가상환경 생성
python3 -m venv .venv
source .venv/bin/activate

```

## IDE 통합

MCP OpenDART는 IDE 통합을 통해 AI 어시스턴트와 함께 사용하도록 설계되었습니다.

### Claude Desktop 설정 방법

1. 햄버거 메뉴(☰) > Settings > Developer > "Edit Config" 버튼 클릭
2. 아래 설정을 추가:

```json
{
  "mcpServers": {
    "mcp-opendart": {
      "command": "YOUR_LOCATION/.venv/bin/mcp-opendart",
      "env": {
        "OPENDART_API_KEY": "API-KEY",
        "OPENDART_BASE_URL": "https://opendart.fss.or.kr/api/",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "TRANSPORT": "stdio",
        "LOG_LEVEL": "INFO",
        "MCP_SERVER_NAME": "mcp-opendart"
      }
    }
  }
}
```

> [!NOTE]
> - `YOUR_LOCATION`: 가상환경이 설치된 실제 경로로 변경
> - `API-KEY`: 발급받은 OpenDART API 키로 변경

### 주요 환경 변수

- `OPENDART_API_KEY`: OpenDART API 키
- `OPENDART_BASE_URL`: API 기본 URL (기본값: 공식 URL)
- `HOST`: 서버 호스트 (기본값: 0.0.0.0)
- `PORT`: 서버 포트 (기본값: 8000)
- `TRANSPORT`: 전송 방식 (stdio 권장)
- `LOG_LEVEL`: 로깅 레벨 (INFO, DEBUG 등)
- `MCP_SERVER_NAME`: 서버 이름

## 도구

### OpenDART 도구

- `ds001_disclosure`: 공시정보 검색 및 조회
- `ds002_periodic`: 정기보고서 주요정보 조회
- `ds003_financial`: 정기보고서 재무정보 조회
- `ds004_ownership`: 지분공시 종합정보 조회
- `ds005_major`: 주요사항보고서 주요정보 조회
- `ds006_securities`: 증권신고서 주요정보 조회

<details>
<summary>주요 도구 목록</summary>

| 카테고리 | 도구 |
|----------|-------|
| **공시정보** | `get_corporation_code_by_name`, `get_disclosure_list`, `get_corporation_info`, `get_disclosure_document`, `get_corporation_code` |
| **정기보고서 주요정보** | `get_annual_report`, `get_quarterly_report`, `get_semi_annual_report` |
| **정기보고서 재무정보** | `get_single_acnt`, `get_multi_acnt`, `get_xbrl_file`, `get_single_acc`, `get_xbrl_taxonomy`, `get_single_index`, `get_multi_index` |
| **지분공시 종합정보** | `get_major_shareholders`, `get_executive_holdings` |
| **주요사항보고서 주요정보** | `get_major_reports`, `get_business_reports` |
| **증권신고서 주요정보** | `get_securities_filing`, `get_prospectus` |

</details>

## 문제 해결 및 디버깅

### 일반적인 문제

- **인증 실패**:
  - API 키가 유효하고 활성 상태인지 확인
  - API 키에 필요한 권한이 있는지 확인
  - API 호출 한도(일 20,000회) 초과 여부 확인

- **데이터 접근 문제**:
  - 일부 데이터는 추가 권한이 필요할 수 있음
  - 특정 데이터는 지연된 접근(최대 24시간)이 있을 수 있음
  - 회사가 접근 가능한 범위 내에 있는지 확인

- **연결 문제**:
  - 인터넷 연결 확인
  - OpenDART API 서비스 가용성 확인
  - 방화벽이 연결을 차단하지 않는지 확인

### 디버깅 도구

```bash
# 상세 로깅 활성화
export LOG_LEVEL=DEBUG

# 로그 확인
tail -f opendart.log

# API 연결 테스트
python -m mcp_opendart test-connection
```

## 보안

- API 키를 절대 공유하지 마세요
- `.env` 파일을 안전하게 보관하세요
- 적절한 속도 제한을 사용하세요
- API 사용량을 모니터링하세요
- 민감한 데이터는 환경 변수에 저장하세요

## 기여하기

기여를 환영합니다! 기여하시려면:

1. 저장소를 포크하세요
2. 기능 브랜치를 만드세요
3. 변경사항을 작성하세요
4. 풀 리퀘스트를 제출하세요

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

이 프로젝트는 공식 OpenDART 제품이 아닙니다. OpenDART는 금융감독원의 등록 상표입니다. 