import streamlit as st
import datetime
from google import genai

st.set_page_config(page_title="Asiya's Ultimate AI", page_icon="🧠", layout="centered")

import os
API_KEY = st.secrets.get("GEMINI_API_KEY")

def get_ai_response(user_query):
    query_lower = user_query.lower().strip()
    
    if "time" in query_lower or "waqt" in query_lower:
        return f"Is waqt live time **{datetime.datetime.now().strftime('%I:%M %p')}** ho raha hay."
    elif "date" in query_lower or "tareekh" in query_lower:
        return f"Aaj ki tareekh **{datetime.datetime.now().strftime('%B %d, %Y')}** hay."
        
    try:
        client = genai.Client(api_key=API_KEY)
        
        system_prompt = (
            "You are a friendly, funny, and highly intelligent AI study partner named 'Super Brain'. "
            "You are talking to Asiya. Always reply in a mix of Roman Urdu and simple English. "
            "Explain complex Physics, Maths, and Science concepts using funny real-life examples and emojis. "
            "Keep your responses clean, helpful, and concise."
        )
        
        full_context = f"Instructions: {system_prompt}\n\n"
        
        for msg in st.session_state.messages:
            role_label = "User" if msg["role"] == "user" else "Model"
            full_context += f"{role_label}: {msg['text']}\n"
            
        full_context += f"User: {user_query}\nModel:"

        # ✅ Sahi and stable model setup bina kisi extra symbols ya pipes ke
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=full_context,
        )
        return response.text
    except Exception as e:
        return f"Yaar server busy hai ya connection ka masla hai. Koshish karein ke dubara send karein. Error: {str(e)}"

st.title("🧠 Asiya's Super AI Brain")
st.write("Welcome! Ab yeh chatbot Physics, Maths, Science sab kuch janta hai! 🚀")
st.markdown("---")

if "username" not in st.session_state:
    st.session_state.username = ""

if st.session_state.username == "":
    naam_input = st.text_input("👉 Apna naam likhein aur Enter dabayein:")
    if naam_input:
        st.session_state.username = naam_input
        st.rerun()
else:
    st.success(f"Logged in as: **{st.session_state.username}** ✨")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    if user_msg := st.chat_input("Mujhe se Physics, Maths ya koi bhi logical sawal poochhein..."):
        with st.chat_message("user"):
            st.write(user_msg)
        st.session_state.messages.append({"role": "user", "text": user_msg})

        reply = get_ai_response(user_msg)

        with st.chat_message("assistant"):
            st.write(reply)
        st.session_state.messages.append({"role": "assistant", "text": reply})
