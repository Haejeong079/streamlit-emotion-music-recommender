import streamlit as st
st.set_page_config(page_title="감정 기반 노래 추천기", layout="centered")  # 반드시 최상단

import pandas as pd
import numpy as np
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ✅ 감정 기반 추천 함수
def recommend_by_emotion(df, emotion_label, top_n=5):
    filtered = df[df["emotion"] == emotion_label].copy()
    filtered = filtered.sort_values(by="Popularity", ascending=False)
    return filtered[["song", "artist", "emotion", "Popularity"]].head(top_n)

# ✅ 모델 및 데이터 불러오기
@st.cache_resource
def load_resources():
    file_path = "light_spotify_dataset.csv"
    if not os.path.exists(file_path):
        st.error(f"❌ '{file_path}' 파일이 존재하지 않습니다.")
        st.stop()
    df = pd.read_csv(file_path)
    return df

@st.cache_resource
def load_sentiment_model():
    model_name = "beomi/KcELECTRA-base"  # 또는 fine-tuned 감정 모델로 교체 가능
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
    return tokenizer, model

df = load_resources()
tokenizer, model = load_sentiment_model()

# ✅ Huggingface 감정 분류 함수
def classify_emotion_huggingface(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    label_idx = torch.argmax(probs, dim=1).item()

    label_map = {
        0: "sadness",
        1: "joy",
        2: "anger"
    }
    return label_map.get(label_idx, "unknown")

# ✅ Streamlit UI 구성
st.title("🎧 문장 기반 감정 분석 + 노래 추천")

st.markdown("""
자연어 문장으로 기분이나 상황을 입력하면,  
🤖 감정을 분석하고 🎵 해당 감정에 어울리는 노래를 추천해드립니다.
""")

# ✅ 사용자 입력
user_input = st.text_area("🗣️ 지금 기분이나 상황을 적어보세요", height=100)

# ✅ 추천 버튼
if st.button("🎯 감정 분석 후 추천"):
    if user_input.strip() == "":
        st.warning("먼저 문장을 입력해주세요.")
    else:
        with st.spinner("감정 분석 중..."):
            emotion = classify_emotion_huggingface(user_input)

        st.write(f"🧠 감정 분석 결과: **`{emotion}`**")

        if emotion == "unknown":
            st.error("❌ 감정을 인식하지 못했습니다. 다른 표현을 시도해보세요.")
        else:
            rec_df = recommend_by_emotion(df, emotion, top_n=5)
            if not rec_df.empty:
                st.success("🎵 추천곡 리스트:")
                st.dataframe(rec_df)
            else:
                st.warning(f"추천 가능한 노래가 없습니다. `{emotion}` 감정 곡이 부족할 수 있습니다.")

st.markdown("---")
st.caption("Made with ❤️ using Huggingface + Streamlit")
