import streamlit as st
import random
import time
from utils.script_manager import ScriptManager
from utils.surveys import DEMOGRAPHICS, FLOW_QUESTIONS, OWNERSHIP_QUESTIONS, OUTCOMES
from utils.data_manager import save_response
import os
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Page Configuration
# st.set_page_config(page_title="Skincare Personal Assistance", page_icon="✨", layout="centered")
st.set_page_config(page_title="Skincare Personal Assistance", page_icon="✨", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');

    .main {
        background-color: #Fdfdfd;
        font-family: 'Lato', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #2C3E50;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        border: none;
        background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%);
        color: white;
        font-weight: bold;
        padding: 12px 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #FECFEF 0%, #FF9A9E 100%);
        color: white;
    }
    
    .hero-container {
        background-color: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .hero-text {
        font-size: 1.2rem;
        color: #555;
        line-height: 1.6;
    }
    
    /* Hide the Streamlit footer */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION & ASSETS ---
# Cuter Bot Avatar (Cartoon Girl)
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/6997/6997662.png" 
# User Avatar (Girl)
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/4140/4140047.png"

# Product Image 
# PRODUCT_IMAGE = "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
# Reliable Home Image
# HOME_IMAGE = "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"

# Local Images
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images')
HOME_IMAGE_PATH = os.path.join(IMAGES_DIR, 'products.png')
DISPENSER_IMAGE_PATH = os.path.join(IMAGES_DIR, 'dispenser.png')

# Recommended images
PRODUCT_IMAGES = {
    "Hydra-Glow Satin Serum": "images/hydraglow.png",
    "AquaLuxe Ultra Nectar": "images/aqualuxe.png",
    "GlowMist Silky Essence": "images/glowmist.png",
    "AloeVelvet Lumi Shine": "images/aloevelvet.png"
}

PRODUCT_BY_CONDITION = {
    ("Flow", "High"): "Hydra-Glow Satin Serum",
    ("Flow", "Low"): "AquaLuxe Ultra Nectar",
    ("Ownership", "High"): "GlowMist Silky Essence",
    ("Ownership", "Low"): "AloeVelvet Lumi Shine"
}


# --- SESSION STATE INITIALIZATION ---
if 'responses_submitted' not in st.session_state:
    st.session_state['responses_submitted'] = False

if 'experiment_group' not in st.session_state:
    st.session_state['experiment_group'] = random.choice(['Flow', 'Ownership'])
    st.session_state['condition_type'] = random.choice(['High', 'Low'])
    st.session_state['full_condition'] = f"{st.session_state['condition_type']} {st.session_state['experiment_group']}"
    
    st.session_state['messages'] = []
    st.session_state['step_index'] = 0
    st.session_state['chat_finished'] = False
    st.session_state['user_name'] = "User"
    st.session_state['started'] = False
    st.session_state['consent_given'] = False # Default: Consent not given
    
    st.session_state['script_manager'] = ScriptManager()

def next_step():
    st.session_state['step_index'] += 1

def handle_option_click(option_text):

    current_step = st.session_state['script_manager'].steps[st.session_state['step_index']]

    # STORE USER CHOICES FOR CHAINING
    if current_step == "ask_skin_type":
        st.session_state['skin_type'] = option_text

    elif current_step == "ask_concern":
        st.session_state['skin_concern'] = option_text

    elif current_step == "ask_routine":
        st.session_state['routine_level'] = option_text

    elif current_step == "ask_duration":
        st.session_state['duration'] = option_text

    elif current_step == "ask_sun":
        st.session_state['sun'] = option_text

    # Add User Message
    msg_content = f"<span style='color: #2980B9;'>{option_text}</span>"
    st.session_state['messages'].append({"role": "user", "content": msg_content})

    # Move forward
    if st.session_state['script_manager'].steps[st.session_state['step_index']] != "recommendation":
        next_step()



# --- FUNCTION TO ADD BOT MESSAGE ---
def add_bot_message_for_current_step():
    bot_text, options = st.session_state['script_manager'].get_message_data(
    st.session_state['step_index'],
    st.session_state['full_condition'],
    user_name=st.session_state.get('user_name', 'User'),
    #skin_type=st.session_state.get("ask_skin_type", ""),
    #skin_concern=st.session_state.get("ask_concern", ""),
    #routine_level=st.session_state.get("ask_routine", "")

    skin_type=st.session_state.get('skin_type', ''),
    skin_concern=st.session_state.get('skin_concern', ''),
    routine_level=st.session_state.get('routine_level', '')
    )


    if bot_text:
        # Style Bot Message (Dark / Standard Color)
        # Note: We apply styling in the markdown string
        styled_text = f"<span style='color: #4A235A;'>{bot_text}</span>"
        
        st.session_state['messages'].append({"role": "assistant", "content": styled_text})
        return True, options
    return False, None


# --- SECTION 0: CONSENT PAGE ---
if not st.session_state.get('consent_given', False):
    # st.title("Skin Kind Products") # Removed per user request
    st.subheader("Study Information & Consent")
    
    st.markdown("""
    Thank you for your interest in participating in this study.
    
    **Study Purpose:**
    This academic study aims to understand user interactions with Chatbots in the context of Personal Care product recommendations.
    
    **Your task:**
    To interact with the Chatbot of a hypothetical Skincare brand. Do so assuming that you are going through a real skincare consultation. 
    
    **Privacy:**
    -   No personal data will be stored or shared.
    -   Your responses are used purely for academic research purposes.
    -   The interaction is anonymous.

    **Researchers' Declaration:**
    The researchers declare that there are no financial, personal, or professional conflicts of interest related to this study.
    
    Please read the following consent statement:
    """)
    
    agree = st.checkbox("I have read the above information and agree to participate in this study.")
    
    if st.button("Proceed", type="primary", disabled=not agree):
        st.session_state['consent_given'] = True
        st.rerun()

# --- SECTION 1: HOME PAGE ---
elif not st.session_state['started']:
    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <!-- <h1 style='color: #2C3E50; font-family: "Playfair Display", serif;'>Skin Kind Products</h1> -->
        <h1 style="color:#780741; font-family:'Playfair Display', serif; white-space: nowrap;">Skin Kind Products </h1>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1], gap="large")
    
    with col1:
        st.image(HOME_IMAGE_PATH, use_container_width=True)
        
    with col2:
        st.markdown("""
        <div style='text-align: left; padding-top: 60px;'>
            <h3 style='color: #780741;'>Experience the future of personalized skincare.</h3>
            <p style='color: #780741; font-size: 1.1rem; line-height: 1.6;'>
                Our skincare assistant creates a unique formulation just for you. 
                Discover the perfect balance for your skin in minutes.
            </p>
            <p style='color: #888; font-size: 0.9rem; margin-bottom: 30px;'>
                <em>Takes approximately 3-4 minutes</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Chat", type="primary"):
            st.session_state['started'] = True
            
            # --- INITIALIZATION LOGIC (Greeting + First Question) ---
            # 1. Add Greeting (Step 0)
            add_bot_message_for_current_step()
            
            # 2. Advance to Step 1 (Ask Name) IMMEDIATELY
            next_step()
            
            # 3. Add Ask Name Question (Step 1)
            add_bot_message_for_current_step()
            
            st.rerun()

# --- SECTION 2: CHAT INTERFACE ---
elif not st.session_state['chat_finished']:
    st.subheader("Let us understand your skin")
    
    # Progress
    total_steps = st.session_state['script_manager'].get_total_steps()
    progress = min(st.session_state['step_index'] / total_steps, 1.0)
    st.progress(progress)
    
    # Display History
    for msg in st.session_state['messages']:
        avatar = BOT_AVATAR if msg["role"] == "assistant" else USER_AVATAR
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"], unsafe_allow_html=True)

    # Bot Turn Management
    # Logic: If the last message was from User, it's Bot's turn.
    # But because we auto-initialized Step 0 and 1, the last message is ALREADY from Assistant (Step 1).
    # So we mainly wait for User Input.
    
    # However, we need to handle the loop:
    # User Follows Up -> Bot Responds -> Check if closing
    
    last_role = st.session_state['messages'][-1]["role"] if st.session_state['messages'] else None
    
    if last_role == "user":
        # It's Bot's turn to respond to the user's latest input
        
        # Simulate typing
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            with st.spinner("Typing..."):
                time.sleep(1.0)
                
        # Get Bot Message for the NEW step
        success, _ = add_bot_message_for_current_step()
        
        if success:
            # Check if recommendation step
            if st.session_state['script_manager'].steps[st.session_state['step_index']] == "recommendation":
                group = st.session_state['experiment_group']
                condition = st.session_state['condition_type']
                product_name = PRODUCT_BY_CONDITION.get((group, condition))
                image_path = PRODUCT_IMAGES.get(product_name)
            
                #try:
                #    img_b64 = get_img_as_base64(image_path)
                #    img_html = f"<img src='data:image/png;base64,{img_b64}' width='300' style='border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>"
                #    st.session_state['messages'].append({"role": "assistant", "content": img_html})
                #except Exception as e:
                #    st.error(f"Image load error: {e}")

                try:
                img_b64 = get_img_as_base64(image_path)
            
                img_html = f"""
                <div style='text-align: center; margin: 15px 0;'>
                    <img src='data:image/png;base64,{img_b64}'
                         style='max-width: 85%; height: auto; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'
                                box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                </div>
                """

    st.session_state['messages'].append({"role": "assistant", "content": img_html})

except Exception as e:
    st.error(f"Image load error: {e}")



                # --- ADD CLOSING TEXT JUST BELOW RECOMMENDATION ---
                closing_index = st.session_state['step_index'] + 1
                
                closing_text, _ = st.session_state['script_manager'].get_message_data(
                    closing_index,
                    st.session_state['full_condition'],
                    user_name=st.session_state.get('user_name', ''),
                    skin_type=st.session_state.get('skin_type', ''),
                    skin_concern=st.session_state.get('skin_concern', ''),
                    routine_level=st.session_state.get('routine_level', '')
                )
                
                if closing_text:
                    styled_closing = f"<br><br><span style='color: #4A235A;'>{closing_text}</span>"
                    st.session_state['messages'].append({
                        "role": "assistant",
                        "content": styled_closing
                    })


            # If closing, finish
            if st.session_state['step_index'] >= total_steps - 1:
                time.sleep(2)
                st.session_state['chat_finished'] = True
                st.rerun()
            
            st.rerun()
        else:
            st.session_state['chat_finished'] = True
            st.rerun()


    # User Turn (Input Display)
    # If last message was from Assistant, show input controls
    if last_role == "assistant":
        
        # Get options for CURRENT step
        # Note: step_index is currently pointing to the question the bot JUST asked.
        # Wait, if bot asked Step 1 (Name), step_index is 1. We need input for Step 1.
        
        _, options = st.session_state['script_manager'].get_message_data(
            st.session_state['step_index'], 
            st.session_state['full_condition']
        )
        
        # If options exist, show buttons
        if options:
            st.write("Select an option:")
            # cols = st.columns(2) # options are in 2 columns
            cols = st.columns(len(options))   # all options in 1 row
            for i, opt in enumerate(options):
                # with cols[i % 2]: # options are in 2 columns
                with cols[i]:  # all options in 1 row
                    if st.button(opt, key=f"btn_{st.session_state['step_index']}_{i}"):
                        handle_option_click(opt)
                        st.rerun()
        
        # If no options (Text Input)
        else:
             # Check if we are at the recommendation step (After bot showed image)
             # The bot just showed the image. Now we want user to click proceed.
             current_step_name = st.session_state['script_manager'].steps[st.session_state['step_index']]
             
             if current_step_name == "recommendation":
                 if st.button("Proceed to Survey", type="primary"):
                     st.session_state['chat_finished'] = True
                     st.rerun()
             else:
                if prompt := st.chat_input("Type your answer..."):
                    step = st.session_state['step_index']
                
                    # STORE KEY ANSWERS
                    if step == 1:  # Name
                        st.session_state['user_name'] = prompt
                
                    elif step == 2:  # Skin type
                        st.session_state['skin_type'] = prompt
                
                    elif step == 3:  # Concern
                        st.session_state['skin_concern'] = prompt
                
                    elif step == 4:  # Routine level
                        st.session_state['routine_level'] = prompt
                
                    elif step == 5:  # Budget
                        st.session_state['budget'] = prompt
                
                    # Add User Message
                    styled_prompt = f"<span style='color: #2980B9;'>{prompt}</span>"
                    st.session_state['messages'].append({"role": "user", "content": styled_prompt})
                
                    next_step()
                    st.rerun()


# --- SECTION 3: SURVEY ---
else:
    st.subheader("Post-Interaction Survey")
    st.write("Thank you for chatting! Please answer the following questions.")
    
    with st.form("survey_form"):
        response_data = {}
        
        st.info("About You")
        for q in DEMOGRAPHICS:
            if q['type'] == 'number':
                response_data[q['id']] = st.number_input(q['question'], min_value=q.get('min_value', 0))
            elif q['type'] == 'select':
                response_data[q['id']] = st.selectbox(q['question'], q['options'])
            elif q['type'] == 'slider':
                # response_data[q['id']] = st.slider(q['question'], q['min'], q['max'], help=f"1={q['labels'][0]}, {q['max']}={q['labels'][1]}")
                
                response_data[q['id']] = st.slider(q['question'], q['min'], q['max'])
                # scale anchors under the slider
                st.markdown(
                    f"<div style='display:flex; justify-content:space-between; font-size:13px;  margin-bottom:50px;'>"
                    f"<span>{q['min']} ({q['labels'][0]})</span>"
                    f"<span>{q['max']} ({q['labels'][1]})</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )


        st.markdown("---")
        st.info("Your experience of the interaction")
        
        if st.session_state['experiment_group'] == 'Flow':
            questions = FLOW_QUESTIONS
        else:
            questions = OWNERSHIP_QUESTIONS
            
        for q in questions:
            #response_data[q['id']] = st.slider(q['question'], 1, 5, key=q['id'], help="1=Strongly Disagree, 5=Strongly Agree")
            response_data[q['id']] = st.slider(q['question'], 1, 5, key=q['id'])
            st.markdown(
                "<div style='display:flex; justify-content:space-between; font-size:13px;  margin-bottom:50px;'>"
                "<span>1 (Strongly Disagree)</span>"
                "<span>5 (Strongly Agree)</span>"
                "</div>",
                unsafe_allow_html=True
            )



        st.markdown("---")
        st.info("Final Thoughts")
        for q in OUTCOMES:
             # response_data[q['id']] = st.slider(q['question'], 1, 5, key=q['id'], help="1=Strongly Disagree, 5=Strongly Agree")
            response_data[q['id']] = st.slider(q['question'], 1, 5, key=q['id'])
            st.markdown(
                "<div style='display:flex; justify-content:space-between; font-size:13px;  margin-bottom:50px;'>"
                "<span>1 (Strongly Disagree)</span>"
                "<span>5 (Strongly Agree)</span>"
                "</div>",
                unsafe_allow_html=True
            )


        # submitted = st.form_submit_button("Submit Responses")
        submitted = st.form_submit_button("Submit Responses",disabled=st.session_state['responses_submitted'])

        
        if submitted and not st.session_state['responses_submitted']:
            #save_response()
            save_response(
                experiment_name=f"Experiment {st.session_state['experiment_group']}",
                condition=st.session_state['full_condition'],
                data_dict=response_data
            )
            st.session_state['responses_submitted'] = True
            # st.success("Thank you! Your responses have been recorded.")
            # Force refresh
            st.rerun()

    if st.session_state['responses_submitted']:
        st.success("Thank you! Your responses have been recorded.")

            


































