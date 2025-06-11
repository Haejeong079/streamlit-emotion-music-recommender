# 🎧 문장 기반 감정 분석 + 노래 추천기

자연어 문장으로 기분이나 상황을 입력하면,  
🤖 감정을 분석하고 🎵 해당 감정에 어울리는 노래를 추천해주는 **감정 기반 음악 추천 시스템**입니다.
<img width="753" alt="스크린샷 2025-06-11 오후 5 26 02" src="https://github.com/user-attachments/assets/d064354d-f9f4-45ce-abc8-b373f2290522" />



---

## 🛠️ 주요 기능

- 자연어 문장을 통한 감정 분석 (Keyword 기반 Rule Matching)
- 감정(Label)에 따라 Spotify 음악 추천
- 인기순 상위 추천곡 5개 표시
- 간단한 입력 예시 제공 및 다크 UI 지원

---

## 🖼️ 예시 화면


### ✅ 입력 예시 보기
<img width="699" alt="스크린샷 2025-06-11 오후 5 26 24" src="https://github.com/user-attachments/assets/6ece1b4b-df7c-4d6c-89b7-3453b4d77169" />

### ✅ 감정 분석 및 추천 결과
<img width="724" alt="스크린샷 2025-06-11 오후 5 26 58" src="https://github.com/user-attachments/assets/1772f2b2-4d60-4f8c-85a2-24121cf0d353" />


---

## 📂 프로젝트 구조
📁 streamlit-emotion-music-recommender/
├── app.py # Streamlit 메인 앱 코드
├── light_spotify_dataset.csv # 감정 라벨이 부여된 Spotify 곡 데이터
├── requirements.txt # 실행에 필요한 Python 라이브러리 목록
├── assets/
│ ├── header.png
│ ├── input_examples.png
│ └── recommendation_result.png
└── README.md



---

## 📦 설치 및 실행 방법

1. Python 가상환경 생성 및 패키지 설치

```bash
pip install -r requirements.txt

