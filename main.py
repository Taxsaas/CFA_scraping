import pyautogui
import time
import subprocess
import autoit
import os
import schedule
import datetime
import logging
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    filename='card_sales_automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def setup_logging():
    """로그 폴더 생성 및 로그 설정"""
    log_dir = "./logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 로그 파일명에 날짜 포함
    log_file = f"{log_dir}/card_sales_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 루트 로거에 핸들러 추가
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    logger.addHandler(file_handler)

    # 콘솔에도 출력
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    return logger


def main_task():
    """메인 자동화 작업 함수"""
    logger = setup_logging()
    start_time = datetime.datetime.now()
    logger.info(f"작업 시작: {start_time}")

    try:
        # .env 파일 로드
        load_dotenv()

        # 환경 변수에서 ID와 PW 가져오기
        ID_KEY = os.getenv("ID_KEY")
        PW_KEY = os.getenv("PW_KEY")

        # ID, PW가 제대로 로드되었는지 확인
        if not ID_KEY or not PW_KEY:
            logger.error("오류: .env 파일에서 ID_KEY 또는 PW_KEY를 찾을 수 없습니다.")
            return

        # CMD를 통해 Edge 열기 (팝업 차단 비활성화)
        subprocess.Popen([
            "cmd.exe", "/k", "start msedge.exe",
            "--incognito",
            "--disable-popup-blocking",
            "--disable-notifications",
            "--disable-infobars",
            "--disable-translate",
            "--no-first-run",
            "--no-default-browser-check",
            "--block-new-web-contents",
            "--disable-background-networking",
            "--disable-extensions",
            "--autoplay-policy=no-user-gesture-required",
            "--disable-features=TranslateUI,DownloadUI",
            "--disable-prompt-on-repost",
            "--bwsi"
        ])

        logger.info("Edge가 실행되었습니다!")
        time.sleep(1)  # Edge가 완전히 열릴 때까지 대기

        # Edge 창 활성화
        try:
            autoit.win_wait("[CLASS:Chrome_WidgetWin_1]", timeout=10)
            autoit.win_activate("[CLASS:Chrome_WidgetWin_1]")
            time.sleep(1)  # Brief pause to ensure activation
        except autoit.AutoItError:
            logger.error("Edge 창을 10초 내에 찾지 못했습니다")
            return
        time.sleep(2)  # 창이 활성화될 때까지 대기

        # 주소창으로 이동 (Ctrl + L)
        autoit.send("^l")  # Ctrl + L을 눌러 주소창에 포커스
        time.sleep(1)

        # URL 입력 및 Enter
        autoit.send("https://www.cardsales.or.kr/signin{ENTER}")
        logger.info("URL로 이동했습니다!")
        time.sleep(3)

        # 이미지 인식 시도
        try:
            # ./img 폴더에서 이미지 찾기
            username_field = pyautogui.locateOnScreen("./img/username_field.png", confidence=0.8)
            if username_field:
                # 이미지 위치로 이동 후 클릭
                center = pyautogui.center(username_field)
                pyautogui.moveTo(center, duration=0.1)
                pyautogui.click()
                pyautogui.typewrite(ID_KEY, interval=0.1)  # 환경 변수에서 가져온 ID 사용
            else:
                logger.warning("사용자 이름 필드를 찾을 수 없습니다.")
        except pyautogui.ImageNotFoundException:
            logger.error("이미지를 찾을 수 없습니다: username_field.png")
        logger.info("ID입력 완료")

        try:
            # ./img 폴더에서 이미지 찾기
            password_field = pyautogui.locateOnScreen("./img/password_field.png", confidence=0.8)
            if password_field:
                # 이미지 위치로 이동 후 클릭
                center = pyautogui.center(password_field)
                pyautogui.moveTo(center, duration=0.1)
                pyautogui.click()
                pyautogui.typewrite(PW_KEY, interval=0.1)  # 환경 변수에서 가져온 PW 사용
            else:
                logger.warning("비밀번호 필드를 찾을 수 없습니다.")
        except pyautogui.ImageNotFoundException:
            logger.error("이미지를 찾을 수 없습니다: password_field.png")
        logger.info("PWD입력 완료")

        # 로그인 버튼 찾기 - ./img 폴더에서 이미지 찾기
        login_button = pyautogui.locateOnScreen("./img/login_button.png", confidence=0.8)
        if login_button:
            center = pyautogui.center(login_button)
            pyautogui.moveTo(center, duration=0.1)
            pyautogui.click()
            logger.info("로그인 시도 완료!")
        else:
            logger.warning("로그인 버튼을 찾을 수 없습니다.")

        # 로그인 성공 후 대기
        logger.info("로그인 페이지 로딩 대기 중...")
        time.sleep(5)  # 로그인 처리 및 페이지 전환 대기

        # 빈 화면 아무데나 한번 클릭
        try:
            # 화면 크기 가져오기
            screen_width, screen_height = pyautogui.size()

            # 화면 중앙 부분 계산 (네비게이션 바나 헤더를 피하기 위해 약간 아래쪽)
            center_x = screen_width // 2
            center_y = (screen_height // 2) + 100

            # 계산된 위치로 이동 후 클릭
            pyautogui.moveTo(center_x, center_y, duration=0.1)
            pyautogui.click()
            logger.info("빈 화면 클릭 완료!")
        except Exception as e:
            logger.error(f"빈 화면 클릭 중 오류 발생: {e}")

        # 주소창으로 이동 (Ctrl + L)
        autoit.send("^l")  # Ctrl + L을 눌러 주소창에 포커스
        time.sleep(0.5)

        # 기존 내용 전체 선택 후 삭제
        autoit.send("^a")  # Ctrl + A로 모든 텍스트 선택
        time.sleep(0.2)
        autoit.send("{DELETE}")  # 선택된 내용 삭제
        time.sleep(0.2)

        # 자동완성 메뉴를 닫기 위해 ESC 키 한 번 누르기
        autoit.send("{ESC}")
        time.sleep(0.2)

        # URL 직접 타이핑 (모드 1 = 느린 타이핑)
        autoit.send("https://www.cardsales.or.kr/page/purchase/day ", 1)  # 정수 1 사용 (느린 타이핑 모드)
        time.sleep(0.2)

        # 입력 완료 후 엔터
        autoit.send("{ENTER}")
        logger.info("매입 내역 URL로 이동했습니다!")

        # 페이지 로딩 대기
        time.sleep(3)

        # loading.png 찾아서 클릭
        try:
            loading_button = pyautogui.locateOnScreen("./img/loading.png", confidence=0.8)
            if loading_button:
                center = pyautogui.center(loading_button)
                pyautogui.moveTo(center, duration=0.1)
                pyautogui.click()
                logger.info("로딩 버튼 클릭 완료!")
            else:
                logger.warning("로딩 버튼을 찾을 수 없습니다.")
        except pyautogui.ImageNotFoundException:
            logger.error("로딩 버튼 이미지를 찾을 수 없습니다.")

        # 데이터 로딩 대기
        time.sleep(5)

        try:
            # 1단계: 테이블 헤더(카드사/매입건수) 영역 먼저 인식
            table_header = pyautogui.locateOnScreen("./img/check_box0.png", confidence=0.8)
            if table_header:
                logger.info("테이블 헤더 영역 인식 완료!")

                # 2단계: 체크박스 인식 및 클릭
                checkbox = pyautogui.locateOnScreen("./img/check_box.png", confidence=0.8)
                if checkbox:
                    center = pyautogui.center(checkbox)
                    pyautogui.moveTo(center, duration=0.1)
                    pyautogui.click()
                    logger.info("상단 체크박스 클릭 완료!")
                else:
                    logger.warning("상단 체크박스를 찾을 수 없습니다.")
            else:
                logger.warning("테이블 헤더 영역을 찾을 수 없습니다.")
        except pyautogui.ImageNotFoundException:
            logger.error("이미지를 찾을 수 없습니다.")

        # 짧은 대기
        time.sleep(1)

        # detail_search.png 클릭
        try:
            detail_search = pyautogui.locateOnScreen("./img/detail_search.png", confidence=0.8)
            if detail_search:
                center = pyautogui.center(detail_search)
                pyautogui.moveTo(center, duration=0.1)
                pyautogui.click()
                logger.info("상세 검색 버튼 클릭 완료!")
            else:
                logger.warning("상세 검색 버튼을 찾을 수 없습니다.")
        except pyautogui.ImageNotFoundException:
            logger.error("상세 검색 버튼 이미지를 찾을 수 없습니다.")

        # 상세 검색 대화 상자 로드 대기
        time.sleep(2)

        # excel_download.png 클릭
        try:
            excel_download = pyautogui.locateOnScreen("./img/excel_download.png", confidence=0.8)
            if excel_download:
                center = pyautogui.center(excel_download)
                pyautogui.moveTo(center, duration=0.1)
                pyautogui.click()
                logger.info("Excel 다운로드 버튼 클릭 완료!")
            else:
                logger.warning("Excel 다운로드 버튼을 찾을 수 없습니다.")
        except pyautogui.ImageNotFoundException:
            logger.error("Excel 다운로드 버튼 이미지를 찾을 수 없습니다.")

        # 다운로드 완료 대기
        time.sleep(10)

        # Edge 브라우저 종료
        autoit.send("!{F4}")  # Alt+F4
        logger.info("Edge 브라우저를 종료했습니다.")

        end_time = datetime.datetime.now()
        duration = end_time - start_time
        logger.info(f"작업 종료: {end_time}")
        logger.info(f"총 소요 시간: {duration}")
        logger.info("모든 작업 완료!")

    except Exception as e:
        logger.error(f"작업 중 예외 발생: {e}")
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        logger.info(f"작업 비정상 종료: {end_time}")
        logger.info(f"총 소요 시간: {duration}")


def run_schedule():
    """스케줄러 실행"""
    logger = setup_logging()
    logger.info("카드세일즈 자동화 스케줄러가 시작되었습니다.")
    logger.info("매일 오전 6:00에 자동으로 실행됩니다.")

    # 매일 아침 6시에 작업 실행
    schedule.every().day.at("06:00").do(main_task)

    # 테스트 목적으로 지금 바로 실행 (선택 사항)
    # logger.info("테스트를 위해 지금 바로 작업을 실행합니다.")
    # main_task()

    # 무한 루프로 스케줄 체크
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 스케줄 체크


if __name__ == "__main__":
    run_schedule()