# mcp_opendart/registry/initialize_registry.py

from mcp_opendart.registry.tool_registry import ToolRegistry

def initialize_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register_tool(
        name="get_corporation_code_by_name",
        korean_name="기업 고유번호 조회",
        description="기업명을 이용해 고유번호(corp_code)를 조회합니다. 모든 공시 자료 검색의 시작점",
        parameters={
            "type": "object",
            "properties": {
                "corp_name": {
                    "type": "string",
                    "description": "기업명"
                }
            },
            "required": ["corp_name"]
        }
    )

    registry.register_tool(
        name="get_disclosure_list",
        korean_name="공시 목록 조회",
        description="기업의 전체 공시 이력을 날짜별로 조회하여 경영활동, 재무현황, 지배구조 변화를 신속하게 파악",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작일 (YYYYMMDD)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료일 (YYYYMMDD)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=["get_corporation_code_by_name", "get_single_index", "get_single_acnt", "get_multi_acnt", "get_corporation_info", "get_multi_index", "get_major_shareholder"]
    )

    registry.register_tool(
        name="get_single_acnt",
        korean_name="단일회사 주요계정 조회",
        description="단일 기업의 매출액, 영업이익, 당기순이익 등 핵심 재무 계정 정보를 조회",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2025)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011:사업보고서, 11012:반기보고서 등)"
                },
                "fs_div": {
                    "type": "string",
                    "description": "재무제표 구분 (OFS: 개별, CFS: 연결)",
                    "nullable": True
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=["get_corporation_code_by_name"]
    )

    registry.register_tool(
        name="get_multi_acnt",
        korean_name="다중회사 주요계정 조회",
        description="기업 그룹 전체의 연결재무제표를 조회하여 재무 건전성과 경영성과를 종합 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 목록 (콤마 구분)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2025)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011:사업보고서, 11012:반기보고서 등)"
                },
                "fs_div": {
                    "type": "string",
                    "description": "재무제표 구분 (OFS: 개별, CFS: 연결)",
                    "nullable": True
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=["get_corporation_code_by_name"]
    )

    registry.register_tool(
        name="get_single_acc",
        korean_name="연결/개별 재무제표 조회",
        description="XBRL 기준으로 기업의 전체 재무제표를 조회",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {"type": "string"},
                "bsns_year": {"type": "string"},
                "reprt_code": {"type": "string"}
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=["get_corporation_code_by_name"]
    )

    registry.register_tool(
        name="get_single_index",
        korean_name="단일회사 주요 재무지표 조회",
        description="단일 기업의 수익성, 안정성, 성장성, 활동성 주요 재무지표를 조회하여 3개년 추세를 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2025)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                },
                "idx_cl_code": {
                    "type": "string",
                    "description": "지표분류코드 (M210000: 수익성지표, M220000: 안정성지표, M230000: 성장성지표, M240000: 활동성지표)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code", "idx_cl_code"]
        },
        linked_tools=["get_corporation_code_by_name", "get_single_acc", "get_single_acnt", "get_disclosure_list"]
    )

    registry.register_tool(
        name="get_multi_index",
        korean_name="다중회사 주요 재무지표 조회",
        description="그룹 전체의 수익성, 안정성, 성장성, 활동성 주요 재무지표를 조회하여 연결재무제표 기반 재무건전성과 성장성을 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 목록 (콤마 구분)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2025)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                },
                "idx_cl_code": {
                    "type": "string",
                    "description": "지표분류코드 (M210000: 수익성지표, M220000: 안정성지표, M230000: 성장성지표, M240000: 활동성지표)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code", "idx_cl_code"]
        },
        linked_tools=["get_corporation_code_by_name", "get_single_acc", "get_multi_acnt", "get_disclosure_list"]
    )

    registry.register_tool(
        name="get_xbrl_taxonomy",
        korean_name="XBRL 표준 계정체계 조회",
        description="IFRS 기반 XBRL 재무제표 표준 계정체계를 조회하여 재무데이터 정형화와 비교 분석을 지원",
        parameters={
            "type": "object",
            "properties": {
                "sj_div": {
                    "type": "string",
                    "description": "재무제표 구분 (BS: 재무상태표, IS: 손익계산서 등)"
                },
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(선택)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도(선택, 예: 2025)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드(선택, 예: 11011:사업보고서 등)"
                }
            },
            "required": ["sj_div"]
        },
        linked_tools=["get_single_acc", "get_single_acnt", "get_multi_acnt"]
    )

    registry.register_tool(
        name="get_corporation_info",
        korean_name="기업 기본정보 조회",
        description="기업의 대표자, 결산월, 상장 상태, 가족관계 등 핵심 기초 정보를 조회",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                }
            },
            "required": ["corp_code"]
        },
        linked_tools=["get_corporation_code_by_name"]
    )

    registry.register_tool(
        name="get_single_acc",
        korean_name="단일회사 전체 재무제표 조회",
        description="상장법인 및 주요 비상장법인의 전체 XBRL 재무제표 데이터를 조회하여 세부 재무상태와 수익성을 정밀 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2025)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011:사업보고서 등)"
                },
                "fs_div": {
                    "type": "string",
                    "description": "재무제표 구분 (OFS: 개별, CFS: 연결). 기본값: 'OFS'"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=["get_corporation_code_by_name"]
    )

    registry.register_tool(
        name="get_major_shareholder",
        korean_name="최대주주 지분 현황 조회",
        description="정기보고서 기준 최대주주 및 특수관계인의 지분 보유 현황을 조회하고, 지분율 변화, 지배구조 집중도, 승계 및 분쟁 리스크를 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_executive_trading",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_major_shareholder_changes",
        korean_name="최대주주 지분 변동 조회",
        description="정기보고서 기준 최대주주의 지분 변동 내역을 조회하고, 변동 원인과 시점, 지분율 변화 등을 바탕으로 승계 흐름, 지배력 약화, 경영권 리스크를 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_major_shareholder",
            "get_disclosure_list",
            "get_executive_trading",
            "get_major_holder_changes"
        ]
    )

    registry.register_tool(
        name="get_minority_shareholder",
        korean_name="소액주주 지분 현황 조회",
        description="정기보고서를 기반으로 소액주주의 수, 지분율, 보유 주식 수 등을 조회하고, 지배구조 안정성, 경영권 방어력, M&A 리스크 등을 종합 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_major_shareholder",
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_treasury_stock"
        ]
    )


    registry.register_tool(
        name="get_major_holder_changes",
        korean_name="대량보유 상황보고 조회",
        description="주요 주주(5% 이상 보유자)의 지분 변동 내역을 조회하여 경영권 변동 리스크 및 지배구조 변화 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "start_date": {
                    "type": "string",
                    "description": "검색 시작일 (예: 20240101)"
                },
                "end_date": {
                    "type": "string",
                    "description": "검색 종료일 (예: 20241231)"
                }
            },
            "required": ["corp_code"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_executive_trading",
            "get_single_acc",
            "get_disclosure_list",
            "get_paid_in_capital_increase",
            "get_free_capital_increase"
        ]
    )

    registry.register_tool(
        name="get_executive_trading",
        korean_name="임원·주요주주 소유보고 조회",
        description="임원 및 주요주주의 주식 보유 변동 내역을 조회하여 내부자 거래 및 경영진 전망 변화 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "start_date": {
                    "type": "string",
                    "description": "검색 시작일 (예: 20240101)"
                },
                "end_date": {
                    "type": "string",
                    "description": "검색 종료일 (예: 20241231)"
                }
            },
            "required": ["corp_code"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_equity",
        korean_name="지분증권 조회",
        description="신주발행 및 주식매출 내역을 조회하여 자본 확충 계획, 지배구조 변동 리스크, 투자자 보호 수준 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_paid_in_capital_increase",
            "get_stock_total",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_debt",
        korean_name="채무증권 조회",
        description="채무증권(회사채 등) 발행 및 매출 내역을 조회하여 부채 리스크, 차환 위험, 재무 건전성 변동 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_debt_securities_issued",
            "get_single_acc",
            "get_creditor_management",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_depository_receipt",
        korean_name="증권예탁증권 발행 조회",
        description="예탁증권(DR) 발행 내역을 조회하여 자금조달 전략, 발행 구조, 투자자 보호 이슈 평가",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_single_acc",
            "get_disclosure_list",
            "get_major_holder_changes"
        ]
    )

    registry.register_tool(
        name="get_merger_report",
        korean_name="합병 증권신고서 조회",
        description="합병 및 분할합병 관련 상세 내역을 조회하여 경영권 변동 리스크, 주주가치 훼손 가능성, 합병 절차의 공정성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_division_merger",
            "get_stock_total",
            "get_major_holder_changes",
            "get_executive_info",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_stock_exchange_report",
        korean_name="주식의포괄적교환·이전 증권신고서 조회",
        description="주식교환 또는 주식이전 관련 상세 내역을 조회하여 지배구조 재편 리스크, 소수주주 보호 이슈, 자본구조 변동 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_division_merger",
            "get_major_holder_changes",
            "get_stock_total",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_division_report",
        korean_name="분할 증권신고서 조회",
        description="회사 분할(신설분할, 인적분할, 물적분할) 관련 상세 내역을 조회하여 경영구조 변화 리스크, 주주가치 훼손 가능성, 신설법인 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_division_merger",
            "get_major_holder_changes",
            "get_stock_total",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_asset_transfer",
        korean_name="자산양수도 및 풋백옵션 조회",
        description="자산 양수도 계약 및 풋백옵션 설정 사실을 조회하여 대규모 자산 이동과 잠재 재무 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=["get_corporation_code_by_name", "get_disclosure_list", "get_single_acc", "get_major_holder_changes", "get_executive_trading"]
    )

    registry.register_tool(
        name="get_bankruptcy",
        korean_name="부도발생 조회",
        description="기업의 부도 발생 사실을 조회하여 유동성 위기와 구조적 재무 리스크 조기 탐지",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_disclosure_list",
            "get_rehabilitation",
            "get_business_suspension",
            "get_dissolution",
            "get_major_holder_changes",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_business_suspension",
        korean_name="영업정지 조회",
        description="기업의 영업정지 사실을 조회하여 사업부문 매출 손실 규모, 수익성 악화 리스크, 경영구조 변화 가능성 평가",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_disclosure_list",
            "get_bankruptcy",
            "get_rehabilitation",
            "get_dissolution",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_rehabilitation",
        korean_name="회생절차 개시신청 조회",
        description="회생절차 개시신청 사실을 조회하여 기업의 재무위기, 유동성 고갈, 향후 존속 가능성 및 회생 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_bankruptcy",
            "get_business_suspension",
            "get_dissolution",
            "get_major_holder_changes",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_dissolution",
        korean_name="해산사유 발생 조회",
        description="기업의 해산사유 발생 사실을 조회하여 법적 존속성 상실, 청산 절차 돌입 가능성, 투자금 회수 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_bankruptcy",
            "get_rehabilitation",
            "get_major_holder_changes",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_paid_in_capital_increase",
        korean_name="유상증자 결정 조회",
        description="유상증자 결정을 조회하여 자금조달 전략, 기존 주주 지분 희석 가능성, 성장 투자 또는 재무구조 개선 의도 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_stock_total",
            "get_major_holder_changes",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_free_capital_increase",
        korean_name="무상증자 결정 조회",
        description="무상증자 결정을 조회하여 자본구조 조정, 내부유보금 전환, 주주구성 변화 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_stock_total",
            "get_major_holder_changes",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_paid_free_capital_increase",
        korean_name="유무상증자 결정 조회",
        description="유상증자와 무상증자 결정을 동시에 조회하여 복합 자본조달 전략, 지배구조 변화 가능성, 재무구조 변동 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_stock_total",
            "get_major_holder_changes",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_capital_reduction",
        korean_name="감자 결정 조회",
        description="감자 결정을 조회하여 자본구조 축소, 재무구조 재편, 부실 정리 목적 여부 분석 및 경영 리스크 조기 탐지",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_disclosure_list",
            "get_single_acc",
            "get_major_holder_changes",
            "get_rehabilitation",
            "get_bankruptcy"
        ]
    )

    registry.register_tool(
        name="get_creditor_management",
        korean_name="채권은행 등의 관리절차 개시 조회",
        description="채권은행 등 관리절차 개시 사실을 조회하여 기업 재무위기, 정상화 가능성, 구조조정 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_disclosure_list",
            "get_bankruptcy",
            "get_rehabilitation",
            "get_major_holder_changes",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_lawsuit",
        korean_name="소송 등의 제기 조회",
        description="소송 제기 사실을 조회하여 재무 리스크, 경영권 분쟁 리스크, 사업 정지 가능성 조기 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_disclosure_list",
            "get_major_holder_changes",
            "get_executive_trading",
            "get_single_acc",
            "get_business_suspension"
        ]
    )

    registry.register_tool(
        name="get_foreign_listing_decision",
        korean_name="해외 증권시장 주권등 상장 결정 조회",
        description="해외 증권시장 상장 결정을 조회하여 글로벌 자금조달 전략, 주주구성 변화 가능성, 투자 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_disclosure_list",
            "get_major_holder_changes",
            "get_single_acc",
            "get_executive_trading"
        ]
    )

    registry.register_tool(
        name="get_foreign_delisting_decision",
        korean_name="해외 증권시장 주권등 상장폐지 결정 조회",
        description="해외 증권시장 상장폐지 결정을 조회하여 글로벌 시장 철수 전략, 투자자 신뢰도 변화, 지배구조 재편 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_disclosure_list",
            "get_major_holder_changes",
            "get_single_acc",
            "get_executive_trading"
        ]
    )

    registry.register_tool(
        name="get_foreign_listing",
        korean_name="해외 증권시장 주권등 상장 조회",
        description="해외 증권시장 상장 사실을 조회하여 글로벌 시장 진출 현황, 투자자 기반 확보 여부, 지배구조 변동 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_foreign_listing_decision",
            "get_foreign_delisting_decision",
            "get_major_holder_changes",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_foreign_delisting",
        korean_name="해외 증권시장 주권등 상장폐지 조회",
        description="해외 증권시장 상장폐지 사실을 조회하여 글로벌 전략 수정 여부, 투자자 신뢰도 변화, 해외시장 철수 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_foreign_delisting_decision",
            "get_disclosure_list",
            "get_major_holder_changes",
            "get_single_acc",
            "get_executive_trading"
        ]
    )

    registry.register_tool(
        name="get_convertible_bond",
        korean_name="전환사채권 발행결정 조회",
        description="전환사채 발행 결정을 조회하여 자금조달 전략, 부채 리스크, 향후 주식수 변동과 지배구조 영향 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_disclosure_list",
            "get_stock_increase_decrease",
            "get_major_holder_changes",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_bond_with_warrant",
        korean_name="신주인수권부사채권 발행결정 조회",
        description="신주인수권부사채 발행결정을 조회하여 미래 지분 희석 리스크, 자금조달 목적, 부채 구조 변동 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_major_holder_changes",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_exchangeable_bond",
        korean_name="교환사채권 발행결정 조회",
        description="교환사채 발행결정을 조회하여 지분 희석 리스크, 특정 종목 연계 리스크, 자금조달 목적, 부채 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_corporation_code_by_name",
            "get_major_holder_changes",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_creditor_management_termination",
        korean_name="채권은행 관리절차 중단 조회",
        description="채권은행 등의 관리절차 종료 여부를 조회하고, 재무 정상화 진행상황과 향후 경영전략 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_disclosure_list",
            "get_major_holder_changes"
        ]
    )

    registry.register_tool(
        name="get_write_down_bond",
        korean_name="상각형 조건부자본증권 발행결정 조회",
        description="상각형 조건부자본증권 발행 내역을 조회하고, 자본확충 전략과 상각 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_treasury_stock_acquisition",
        korean_name="자기주식 취득 결정 조회",
        description="기업의 자기주식 취득 계획을 조회하고, 주가 방어 전략과 지배구조 변동 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_treasury_stock_disposal",
        korean_name="자기주식 처분 결정 조회",
        description="기업의 자기주식 처분 계획을 조회하고, 주주환원 전략과 지배구조 변화 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_treasury_stock_trust_contract",
        korean_name="자기주식취득 신탁계약 체결 결정 조회",
        description="기업의 자기주식 신탁계약 체결 내역을 조회하고, 주가 안정화 전략 및 지배구조 변화 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_treasury_stock_trust_termination",
        korean_name="자기주식취득 신탁계약 해지 결정 조회",
        description="기업의 자기주식 신탁계약 해지 내역을 조회하고, 주가 방어 전략 수정 및 경영 리스크 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_business_acquisition",
        korean_name="영업양수 결정 조회",
        description="기업의 영업 양수 결정을 조회하고, 구조 재편, 경영전략 전환, 내부거래 리스크 등을 종합 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_business_transfer",
        korean_name="영업양도 결정 조회",
        description="기업의 영업 양도 결정을 조회하고, 사업 철수, 내부자산 이전 리스크 등을 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_tangible_asset_acquisition",
        korean_name="유형자산 양수 결정 조회",
        description="기업의 대규모 유형자산 양수 결정을 조회하고, 자산구조 변화 및 특수관계자 거래 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_tangible_asset_transfer",
        korean_name="유형자산 양도 결정 조회",
        description="기업의 유형자산 양도 결정을 조회하고, 재무구조 변화와 내부자 거래 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호(8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_disclosure_list",
            "get_major_holder_changes"
        ]
    )

    registry.register_tool(
        name="get_other_corp_stock_acquisition",
        korean_name="타법인 주식 및 출자증권 양수결정 조회",
        description="타법인 주식 및 출자증권 양수 결정을 조회하고, 우회상장 리스크와 내부거래 가능성 등을 종합 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_other_corp_stock_transfer",
        korean_name="타법인 주식 및 출자증권 양도결정 조회",
        description="타법인 주식 및 출자증권 양도 결정을 조회하고, 핵심자산 정리 리스크와 지배구조 변화 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_stock_related_bond_acquisition",
        korean_name="주권 관련 사채권 양수결정 조회",
        description="전환사채, 신주인수권부사채 등 주권 관련 사채권 양수 결정을 조회하고, 향후 지분율 변동과 경영권 리스크 가능성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_stock_related_bond_transfer",
        korean_name="주권 관련 사채권 양도결정 조회",
        description="주식 관련 사채권 양도에 따른 유동성 확보 현황 및 잠재적 지분 구조 변화 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_single_acc"
        ]
    )
    
    registry.register_tool(
        name="get_merger",
        korean_name="회사합병 결정 조회",
        description="흡수합병 또는 신설합병 결정 공시를 조회하고, 합병비율, 외부평가 의견, 합병상대회사의 재무정보를 통해 지배구조 변화 및 재무 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_executive_trading"
        ]
    )

    registry.register_tool(
        name="get_division",
        korean_name="회사분할 결정 조회",
        description="인적분할 또는 물적분할 결정 공시를 조회하고, 분할방식, 이전사업, 신설법인 재무정보 등을 통해 지배구조 및 재무 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_executive_trading"
        ]
    )

    registry.register_tool(
        name="get_division_merger",
        korean_name="회사분할합병 결정 조회",
        description="분할과 합병이 동시에 이루어지는 복합 구조의 분할합병 결정을 조회하고, 사업 이전, 합병비율, 외부평가, 신설회사 리스크 등을 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_executive_trading"
        ]
    )

    registry.register_tool(
        name="get_stock_exchange",
        korean_name="주식교환·이전 결정 조회",
        description="주식의 포괄적 교환 또는 이전 결정을 조회하고, 교환비율, 외부평가, 대상 법인의 재무정보 등을 통해 지배구조 개편 및 리스크 요인 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bgn_de": {
                    "type": "string",
                    "description": "검색 시작 접수일자 (예: 20240101)"
                },
                "end_de": {
                    "type": "string",
                    "description": "검색 종료 접수일자 (예: 20241231)"
                }
            },
            "required": ["corp_code", "bgn_de", "end_de"]
        },
        linked_tools=[
            "get_single_acc",
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_foreign_listing_decision"
        ]
    )

    registry.register_tool(
        name="get_stock_increase_decrease",
        korean_name="증자·감자 현황 조회",
        description="정기보고서에 기재된 증자 및 감자 내역을 조회하고, 자본금 변동, 주식 수량 변화, 감자 형태 등을 바탕으로 지배구조 및 재무전략 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_single_acc",
            "get_disclosure_list",
            "get_major_holder_changes",
            "get_executive_trading"
        ]
    )

    registry.register_tool(
        name="get_treasury_stock",
        korean_name="자기주식 취득·처분 현황 조회",
        description="정기보고서를 기반으로 자기주식의 취득, 처분, 소각 내역을 조회하고, 주가 방어, 지배구조 조정, 자본 정책 등과의 연계성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_major_holder_changes",
            "get_disclosure_list",
            "get_single_acc",
            "get_executive_trading"
        ]
    )

    registry.register_tool(
        name="get_executive_info",
        korean_name="임원 현황 조회",
        description="정기보고서 기준 임원의 성명, 직위, 경력, 임기, 최대주주와의 관계 등을 조회하고, 경영진 구조 및 지배구조 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_executive_trading",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_employee_info",
        korean_name="직원 현황 조회",
        description="정기보고서 기준 직원 수, 근속연수, 고용형태, 평균 급여 등을 조회하고, 조직 안정성, 인건비 구조, 고용 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_single_acc",
            "get_executive_info",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_individual_compensation",
        korean_name="개별 임원 보수 조회",
        description="5억 원 초과 보수를 수령한 개별 임원의 보수 총액, 직위, 비포함 항목 등을 조회하고, 경영성과 대비 과도한 보상 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_executive_info",
            "get_employee_info",
            "get_disclosure_list"
        ]
    )
    
    registry.register_tool(
        name="get_total_compensation",
        korean_name="임원 전체 보수 조회",
        description="정기보고서를 기반으로 임원 전체 보수 총액, 평균 보수액, 수령 인원 등을 조회하고, 보상 집중도 및 보수 투명성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_individual_compensation",
            "get_executive_info",
            "get_employee_info",
            "get_disclosure_list"
        ]
    )
   
    registry.register_tool(
        name="get_individual_compensation_amount",
        korean_name="개인별 보수 지급 금액 조회",
        description="정기보고서에 공시된 5억 원 이상 보수를 수령한 상위 5인의 보수 총액, 직위, 비포함 항목 등을 조회하고, 보상 집중도 및 지배구조 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_total_compensation",
            "get_individual_compensation",
            "get_executive_info",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_investment_in_other_corp",
        korean_name="타법인 출자현황 조회",
        description="사업보고서에 공시된 타법인 출자 내역을 조회하고, 출자 목적, 보유 지분율, 장부가액, 평가손익, 피출자법인의 재무성과 등을 분석하여 그룹 전략 및 투자 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_major_holder_changes",
            "get_single_acc",
            "get_business_acquisition",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_stock_total",
        korean_name="주식 총수 현황 조회",
        description="정기보고서 내 발행가능 주식 수, 발행 주식 수, 감자 및 소각 주식 수, 자기주식 및 유통주식 수 등을 조회하고, 자본금 구조 및 유통물량 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_paid_in_capital_increase",
            "get_free_capital_increase",
            "get_capital_reduction",
            "get_major_holder_changes",
            "get_treasury_stock_acquisition",
            "get_treasury_stock_disposal"
        ]
    )

    registry.register_tool(
        name="get_debt_securities_issued",
        korean_name="채무증권 발행 실적 조회",
        description="정기보고서 기준 회사채·전환사채·교환사채 등의 발행 내역을 조회하고, 발행금액, 이자율, 만기, 상환여부 등을 통해 자금조달 구조 및 부채 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_single_acc",
            "get_write_down_bond",
            "get_major_holder_changes",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_commercial_paper_outstanding",
        korean_name="기업어음 미상환 잔액 조회",
        description="정기보고서 기준 기업어음(CP)의 잔여만기별 미상환 잔액을 조회하고, 단기차입 의존도 및 유동성 리스크, 차환 부담 구조 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_debt_securities_issued",
            "get_single_acc",
            "get_creditor_management",
            "get_bankruptcy"
        ]
    )

    registry.register_tool(
        name="get_short_term_bond_outstanding",
        korean_name="단기사채 미상환 잔액 조회",
        description="정기보고서 기준 단기사채(SB)의 잔여만기별 미상환 금액과 발행 한도 정보를 조회하고, 단기차입 의존도, 유동성 리스크, 차환 부담 수준 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_commercial_paper_outstanding",
            "get_single_acc",
            "get_creditor_management",
            "get_bankruptcy"
        ]
    )

    registry.register_tool(
        name="get_corporate_bond_outstanding",
        korean_name="회사채 미상환 잔액 조회",
        description="정기보고서를 기반으로 회사채의 잔존 만기별 미상환 금액, 총액, 발행 유형을 조회하고, 상환 집중 구조, 장기 레버리지 비중, 유동성 리스크 정량적 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_debt_securities_issued",
            "get_single_acc",
            "get_creditor_management",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_hybrid_securities_outstanding",
        korean_name="신종자본증권 미상환 잔액 조회",
        description="정기보고서를 기반으로 신종자본증권(하이브리드 증권)의 잔존 만기별 미상환 금액과 발행 유형을 조회하고, 자본 인정 구조, 상환 리스크, 재무 레버리지 영향 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_write_down_bond",
            "get_single_acc",
            "get_debt_securities_issued",
            "get_major_holder_changes"
        ]
    )

    registry.register_tool(
        name="get_conditional_capital_securities_outstanding",
        korean_name="조건부 자본증권 미상환 잔액 조회",
        description="정기보고서를 기반으로 상각형 조건부자본증권의 만기별 미상환 잔액과 발행 유형을 조회하고, 자본 잠식 리스크, 상각 조건 도달 가능성, 리파이낸싱 구조 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_write_down_bond",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_accounting_auditor_opinion",
        korean_name="회계감사인의 명칭 및 감사의견 조회",
        description="정기보고서를 기반으로 회계감사인의 감사의견, 핵심감사사항, 강조사항 등을 조회하여 회계 투명성, 내부통제 위험, 기업 지속 가능성에 대한 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_single_acc",
            "get_disclosure_list",
            "get_executive_info",
            "get_investment_in_other_corp"
        ]
    )

    registry.register_tool(
        name="get_audit_service_contract",
        korean_name="감사용역체결현황 조회",
        description="정기보고서를 기반으로 감사용역계약 체결 내역과 실제 감사 수행 결과를 비교하여 회계감사 품질, 보수 변동, 감사 독립성 리스크 등을 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_accounting_auditor_opinion",
            "get_executive_info",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_non_audit_service_contract",
        korean_name="회계감사인과의 비감사용역 계약체결 현황 조회",
        description="정기보고서를 기반으로 회계법인 또는 계열사와 체결된 비감사용역 계약 내역을 조회하고, 감사인의 독립성 침해 여부 및 경제적 종속 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_audit_service_contract",
            "get_accounting_auditor_opinion",
            "get_disclosure_list",
            "get_executive_info"
        ]
    )

    registry.register_tool(
        name="get_outside_director_status",
        korean_name="사외이사 및 그 변동현황 조회",
        description="정기보고서를 기반으로 사외이사의 수, 비율, 선임 및 해임 현황을 조회하고, 이사회 독립성, 사외이사 유지율, 지배구조 감시 기능 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_executive_info",
            "get_disclosure_list",
            "get_audit_committee",
            "get_major_shareholder"
        ]
    )

    registry.register_tool(
        name="get_unregistered_exec_compensation",
        korean_name="미등기임원 보수현황 조회",
        description="사업보고서를 기반으로 미등기임원에게 지급된 보수 총액, 인원수, 평균 보수를 조회하고, 내부자 보상 집중도 및 투명성, 보상 구조의 적절성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_individual_compensation",
            "get_employee_info",
            "get_total_compensation",
            "get_disclosure_list"
        ]
    )

    registry.register_tool(
        name="get_executive_compensation_approved",
        korean_name="이사·감사 전체의 보수현황 (주주총회 승인금액) 조회",
        description="사업보고서를 기반으로 이사, 감사, 사외이사 등의 보수에 대해 주주총회에서 승인된 금액을 조회하고, 실제 보수 집행 내역과 비교하여 보상 통제 수준과 집행률 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_total_compensation",
            "get_individual_compensation_amount",
            "get_disclosure_list",
            "get_executive_info"
        ]
    )

    registry.register_tool(
        name="get_executive_compensation_by_type",
        korean_name="이사·감사 전체의 보수현황 (보수지급금액 - 유형별) 조회",
        description="사업보고서를 기반으로 등기이사, 사외이사, 감사위원 등의 직책별 보수 지급 내역을 조회하고, 평균 보수 수준과 집중도, 보상 구조의 합리성 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_executive_compensation_approved",
            "get_total_compensation",
            "get_individual_compensation",
            "get_executive_info"
        ]
    )

    registry.register_tool(
        name="get_public_capital_usage",
        korean_name="공모자금의 사용내역 조회",
        description="사업보고서를 기반으로 유상증자나 전환사채 발행 등으로 조달된 자금의 사용 계획과 실제 사용 내역을 조회하고, 계획 대비 집행 수준과 내부통제 리스크 분석",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_paid_in_capital_increase",
            "get_convertible_bond",
            "get_disclosure_list",
            "get_single_acc"
        ]
    )

    registry.register_tool(
        name="get_private_capital_usage",
        korean_name="사모자금의 사용내역 조회",
        description="주요사항보고서를 기반으로 제3자배정 유상증자 등 사모방식으로 조달한 자금의 사용계획과 실제 집행 내역을 비교 분석하여, 운용 리스크와 계획 이탈 가능성 평가",
        parameters={
            "type": "object",
            "properties": {
                "corp_code": {
                    "type": "string",
                    "description": "기업 고유번호 (8자리)"
                },
                "bsns_year": {
                    "type": "string",
                    "description": "사업연도 (예: 2024)"
                },
                "reprt_code": {
                    "type": "string",
                    "description": "보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)"
                }
            },
            "required": ["corp_code", "bsns_year", "reprt_code"]
        },
        linked_tools=[
            "get_paid_in_capital_increase",
            "get_single_acc",
            "get_disclosure_list"
        ]
    )

    return registry
