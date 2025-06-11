import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ✅ 감정 키워드 기반 추출 함수
def extract_emotion_from_text(text):
    text = text.lower()
    if any(word in text for word in ["우울", "슬퍼", "울었", "외로", "눈물"]):
        return "sadness"
    elif any(word in text for word in ["좋아", "행복", "웃", "사랑", "기뻐"]):
        return "joy"
    elif any(word in text for word in ["화나", "짜증", "열받", "분노"]):
        return "anger"
    elif any(word in text for word in ["편안", "조용", "차분", "평온"]):
        return "calm"
    elif any(word in text for word in ["신나", "흥분", "재밌", "놀", "댄스"]):
        return "excited"
    else:
        return "unknown"

# ✅ 감정 기반 추천 함수
def recommend_by_emotion(df, emotion_label, top_n=5):
    filtered = df[df["emotion"] == emotion_label].copy()
    filtered = filtered.sort_values(by="Popularity", ascending=False)
    return filtered[["song", "artist", "emotion", "Popularity"]].head(top_n)

# ✅ 모델 및 데이터 불러오기
@st.cache_resource
def load_resources():
    df = pd.read_csv("light_spotify_dataset.csv")
    return df

df = load_resources()

# ✅ Streamlit UI 구성
st.set_page_config(page_title="감정 기반 노래 추천기", layout="centered")
st.title("🎧 텍스트 감정 분석 + 노래 추천")

st.markdown("""
당신의 감정을 자연어로 입력하면, 해당 감정에 어울리는 노래를 추천해드립니다.  
예시: `"오늘 너무 우울해서 빵을 샀어"` → 감정: *sadness* → 노래 추천 🎵
""")

# ✅ 사용자 입력
user_input = st.text_area("🗣️ 지금 기분이나 상황을 적어보세요", height=100)

# ✅ 추천 버튼
if st.button("🎯 감정 분석 후 추천"):
    if user_input.strip() == "":
        st.warning("먼저 문장을 입력해주세요.")
    else:
        emotion = extract_emotion_from_text(user_input)
        st.write(f"🧠 감정 분석 결과: **`{emotion}`**")

        if emotion == "unknown":
            st.error("❌ 감정을 인식하지 못했습니다. 더 명확한 문장을 입력해주세요.")
        else:
            rec_df = recommend_by_emotion(df, emotion, top_n=5)
            if not rec_df.empty:
                st.success("🎵 추천곡 리스트:")
                st.dataframe(rec_df)
            else:
                st.warning(f"추천 가능한 노래가 없습니다. 데이터셋에 `{emotion}` 감정이 적을 수 있습니다.")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit + Keyword Emotion Parser")