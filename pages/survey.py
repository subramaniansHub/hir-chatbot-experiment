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

# Page Configuration
st.set_page_config(page_title="Post-Interaction Survey", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
/* Hide sidebar completely */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Remove the top-left hamburger / collapse button */
button[kind="header"] {
    display: none !important;
}

/* Remove extra padding where sidebar used to be */
div[data-testid="stAppViewContainer"] {
    margin-left: 0 !important;
}
</style>
""", unsafe_allow_html=True)


# --- SECTION 3: SURVEY ---

# safe defaults if user refreshes this page directly
if "chat_finished" not in st.session_state or not st.session_state["chat_finished"]:
    st.warning("Please complete the chat first.")
    st.switch_page("app.py")
if "responses_submitted" not in st.session_state:
    st.session_state["responses_submitted"] = False
if "experiment_group" not in st.session_state:
    st.warning("Session expired. Please restart the study.")
    st.stop()


st.title("Post-Interaction Survey")
st.write("Thank you for chatting! Please answer the following questions.")
st.divider()

# ---- HARD GUARD (ADD THIS BLOCK HERE) ----
if st.session_state.get("responses_submitted", False):
    st.success("Thank you! Your responses have been recorded.")
    st.stop()
# ------------------------------------------

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
        ### FORM ENDS HERE

if st.session_state['responses_submitted']:
        st.success("Thank you! Your responses have been recorded.")
