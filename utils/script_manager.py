import streamlit as st

class ScriptManager:
    def __init__(self):

        self.steps = [
            "greeting",
            "ask_name",
            "ask_skin_type",
            "ask_concern",
            "ask_duration",
            "ask_routine",
            "ask_makeup",
            "ask_sun",
            "ask_sleep",
            "ask_stress",
            "ask_fragrance",
            "ask_sensitivity",
            "ask_preference",
            "recommendation",
            "closing"
        ]

        self.step_options = {
            "greeting": None,
            "ask_name": None,
            "ask_skin_type": ["Oily", "Dry", "Combination", "Normal"],
            "ask_concern": ["Acne / Blemishes", "Anti-aging / Wrinkles", "Hydration / Dryness", "Pigmentation / Spots"],
            "ask_duration": ["Just recently", "1–2 months", "Over a year", "Always had it"],
            "ask_routine": ["Just water", "Cleanser & Moisturizer", "Full multi-step routine", "Inconsistent"],
            "ask_makeup": ["Daily", "Occasionally", "Rarely / Never", "Weekends only"],
            "ask_sun": ["High exposure", "Moderate exposure", "Low exposure", "Daily sunscreen"],
            "ask_sleep": ["Less than 5 hrs", "5–6 hrs", "7–8 hrs", "More than 8 hrs"],
            "ask_stress": ["Very high", "Moderate", "Low", "Rarely stressed"],
            "ask_fragrance": ["Love scents", "Light scents", "No fragrance", "No preference"],
            "ask_sensitivity": ["Very sensitive", "Sometimes react", "Resilient skin", "Unsure"],
            "ask_preference": ["Lightweight Gel", "Rich Cream", "Oil-based", "Milky Lotion"]
        }

        self.scripts = {

            "greeting": {
                "flow_high": "Hello! I'm Heera, your personal skincare assistant. I'm excited to learn about your skin and guide you step by step.",
                "flow_low": "Welcome. Automated skincare assistant activated.",
                "own_high": "Hi! I'm Heera. We'll build your skincare solution together.",
                "own_low": "System assistant active."
            },

            "ask_name": {
                "flow_high": "Before we begin, may I know your name?",
                "flow_low": "Enter name.",
                "own_high": "What should I call you as we create your skincare plan?",
                "own_low": "Input name:"
            },

            "ask_skin_type": {
                "flow_high": "Lovely to meet you, {name}. How would you describe your skin type?",
                "flow_low": "Select skin type.",
                "own_high": "{name}, which skin type best represents you?",
                "own_low": "Choose category:"
            },

            "ask_concern": {
                "flow_high": "I understand you have {skin_type} skin. What concern would you like to focus on first?",
                "flow_low": "Select concern.",
                "own_high": "You chose {skin_type}. What goal would you like to prioritise?",
                "own_low": "Select concern:"
            },

            "ask_duration": {
                "flow_high": "Since you mentioned {skin_concern}, how long has this been affecting you?",
                "flow_low": "Select duration.",
                "own_high": "How long have you been dealing with {skin_concern}?",
                "own_low": "Select duration:"
            },

            "ask_routine": {
                "flow_high": "That helps. What does your current routine look like for managing {skin_concern}?",
                "flow_low": "Routine status:",
                "own_high": "Tell me about your current routine so we can build around it.",
                "own_low": "Select routine:"
            },

            "ask_makeup": {
                "flow_high": "Thanks. With a routine like '{routine_level}', how often do you wear makeup?",
                "flow_low": "Makeup frequency:",
                "own_high": "How does makeup fit into your routine?",
                "own_low": "Select option:"
            },

            "ask_sun": {
                "flow_high": "Considering your {routine_level} routine and concern about {skin_concern}, how much sun exposure do you usually get?",
                "flow_low": "Sun exposure:",
                "own_high": "How much sun does your skin get daily? We'll factor that into your solution.",
                "own_low": "Select exposure:"
            },

            "ask_sleep": {
                "flow_high": "Sleep also impacts {skin_concern}. How many hours do you typically sleep?",
                "flow_low": "Sleep duration:",
                "own_high": "How is your sleep pattern? This shapes your skin health.",
                "own_low": "Select sleep:"
            },

            "ask_stress": {
                "flow_high": "Stress can influence {skin_concern}, especially for {skin_type} skin. How would you rate your stress level?",
                "flow_low": "Stress level:",
                "own_high": "How stressed do you usually feel? We'll include that in your profile.",
                "own_low": "Select stress:"
            },

            "ask_fragrance": {
                "flow_high": "Some people with {skin_type} skin prefer specific scents. What's your fragrance preference?",
                "flow_low": "Fragrance preference:",
                "own_high": "Do you enjoy scented products or prefer neutral ones?",
                "own_low": "Select option:"
            },

            "ask_sensitivity": {
                "flow_high": "Given your {skin_concern} concern, do you have any sensitivities we should be careful about?",
                "flow_low": "Sensitivity status:",
                "own_high": "Any sensitivities you want us to avoid?",
                "own_low": "Select sensitivity:"
            },

            "ask_preference": {
                "flow_high": "Almost done, {name}. What texture feels best for your skin?",
                "flow_low": "Texture preference:",
                "own_high": "Which texture do you personally prefer using?",
                "own_low": "Select texture:"
            },

            "recommendation": {
                "flow_high": "Based on everything you've shared — your {skin_type} skin, focus on {skin_concern}, and current routine — the Hydra-Glow Serum looks like a great fit for you, {name}.",
                "flow_low": "Recommended: Hydra-Glow Serum.",
                "own_high": "Here's the profile you created, {name}: You chose {skin_type} skin, prioritised {skin_concern}, and described your routine as '{routine_level}'. Based on the choices you made, the Hydra-Glow Serum matches your profile.",
                "own_low": "Use Hydra-Glow Serum."
            },

            "closing": {
                "flow_high": "It was lovely guiding you, {name}. I hope this helps you feel more confident in your skincare journey.",
                "flow_low": "Session complete.",
                "own_high": "Great work building your skincare profile, {name}. I’m glad we created this together.",
                "own_low": "End."
            }
        }

    def get_message_data(
        self,
        step_index,
        condition,
        user_name="User",
        skin_type="",
        skin_concern="",
        routine_level="",
        budget=""
    ):
    
        if step_index >= len(self.steps):
            return None, None
    
        step_key = self.steps[step_index]
    
        key_map = {
            "High Flow": "flow_high",
            "Low Flow": "flow_low",
            "High Ownership": "own_high",
            "Low Ownership": "own_low"
        }
    
        script_key = key_map.get(condition, "flow_low")
        message = self.scripts[step_key][script_key]
    
        # USE VALUES PASSED FROM APP.PY (NOT session_state here)
        context = {
            "name": user_name,
            "skin_type": skin_type,
            "skin_concern": skin_concern,
            "routine_level": routine_level,
            "budget": budget
        }
    
        try:
            message = message.format(**context)
        except:
            pass
    
        options = self.step_options.get(step_key)
        return message, options


    def get_total_steps(self):
        return len(self.steps)





