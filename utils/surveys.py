
# Surveys Module

DEMOGRAPHICS = [
    {
        "id": "age",
        "question": "What is your age?",
        "type": "number",
        "min_value": 18,
        "max_value": 100
    },
    {
        "id": "gender",
        "question": "What is your gender?",
        "type": "select",
        "options": ["Male", "Female", "Non-binary", "Prefer not to say"]
    },
    {
        "id": "skin_concern_severity",
        "question": "How severe would you rate your primary skin concern?",
        "type": "slider",
        "min": 1,
        "max": 5,
        "labels": ["Not severe at all", "Very severe"]
    },
    {
        "id": "skincare_involvement",
        "question": "How important is skincare to you?",
        "type": "slider",
        "min": 1,
        "max": 5,
        "labels": ["Not important", "Extremely important"]
    },
    {
        "id": "prior_chatbot_usage",
        "question": "How often do you use chatbots?",
        "type": "select",
        "options": ["Never", "Rarely", "Occasionally", "Frequently"]
    },
    {
        "id": "ai_familiarity",
        "question": "How familiar are you with AI technology?",
        "type": "slider",
        "min": 1,
        "max": 5,
        "labels": ["Not familiar", "Very familiar"]
    },
    {
        "id": "online_shopping_freq",
        "question": "How often do you shop for personal care products online?",
        "type": "slider",
        "min": 1,
        "max": 5,
        "labels": ["Never", "Very frequently"]
    }
]

# Experiment 1: Perceived Conversational Flow
FLOW_QUESTIONS = [
    {"id": "flow_smooth", "question": "The conversation felt smooth."},
    {"id": "flow_understood", "question": "The chatbot understood me."},
    {"id": "flow_connected", "question": "The responses were connected to previous turns."},
    {"id": "flow_natural", "question": "The interaction felt natural."},
    {"id": "flow_track", "question": "The chatbot stayed on track."}
]

# Experiment 2: Psychological Ownership
OWNERSHIP_QUESTIONS = [
    {"id": "own_choice", "question": "I felt that the final choice was mine."},
    {"id": "own_decision", "question": "The recommendation reflects my own decision."},
    {"id": "own_control", "question": "I felt in control of the recommendation process."},
    {"id": "own_personal", "question": "I feel a sense of personal ownership over the chosen product."}
]

OUTCOMES = [
    {"id": "purchase_intention", "question": "I would be likely to purchase the recommended product."},
    {"id": "perceived_warmth", "question": "The chatbot felt warm and friendly."},
    {"id": "perceived_intelligence", "question": "The chatbot seemed intelligent."},
    {"id": "satisfaction", "question": "I am satisfied effectively with this engagement."}
]
