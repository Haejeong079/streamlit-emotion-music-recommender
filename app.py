import streamlit as st
import pandas as pd
import os
from collections import Counter

st.set_page_config(page_title="감정 기반 노래 추천기", layout="centered")

# ✅ 감정 키워드 사전
SAD_KEYWORDS = ["우울", "슬퍼", "울었", "외로", "눈물", "지쳤", "힘들", "괴로워", "절망", "고통"]
JOY_KEYWORDS = ["좋아", "행복", "웃", "사랑", "기뻐", "즐거", "감사", "만족", "행운"]
ANGER_KEYWORDS = ["화나", "짜증", "열받", "분노", "안좋아", "개짜증", "속상", "불쾌", "혐오"]
CALM_KEYWORDS = ["편안", "조용", "차분", "평온", "휴식", "안정", "느긋"]
EXCITED_KEYWORDS = ["신나", "흥분", "재밌", "놀", "댄스", "들떠", "짜릿", "열광"]

# ✅ 감정 유사도 맵 (fallback)
similar_emotion_map = {
    "sadness": ["calm"],
    "joy": ["excited"],
    "anger": ["sadness"],
    "calm": ["joy"],
    "excited": ["joy"]
}

# ✅ 감정 추출 함수 (다중 키워드 기반)
def extract_emotion_from_text(text):
    text = text.lower()
    emotion_count = Counter()

    for word in SAD_KEYWORDS:
        if word in text: emotion_count["sadness"] += 1
    for word in JOY_KEYWORDS:
        if word in text: emotion_count["joy"] += 1
    for word in ANGER_KEYWORDS:
        if word in text: emotion_count["anger"] += 1
    for word in CALM_KEYWORDS:
        if word in text: emotion_count["calm"] += 1
    for word in EXCITED_KEYWORDS:
        if word in text: emotion_count["excited"] += 1

    if not emotion_count:
        return "unknown"

    return emotion_count.most_common(1)[0][0]

# ✅ 추천 함수 (유사 감정 fallback 포함)
def recommend_by_emotion_smart(df, emotion_label, top_n=5):
    filtered = df[df["emotion"] == emotion_label].copy()
    if len(filtered) < top_n:
        for alt in similar_emotion_map.get(emotion_label, []):
            alt_filtered = df[df["emotion"] == alt]
            filtered = pd.concat([filtered, alt_filtered])
            if len(filtered) >= top_n:
                break
    filtered = filtered.sort_values(by="Popularity", ascending=False)
    return filtered[["song", "artist", "emotion", "Popularity"]].head(top_n)

# ✅ 데이터 불러오기
@st.cache_resource
def load_dataset():
    path = "light_spotify_dataset.csv"
    if not os.path.exists(path):
        st.error("❌ light_spotify_dataset.csv 파일이 없습니다.")
        st.stop()
    return pd.read_csv(path)

df = load_dataset()

# ✅ UI
st.title("🎧 문장 기반 감정 분석 + 노래 추천기")

st.markdown("""
기분이나 상황을 간단히 적어주세요.  
🤖 감정을 분석하고 🎵 감정에 어울리는 노래를 추천해드립니다.
""")

# ✅ 예시 제공
with st.expander("💡 입력 예시 보기"):
    st.markdown("""
- 😊 오늘 너무 행복해서 친구들과 놀러 갔어요  
- 😢 외롭고 슬픈 밤이야  
- 😠 진짜 화나고 짜증나는 하루였어  
- 😌 오늘은 차분하고 조용한 분위기가 좋아요  
- 🕺 너무 신나서 춤추고 싶어!
""")

# ✅ 입력창
user_input = st.text_area("🗣️ 지금 기분이나 상황을 자유롭게 적어보세요", height=100)

if st.button("🎯 감정 분석 + 추천"):
    if user_input.strip() == "":
        st.warning("문장을 입력해주세요.")
    else:
        emotion = extract_emotion_from_text(user_input)
        st.write(f"🧠 감정 분석 결과: **`{emotion}`**")

        if emotion == "unknown":
            st.error("❌ 감정을 인식하지 못했습니다. 다른 표현을 사용해보세요.")
        else:
            rec_df = recommend_by_emotion_smart(df, emotion)
            if not rec_df.empty:
                st.success("🎵 추천 곡 리스트:")
                st.dataframe(rec_df)
            else:
                st.warning(f"추천 가능한 노래가 없습니다. `{emotion}` 감정 곡이 부족할 수 있습니다.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit + 감정 키워드 분류기")
