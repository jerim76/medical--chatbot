import streamlit as st
import random
from datetime import datetime

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
    }
    
    /* Chat container */
    .stChatFloatingInputContainer {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        padding: 15px;
    }
    
    /* User messages */
    .user-message .stChatMessage {
        background-color: #d1e7ff !important;
        border-radius: 18px 18px 4px 18px !important;
        color: #004085;
    }
    
    /* Assistant messages */
    .assistant-message .stChatMessage {
        background-color: white !important;
        border-radius: 18px 18px 18px 4px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        color: #333;
    }
    
    /* Header styling */
    .header {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 114, 255, 0.3) !important;
    }
    
    /* Chat input */
    .stTextInput>div>div>input {
        border-radius: 20px !important;
        padding: 12px 20px !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* Emergency badge */
    .emergency-badge {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    /* Warning badge */
    .warning-badge {
        background: linear-gradient(90deg, #ffb347 0%, #ffcc33 100%);
        color: #333;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    /* Medication card */
    .medication-card {
        background: linear-gradient(135deg, #f5f9ff 0%, #e6f0ff 100%);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #4d94ff;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Step card */
    .step-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #33cc33;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #666;
        font-size: 0.85rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Comprehensive Medical Knowledge Base
MEDICAL_KNOWLEDGE = {
    # Pain Conditions
    "headache": {
        "symptoms": ["head pain", "migraine", "head throbbing", "tension head"],
        "questions": ["How long have you had the headache?", "Is the pain sharp or dull?", "Any light sensitivity?"],
        "steps": [
            "Rest in a quiet, dark room",
            "Apply cool compress to forehead",
            "Gently massage temples and neck",
            "Stay hydrated - drink water slowly"
        ],
        "medications": [
            {"name": "Acetaminophen (Tylenol)", "dosage": "500-1000mg every 4-6 hours", "max": "4000mg/day"},
            {"name": "Ibuprofen (Advil)", "dosage": "200-400mg every 4-6 hours", "max": "1200mg/day"},
            {"name": "Aspirin", "dosage": "325-650mg every 4 hours", "max": "4000mg/day"}
        ],
        "warning": "Seek emergency care if: Sudden severe headache, headache after injury, or with fever/stiff neck",
        "followup": "How is your headache now? Better or worse?"
    },
    "back pain": {
        "symptoms": ["backache", "spine pain", "lower back discomfort"],
        "questions": ["Did you lift something heavy?", "Is the pain radiating to legs?", "Any numbness/tingling?"],
        "steps": [
            "Apply ice pack for first 48 hours (20 mins on/40 mins off)",
            "After 48 hours, apply heat",
            "Gentle stretching exercises",
            "Maintain good posture when sitting"
        ],
        "medications": [
            {"name": "Ibuprofen (Advil)", "dosage": "400mg every 6 hours", "max": "3200mg/day"},
            {"name": "Acetaminophen (Tylenol)", "dosage": "650mg every 6 hours", "max": "4000mg/day"},
            {"name": "Topical pain reliever (Bengay, Icy Hot)", "dosage": "Apply thin layer 3-4 times daily"}
        ],
        "warning": "Seek immediate care if: Loss of bladder/bowel control, leg weakness, or trauma-related pain",
        "followup": "Is the pain localized or spreading?"
    },
    
    # Injury Conditions
    "sprain": {
        "symptoms": ["twisted ankle", "wrist injury", "ligament pain", "joint swelling"],
        "questions": ["Which joint is affected?", "Can you bear weight on it?", "How did it happen?"],
        "steps": [
            "Rest the injured area",
            "Ice for 20 minutes every 2 hours (first 48 hours)",
            "Compress with elastic bandage",
            "Elevate above heart level"
        ],
        "medications": [
            {"name": "Ibuprofen (Advil)", "dosage": "400mg every 6 hours", "max": "3200mg/day"},
            {"name": "Naproxen (Aleve)", "dosage": "220mg every 8-12 hours", "max": "660mg/day"}
        ],
        "warning": "See a doctor if: You heard a popping sound, can't move joint, or numbness occurs",
        "followup": "How's the swelling? Reduced or increased?"
    },
    "cut": {
        "symptoms": ["laceration", "bleeding", "skin tear", "abrasion"],
        "questions": ["How deep is the cut?", "Is bleeding controlled?", "Was it from a dirty object?"],
        "steps": [
            "Apply direct pressure with clean cloth for 10 mins",
            "Rinse with clean water",
            "Apply antibiotic ointment",
            "Cover with sterile bandage"
        ],
        "medications": [
            {"name": "Antibiotic ointment (Neosporin)", "dosage": "Apply thin layer 1-3 times daily"},
            {"name": "Hydrogen peroxide", "dosage": "Clean once then avoid repeated use"},
            {"name": "Acetaminophen for pain", "dosage": "500mg every 6 hours as needed"}
        ],
        "warning": "Go to ER if: Bleeding doesn't stop after 10 minutes, cut is deep/gaping, or caused by animal bite",
        "followup": "Is there any redness or swelling around the cut?"
    },
    
    # Illness Conditions
    "fever": {
        "symptoms": ["high temperature", "chills", "sweating", "body aches"],
        "questions": ["What's your temperature?", "How long have you had fever?", "Any other symptoms?"],
        "steps": [
            "Drink plenty of fluids (water, broth)",
            "Take lukewarm sponge bath",
            "Use light clothing and bedding",
            "Rest in comfortable environment"
        ],
        "medications": [
            {"name": "Acetaminophen (Tylenol)", "dosage": "500-1000mg every 4-6 hours", "max": "4000mg/day"},
            {"name": "Ibuprofen (Advil)", "dosage": "200-400mg every 6 hours", "max": "1200mg/day"}
        ],
        "warning": "Seek emergency care if: Fever >104°F (40°C), lasts more than 3 days, or with stiff neck/rash",
        "followup": "Has your temperature changed since last measurement?"
    },
    "cough": {
        "symptoms": ["coughing", "chest congestion", "throat irritation", "phlegm"],
        "questions": ["Is it dry or productive?", "Any breathing difficulty?", "How long have you had it?"],
        "steps": [
            "Stay hydrated with warm liquids",
            "Use humidifier or steam inhalation",
            "Prop head up when sleeping",
            "Avoid irritants (smoke, dust)"
        ],
        "medications": [
            {"name": "Dextromethorphan (cough suppressant)", "dosage": "10-20mg every 4 hours", "max": "120mg/day"},
            {"name": "Guaifenesin (expectorant)", "dosage": "200-400mg every 4 hours", "max": "2400mg/day"},
            {"name": "Honey (for adults)", "dosage": "1-2 teaspoons as needed"}
        ],
        "warning": "See doctor if: Coughing blood, lasts >3 weeks, or with chest pain/fever >101°F",
        "followup": "Is the cough productive? What color is the phlegm?"
    },
    
    # Additional Conditions
    "burn": {
        "symptoms": ["skin burn", "thermal injury", "scald", "sunburn"],
        "questions": ["What caused the burn?", "How large is it?", "Any blistering?"],
        "steps": [
            "Cool under running water for 10-15 minutes",
            "Apply aloe vera or antibiotic ointment",
            "Cover with sterile non-stick gauze",
            "Protect from sun exposure"
        ],
        "medications": [
            {"name": "Ibuprofen for pain", "dosage": "400mg every 6 hours", "max": "3200mg/day"},
            {"name": "Burn cream (Silvadene)", "dosage": "Apply thin layer twice daily"},
            {"name": "Aloe vera gel", "dosage": "Apply liberally as needed"}
        ],
        "warning": "Seek emergency care for: Burns larger than your palm, on face/hands/genitals, or charred skin",
        "followup": "How is the pain level now?"
    },
    "allergy": {
        "symptoms": ["sneezing", "itchy eyes", "rash", "hives", "swelling"],
        "questions": ["What triggered it?", "Any breathing difficulty?", "Where is the rash located?"],
        "steps": [
            "Remove allergen source if possible",
            "Take cool shower for skin reactions",
            "Use cold compress for swollen eyes",
            "Wear loose cotton clothing"
        ],
        "medications": [
            {"name": "Diphenhydramine (Benadryl)", "dosage": "25-50mg every 4-6 hours", "max": "300mg/day"},
            {"name": "Loratadine (Claritin)", "dosage": "10mg once daily", "max": "10mg/day"},
            {"name": "Hydrocortisone cream", "dosage": "Apply thin layer 2-4 times daily"}
        ],
        "warning": "Use epinephrine and call 911 for: Difficulty breathing, throat swelling, or dizziness",
        "followup": "Any changes in breathing or swelling?"
    }
}

# Emergency Protocol
EMERGENCY_KEYWORDS = {
    "chest pain": "🚨 Call emergency services immediately! This could be a heart attack.",
    "difficulty breathing": "🚨 Seek emergency care now! This could be a serious respiratory issue.",
    "severe bleeding": "🚨 Apply direct pressure and call emergency services!",
    "unconscious": "🚨 Call emergency services! Check breathing and perform CPR if trained.",
    "stroke symptoms": "🚨 Remember FAST: Face drooping, Arm weakness, Speech difficulty - Time to call emergency!",
    "severe allergic reaction": "🚨 Use epinephrine injector if available and call emergency services immediately!",
    "suicidal thoughts": "🚨 Call the National Suicide Prevention Lifeline at 988 immediately for help."
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Medical Assistant. Please describe your symptoms or health concern."}
    ]
if "last_condition" not in st.session_state:
    st.session_state.last_condition = None

# Helper functions
def get_condition_from_input(user_input):
    user_input = user_input.lower()
    
    # Check emergency keywords first
    for keyword, response in EMERGENCY_KEYWORDS.items():
        if keyword in user_input:
            return {"type": "emergency", "response": response}
    
    # Check specific conditions
    for condition, data in MEDICAL_KNOWLEDGE.items():
        # Check condition name
        if condition in user_input:
            return {"type": "condition", "condition": condition}
        
        # Check symptoms
        for symptom in data["symptoms"]:
            if symptom in user_input:
                return {"type": "condition", "condition": condition}
    
    return {"type": "unknown"}

def format_medication_info(meds):
    formatted = []
    for med in meds:
        info = f"""
        <div class="medication-card">
            <b>{med['name']}</b><br>
            <span style="color: #0066cc;">Dosage: {med['dosage']}</span>
            {f"<br><span style='color: #ff5500;'>Max: {med['max']}</span>" if "max" in med else ""}
        </div>
        """
        formatted.append(info)
    return "\n".join(formatted)

def format_steps_info(steps):
    formatted = []
    for i, step in enumerate(steps, 1):
        info = f"""
        <div class="step-card">
            <b>Step {i}:</b> {step}
        </div>
        """
        formatted.append(info)
    return "\n".join(formatted)

# Header with gradient background
st.markdown("""
<div class="header">
    <h1 style="margin:0; padding:0;">⚕️ MediAssist</h1>
    <p style="margin:0; padding:0; opacity:0.9;">Your personal medical assistant for minor health concerns</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with features and disclaimer
with st.sidebar:
    st.markdown("## 🌟 Features")
    st.markdown("""
    - Symptom analysis
    - First aid guidance
    - Medication suggestions
    - Emergency protocols
    - Follow-up questions
    """)
    
    st.markdown("## 📋 Common Conditions")
    cols = st.columns(2)
    for i, condition in enumerate(MEDICAL_KNOWLEDGE.keys()):
        with cols[i % 2]:
            st.info(f"• {condition.title()}")
    
    st.markdown("## ⚠️ Important Disclaimer")
    st.warning("""
    This chatbot provides general health information only. 
    It is not a substitute for professional medical advice. 
    
    For emergencies:
    - Call your local emergency number
    - In the US: Call 911
    - Poison Control: 1-800-222-1222
    """)

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">', unsafe_allow_html=True)
        st.chat_message("user").write(msg["content"])
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">', unsafe_allow_html=True)
        st.chat_message("assistant").write(msg["content"], unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# User input
if prompt := st.chat_input("Describe your symptoms or health concern..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process input
    response = ""
    prompt_lower = prompt.lower()
    
    # Check if follow-up to previous condition
    if st.session_state.last_condition and any(keyword in prompt_lower for keyword in ["better", "worse", "same", "improved", "not"]):
        condition = st.session_state.last_condition
        info = MEDICAL_KNOWLEDGE[condition]
        
        if "better" in prompt_lower or "improved" in prompt_lower:
            response = f"✅ Good to hear your {condition} is improving. Continue with:"
            response += f"\n{format_steps_info(info['steps']}"
            response += "\n\nIf symptoms return or worsen, consult a healthcare provider."
        else:
            response = f"⚠️ Since your {condition} hasn't improved, I recommend:"
            response += "\n\n- Consult a healthcare professional within 24 hours"
            response += f"\n{format_steps_info(info['steps']}"
            response += f"\n\n<div class='warning-badge'>Monitor for warning signs: {info['warning']}</div>"
        
        st.session_state.last_condition = None
    
    # Process new input
    elif not response:
        result = get_condition_from_input(prompt_lower)
        
        if result["type"] == "emergency":
            response = f"<div class='emergency-badge'>EMERGENCY ALERT</div>{result['response']}"
            response += "\n\nAfter calling emergency services, please update me on your status when safe."
        
        elif result["type"] == "condition":
            condition = result["condition"]
            info = MEDICAL_KNOWLEDGE[condition]
            st.session_state.last_condition = condition
            
            response = f"<div style='font-size:18px; color:#0066cc; margin-bottom:10px;'><b>Possible Condition: {condition.title()}</b></div>"
            
            response += "<div style='margin-bottom:15px;'><b>Recommended Care Steps:</b></div>"
            response += format_steps_info(info["steps"])
            
            response += "<div style='margin-top:20px; margin-bottom:10px;'><b>Medication Options:</b></div>"
            response += format_medication_info(info["medications"])
            
            response += f"\n\n<div class='warning-badge'>Important: {info['warning']}</div>"
            
            if "questions" in info:
                response += f"\n\n<div style='margin-top:20px;'><b>To help further, please answer:</b></div>"
                response += "\n".join(f"- {q}" for q in info["questions"])
        
        else:
            generic_responses = [
                "I understand you're not feeling well. Could you describe your symptoms in more detail?",
                "To help you better, please tell me more about what you're experiencing.",
                "I specialize in common medical issues. Could you clarify your main concern?",
                "For accurate assistance, please describe: What symptoms you have, how long they've lasted, and their severity.",
                "I'm here to help. Please share more details about your health concern."
            ]
            response = random.choice(generic_responses)
            response += "\n\nI can assist with: " + ", ".join([c.replace('_', ' ').title() for c in MEDICAL_KNOWLEDGE.keys()])
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Add reset button
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Medical Assistant. Please describe your symptoms or health concern."}
        ]
        st.session_state.last_condition = None
        st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>MediAssist v1.0 | For demonstration purposes only | Not for medical diagnosis</p>
    <p>Always consult with a qualified healthcare provider for medical advice</p>
</div>
""", unsafe_allow_html=True)
