# CFA_scraping

---

```markdown
# 📊 카드세일즈 자동화 스크립트

카드세일즈 웹사이트([https://www.cardsales.or.kr](https://www.cardsales.or.kr))에 자동 로그인하여, 매일 오전 6시에 매입내역을 조회하고 Excel 파일로 다운로드하는 자동화 스크립트입니다.

## 📦 주요 기능
- `.env` 파일을 통한 ID/PW 보안 관리
- Microsoft Edge 브라우저 자동 실행 및 조작
- 이미지 기반 UI 자동화 (PyAutoGUI)
- Excel 다운로드 자동화
- 스케줄링 기반 자동 실행 (매일 오전 6시)
- 상세 로깅 기능

---

## 🛠️ 설치 및 실행 방법

### 1. 필수 환경 구성

#### 🐍 Python 패키지 설치
```bash
pip install pyautogui python-dotenv schedule autoit
```

#### 📁 추가 설정
- `Microsoft Edge` 브라우저가 설치되어 있어야 합니다.
- 이미지 기반 자동화를 위해 화면 해상도 및 DPI 설정은 **변하지 않아야** 합니다.

### 2. `.env` 파일 생성

프로젝트 루트에 `.env` 파일을 만들고 아래와 같이 작성합니다:

```
ID_KEY=your_username
PW_KEY=your_password
```

> 💡 보안을 위해 `.env` 파일은 `.gitignore`에 포함시키세요.

### 3. 이미지 리소스 준비

스크립트는 `./img/` 폴더에 있는 아래 이미지를 기반으로 작동합니다:

| 이미지 파일명 | 용도 |
|---------------|------|
| username_field.png | ID 입력 필드 인식 |
| password_field.png | 비밀번호 입력 필드 인식 |
| login_button.png   | 로그인 버튼 인식 |
| loading.png        | 로딩 버튼 인식 |
| check_box0.png     | 테이블 헤더 확인 |
| check_box.png      | 전체 선택 체크박스 |
| detail_search.png  | 상세 검색 버튼 |
| excel_download.png | 엑셀 다운로드 버튼 |

각 이미지의 정확한 캡처가 매우 중요합니다. 해상도나 브라우저 UI가 다르면 인식되지 않을 수 있습니다.

---

## ▶️ 실행 방법

### 수동 실행
```bash
   python main.py
```

### 자동 스케줄 실행
스크립트는 `run_schedule()` 함수를 통해 매일 오전 6시에 자동 실행됩니다.  
프로그램을 항상 실행 상태로 유지하려면 백그라운드 실행 또는 작업 스케줄러 등록이 필요합니다.

---

## 📁 로그 확인

스크립트는 `./logs/` 폴더에 날짜별 로그를 저장합니다.  
또한 `card_sales_automation.log` 파일에도 최근 로그가 기록됩니다.

---

## ⛔ 주의 사항
- **이미지 인식 기반**으로 작동하므로 화면 구성이 변경되면 인식이 실패할 수 있습니다.
- 화면 해상도 또는 배율(100%, 125% 등)은 고정하는 것이 좋습니다.
- 보안 팝업이나 알림창 등이 열리면 자동화가 중단될 수 있습니다.
- 자동화 도중 예외가 발생하면 로그에 기록되며, Edge 브라우저는 자동 종료됩니다.

---

## 📌 사용 기술

- Python
- [PyAutoGUI](https://pyautogui.readthedocs.io/)
- [AutoIt](https://www.autoitscript.com/site/autoit/)
- [Schedule](https://schedule.readthedocs.io/en/stable/)
- dotenv (.env 환경변수)
- subprocess / logging 모듈

---
