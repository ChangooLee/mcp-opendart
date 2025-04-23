import trio
from .server import run_server

def main():
    import sys
    # 간단한 인자 파싱 (test-connection 옵션 등 처리 가능)
    transport = "stdio"
    if len(sys.argv) > 1 and sys.argv[1] == "test-connection":
        # 간단한 연결 테스트: OpenDart에 서버 없이 요청 시도
        from .apis.client import OpenDartClient
        try:
            OpenDartClient().get("corpCode.xml")
            print("✅ OpenDART API 연결 성공")
        except Exception as e:
            print(f"❌ OpenDART API 연결 실패: {e}")
        return 0

    # transport나 port에 대한 인자 추가 파싱 (생략)

    # Trio를 통해 서버 실행
    trio.run(run_server, transport)
