import pandas as pd
import os
from datetime import datetime
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def save_to_google_sheets(data_dict, sheet_name):
    scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = st.secrets["gcp_service_account"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, scope
    )

    client = gspread.authorize(creds)

    #sheet = client.open("Hir-chatbot-experiment").worksheet(sheet_name)
    sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1OQZnS1-gCmIgmI4huiQf6wMfwSlbPFLhn0z7E7Omvlo/edit?gid=0#gid=0"
    ).worksheet(sheet_name)

    st.write("Spreadsheet title:", sheet.spreadsheet.title)
    st.write("Worksheet title:", sheet.title)
    st.write("Writing row to:", sheet_name)
    st.write(data_dict)
    
    # Force write to a specific row to test
    # sheet.update('A1', [['WORKING']])
    # sheet.update('A2', [[datetime.now().strftime("%H:%M:%S")]])
    # sheet.update('A3', [[str(data_dict)]])

    # If sheet empty → add header row first
    #if not sheet.get_all_values():
    #    sheet.append_row(list(data_dict.keys()))

    # sheet.append_row(list(data_dict.values()))

    #headers = list(data_dict.keys())
    #row = [data_dict[h] for h in headers]
    #sheet.append_row(row)

    # REMOVE header logic completely for testing
    row = [str(v) for v in data_dict.values()]
    sheet.append_row(row)
    
    st.write("APPEND EXECUTED")


def save_response(experiment_name, condition, data_dict):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add metadata (same as CSV version)
    data_dict['timestamp'] = timestamp
    data_dict['condition'] = condition
    data_dict['experiment'] = experiment_name

    # Decide sheet
    if "Flow" in experiment_name:
        sheet_name = "FlowData"
    else:
        sheet_name = "OwnershipData"

    # Send to Google Sheets
    save_to_google_sheets(data_dict, sheet_name)


def save_response2():
    responses = st.session_state.get("responses", {})

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    condition = st.session_state.get("full_condition")
    experiment_group = st.session_state.get("experiment_group")

    # Base demographic + profile data
    data = {
        "age": responses.get("age"),
        "gender": responses.get("gender"),
        "skin_concern_severity": responses.get("skin_concern_severity"),
        "skincare_involvement": responses.get("skincare_involvement"),
        "prior_chatbot_usage": responses.get("prior_chatbot_usage"),
        "ai_familiarity": responses.get("ai_familiarity"),
        "online_shopping_freq": responses.get("online_shopping_freq"),
    }

    # Add condition-specific measures
    if experiment_group == "Flow":
        data.update({
            "flow_smooth": responses.get("flow_smooth"),
            "flow_understood": responses.get("flow_understood"),
            "flow_connected": responses.get("flow_connected"),
            "flow_natural": responses.get("flow_natural"),
            "flow_track": responses.get("flow_track"),
        })
        sheet_name = "FlowData"
        experiment_label = "Experiment Flow"

    else:
        data.update({
            "own_choice": responses.get("own_choice"),
            "own_decision": responses.get("own_decision"),
            "own_control": responses.get("own_control"),
        })
        sheet_name = "OwnershipData"
        experiment_label = "Experiment Ownership"

    # Common outcome variables
    data.update({
        "purchase_intention": responses.get("purchase_intention"),
        "perceived_warmth": responses.get("perceived_warmth"),
        "perceived_intelligence": responses.get("perceived_intelligence"),
        "satisfaction": responses.get("satisfaction"),
        "timestamp": timestamp,
        "condition": condition,
        "experiment": experiment_label
    })

    # Send to Google Sheets
    save_to_google_sheets(data, sheet_name)


def save_response1(experiment_name, condition, data_dict):
    """
    Appends a single response to the appropriate CSV file.
    """
    # Determine file name based on experiment
    if "Flow" in experiment_name:
        filename = "experiment_flow.csv"
    else:
        filename = "experiment_ownership.csv"
        
    filepath = os.path.join(os.getcwd(), filename)
    
    # Add metadata
    data_dict['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict['condition'] = condition
    data_dict['experiment'] = experiment_name
    
    df = pd.DataFrame([data_dict])
    
    if not os.path.exists(filepath):
        df.to_csv(filepath, index=False)
    else:
        df.to_csv(filepath, mode='a', header=False, index=False)
    
    return filename













