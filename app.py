# app.py
import streamlit as st
import random

MEDICAL_KNOWLEDGE = {
    # ... [same medical knowledge dictionary from previous code] ...
}

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your First Aid Assistant. Describe your minor injury or symptom."}
    ]

st.title("🤖 First Aid Chat Assistant")
st.caption("⚠️ For testing purposes only - Not real medical advice")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Describe your issue..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = ""
    prompt_lower = prompt.lower()
    
    condition_found = None
    for condition in MEDICAL_KNOWLEDGE:
        if condition in prompt_lower:
            condition_found = condition
            break
    
    if condition_found:
        info = MEDICAL_KNOWLEDGE[condition_found]
        response = f"**For {condition_found.capitalize()}:**\n\n"
        response += "**First Aid Steps:**\n" + "\n".join(f"- {step}" for step in info["steps"])
        response += "\n\n**Possible Medications:**\n" + ", ".join(info["medications"])
        response += f"\n\n⚠️ **Warning:** {info['warning']}"
    else:
        response = random.choice([
            "Please describe your symptoms in more detail",
            "I specialize in minor injuries - could you clarify?",
            "For emergencies, call 911 or go to ER immediately",
            "I can help with: " + ", ".join(MEDICAL_KNOWLEDGE.keys())
        ])
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
