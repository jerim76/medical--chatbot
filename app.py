# app.py
import streamlit as st
import random
from datetime import datetime

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
        info = f"- **{med['name']}**: {med['dosage']}"
        if "max" in med:
            info += f" (Max: {med['max']})"
        formatted.append(info)
    return "\n".join(formatted)

# Chat UI
st.title("⚕️ Medical Assistance Chatbot")
st.caption("⚠️ For informational purposes only - Not a substitute for professional medical advice")

# Display disclaimer
with st.expander("Important Disclaimer"):
    st.warning("""
    This chatbot provides general health information and is not a substitute for professional medical advice. 
    Always consult with a qualified healthcare provider for diagnosis and treatment. 
    
    In case of emergency:
    - Call your local emergency number immediately
    - For US: Call 911 or go to nearest emergency room
    - For Poison Control: 1-800-222-1222
    """)

# Display messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input("Describe your symptoms or health concern..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Process input
    response = ""
    prompt_lower = prompt.lower()
    
    # Check if follow-up to previous condition
    if st.session_state.last_condition and any(keyword in prompt_lower for keyword in ["better", "worse", "same", "improved", "not"]):
        condition = st.session_state.last_condition
        info = MEDICAL_KNOWLEDGE[condition]
        
        if "better" in prompt_lower or "improved" in prompt_lower:
            response = f"Good to hear your {condition} is improving. Continue with:"
            response += "\n\n" + "\n".join(f"- {step}" for step in info["steps"])
            response += "\n\nIf symptoms return or worsen, consult a healthcare provider."
        else:
            response = f"Since your {condition} hasn't improved, I recommend:"
            response += "\n\n- Consult a healthcare professional within 24 hours"
            response += "\n- Continue with the self-care steps"
            response += "\n- Monitor for warning signs: " + info["warning"]
        
        st.session_state.last_condition = None
    
    # Process new input
    elif not response:
        result = get_condition_from_input(prompt_lower)
        
        if result["type"] == "emergency":
            response = result["response"]
            response += "\n\nAfter calling emergency services, please update me on your status when safe."
        
        elif result["type"] == "condition":
            condition = result["condition"]
            info = MEDICAL_KNOWLEDGE[condition]
            st.session_state.last_condition = condition
            
            response = f"**Based on your symptoms, this may relate to {condition.replace('_', ' ').title()}**\n\n"
            response += "**Recommended Care Steps:**\n" + "\n".join(f"- {step}" for step in info["steps"])
            response += "\n\n**Medication Options:**\n" + format_medication_info(info["medications"])
            response += f"\n\n⚠️ **Warning:** {info['warning']}"
            
            if "questions" in info:
                response += f"\n\n**To help further, please answer:**\n" + "\n".join(f"- {q}" for q in info["questions"])
        
        else:
            generic_responses = [
                "I understand you're not feeling well. Could you describe your symptoms in more detail?",
                "To help you better, please tell me more about what you're experiencing.",
                "I specialize in common medical issues. Could you clarify your main concern?",
                "For accurate assistance, please describe: What symptoms you have, how long they've lasted, and their severity.",
                "I'm here to help. Please share more details about your health concern."
            ]
            response = random.choice(generic_responses)
            response += "\n\nI can assist with: " + ", ".join([c.replace('_', ' ') for c in MEDICAL_KNOWLEDGE.keys()])
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# Add reset button
if st.button("Clear Conversation"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Medical Assistant. Please describe your symptoms or health concern."}
    ]
    st.session_state.last_condition = None
    st.experimental_rerun()
