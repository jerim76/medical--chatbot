# medical--chatbot
import streamlit as st
import random

# Medical knowledge base (for testing only - not real medical advice)
MEDICAL_KNOWLEDGE = {
    "minor burns": {
        "steps": [
            "Cool the burn under cool running water for 10-15 minutes",
            "Apply aloe vera gel or antibiotic ointment",
            "Cover with sterile non-stick gauze",
            "Take OTC pain reliever if needed"
        ],
        "medications": ["Ibuprofen (Advil)", "Acetaminophen (Tylenol)", "Burn cream"],
        "warning": "Seek emergency care for large burns, facial burns, or charred skin"
    },
    "sprains": {
        "steps": [
            "Rest the injured area",
            "Apply ice pack for 20 minutes every 2-3 hours",
            "Use compression bandage",
            "Elevate above heart level"
        ],
        "medications": ["Ibuprofen (Advil)", "Naproxen (Aleve)", "Acetaminophen (Tylenol)"],
        "warning": "See a doctor if you can't bear weight or hear a popping sound"
    },
    "cuts": {
        "steps": [
            "Apply direct pressure with clean cloth",
            "Rinse with clean water",
            "Apply antibiotic ointment",
            "Cover with sterile bandage"
        ],
        "medications": ["Antibiotic ointment (Neosporin)", "Hydrogen peroxide", "Adhesive bandages"],
        "warning": "Go to ER if bleeding doesn't stop after 10 minutes of pressure"
    },
    "headache": {
        "steps": [
            "Rest in quiet, dark room",
            "Apply cool compress to forehead",
            "Gently massage temples",
            "Stay hydrated"
        ],
        "medications": ["Aspirin", "Acetaminophen (Tylenol)", "Ibuprofen (Advil)"],
        "warning": "Seek immediate help for sudden severe headache or after head injury"
    },
    "fever": {
        "steps": [
            "Drink plenty of fluids",
            "Take lukewarm bath",
            "Use light clothing",
            "Rest"
        ],
        "medications": ["Acetaminophen (Tylenol)", "Ibuprofen (Advil)", "Aspirin (adults only)"],
        "warning": "See doctor if fever >103°F (39.4°C) or lasts more than 3 days"
    }
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your First Aid Assistant. Describe your minor injury or symptom."}
    ]

# Chat UI
st.title("🤖 First Aid Chat Assistant")
st.caption("⚠️ For testing purposes only - Not real medical advice")

# Display messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input("Describe your issue..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Process input
    response = ""
    prompt_lower = prompt.lower()
    
    # Identify condition
    condition_found = None
    for condition in MEDICAL_KNOWLEDGE:
        if condition in prompt_lower:
            condition_found = condition
            break
    
    # Generate response
    if condition_found:
        info = MEDICAL_KNOWLEDGE[condition_found]
        response = f"**For {condition_found.capitalize()}:**\n\n"
        response += "**First Aid Steps:**\n" + "\n".join(f"- {step}" for step in info["steps"])
        response += "\n\n**Possible Medications:**\n" + ", ".join(info["medications"])
        response += f"\n\n⚠️ **Warning:** {info['warning']}"
    else:
        generic_responses = [
            "Please describe your symptoms in more detail",
            "I specialize in minor injuries - could you clarify your symptoms?",
            "For serious medical emergencies, call 911 or go to ER immediately",
            "I'm currently trained to handle: " + ", ".join(MEDICAL_KNOWLEDGE.keys())
        ]
        response = random.choice(generic_responses)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
