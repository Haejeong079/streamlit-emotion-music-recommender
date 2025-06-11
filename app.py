import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="키워드 감정 기반 노래 추천기", layout="centered")

# ✅ 키워드 감정 추출 함수
def extract_emotion_keyword(text):
    text = text.lower()
    if any(word in text for word in ["기쁘", "좋", "행복", "웃", "사랑"]):
        return "joy"
    elif any(word in text for word in ["우울", "슬픔", "외로", "눈물", "그리움"]):
        return "sadness"
    elif any(word in text for word in ["화", "짜증", "분노", "열받"]):
        return "anger"
    elif any(word in text for word in ["편안", "조용", "차분"]):
        return "calm"
    else:
        return "unknown"

# ✅ 추천 함수
def recommend_by_emotion(df, emotion_label, top_n=5):
    filtered = df[df["emotion"] == emotion_label].copy()
    filtered = filtered.sort_values(by="Popularity", ascending=False)
    return filtered[["song", "artist", "emotion", "Popularity"]].head(top_n)

# ✅ 데이터 로드
@st.cache_resource
def load_data():
    path = "light_spotify_dataset.csv"
    if not os.path.exists(path):
        st.error("데이터셋이 없습니다. 파일을 업로드해주세요.")
        st.stop()
    return pd.read_csv(path)

df = load_data()

# ✅ UI
st.title("🎧 키워드 기반 감정 분석 + 노래 추천")
st.markdown("기분이나 상황을 간단히 적어보세요. 감정을 추출하여 노래를 추천해드립니다.")

user_input = st.text_area("🗣️ 지금 기분은 어떤가요?", height=100)

if st.button("🎯 감정 분석 및 추천"):
    if not user_input.strip():
        st.warning("먼저 문장을 입력해주세요.")
    else:
        emotion = extract_emotion_keyword(user_input)
        st.write(f"🧠 분석된 감정: **{emotion}**")

        if emotion == "unknown":
            st.warning("감정을 파악할 수 없습니다. 다른 표현을 사용해보세요.")
        else:
            rec_df = recommend_by_emotion(df, emotion)
            if not rec_df.empty:
                st.success("🎵 추천 곡 리스트:")
                st.dataframe(rec_df)
            else:
                st.warning("해당 감정에 대한 추천곡이 없습니다.")
