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
            "ask_sensitivity",
            "ask_fragrance",
            "ask_preference",
            "recommendation",
            "closing"
        ]

        self.step_options = {
            "greeting": None,
            "ask_name": None,
            "ask_skin_type": ["Normal", "Oily", "Dry", "Combination"],
            "ask_concern": ["Acne / Blemishes", "Aging / Wrinkles", "Dryness", "Pigmentation / Spots"],
            "ask_duration": ["Very recently", "About 1–2 months", "Over a year", "Always had it"],
            "ask_routine": ["Just water", "Only Moisturizer", "Cleanser & Moisturizer", "Full multi-step routine"],
            "ask_makeup": ["Daily", "Occasionally", "Weekends only", "Rarely / Never"],
            "ask_sun": ["High exposure", "Moderate exposure", "Low exposure", "Zero exposure"],
            "ask_sleep": ["Less than 5 hrs", "5–6 hrs", "7–8 hrs", "More than 8 hrs"],
            "ask_stress": ["Very high", "Moderate", "Low", "Rarely stressed"],
            "ask_sensitivity": ["Very sensitive", "Sometimes reactive", "Resilient skin", "Unsure"],
            "ask_fragrance": ["Unscented", "Mild scent",  "Bold scent", "No specific preference"],
            "ask_preference": ["Lightweight Gel", "Rich Cream", "Oil-based", "Milky Lotion"]
        }

        self.scripts = {

            "greeting": {
                "flow_high": "Hello! I'm Heera, your personal skincare assistant. I'm excited to understand your skin and guide you step by step.",
                "flow_low": "Welcome. You are chatting with the skincare assistant.",
                "own_high": "Hi! I'm Heera. I am here to help you decide the ideal skincare solution for yourself. Let's build it together with you leading it.",
                "own_low": "You are chatting with the skincare assistant."
            },

            "ask_name": {
                "flow_high": "Before we begin, what should I call you?",
                "flow_low": "Enter your name.",
                "own_high": "What should I call you as we create your skincare plan?",
                "own_low": "Input your name:"
            },

            "ask_skin_type": {
                "flow_high": "Nice to meet you, {name}. How would you describe your skin type?",
                "flow_low": "Select skin type.",
                "own_high": "{name}, which skin type best represents you?",
                "own_low": "Choose skin type:"
            },

            "ask_concern": {
                "flow_high": "Got it - you have {skin_type} skin. What would you like to focus on the most?",
                "flow_low": "Select main concern.",
                "own_high": "You chose {skin_type} skin. What issue would you like to prioritise?",
                "own_low": "Select main concern:"
            },

            "ask_duration": {
                "flow_high": "Thanks for sharing that. How long has {skin_concern} been affecting you?",
                "flow_low": "Duration of the concern:",
                "own_high": "How long have you been dealing with {skin_concern}?",
                "own_low": "Duration of the concern:"
            },

            "ask_routine": {
                "flow_high": "That helps me understand your skin better. What does your current routine look like?",
                "flow_low": "Current skincare routine:",
                "own_high": "You are well aware of your skin!. Tell me about your current routine so we can build around it.",
                "own_low": "Current skincare routine:"
            },

            "ask_makeup": {
                "flow_high": "Since you follow a {routine_level} routine, how often do you wear makeup?",
                "flow_low": "Makeup frequency:",
                "own_high": "How does makeup fit into your lifestyle?",
                "own_low": "Makeup frequency:"
            },

            "ask_sun": {
                "flow_high": "Considering your routine and concern about {skin_concern}, how much sun exposure do you usually get?",
                "flow_low": "Sun exposure:",
                "own_high": "Am pretty sure you'll know how much sun does your skins get on a regular basis. We'll factor that into your solution.",
                "own_low": "Sun exposure:"
            },

            "ask_sleep": {
                "flow_high": "Sleep can impact {skin_concern}. How many hours do you typically sleep?",
                "flow_low": "Sleep duration:",
                "own_high": "As you'd know, sleep can impact your skin health. How is your sleep pattern? ",
                "own_low": "Sleep duration:"
            },

            "ask_stress": {
                "flow_high": "Stress can influence {skin_concern}, especially for {skin_type} skin. How would you rate your stress level?",
                "flow_low": "Stress level:",
                "own_high": "You seem quite aware about yourself. How stressed do you usually feel? We'll include that in your profile.",
                "own_low": "Stress level:"
            },

            "ask_fragrance": {
                "flow_high": "Some people with {skin_type} skin prefer specific scents. What type of fragrance do you prefer?",
                "flow_low": "Fragrance preferred in product:",
                "own_high": "Would you choose a scented product for your skin or prefer neutral ones? Choose an option:",
                "own_low": "Fragrance preferred in product:"
            },

            "ask_sensitivity": {
                "flow_high": "Given your {skin_concern} concern, do you have any sensitivities we should consider?",
                "flow_low": "Sensitivity status:",
                "own_high": "I am sure you'd be well aware of your sensitivities. Any that you want us to avoid?",
                "own_low": "Sensitivity status:"
            },

            "ask_preference": {
                "flow_high": "Almost done, {name}. What texture feels most comfortable for your skin?",
                "flow_low": "Texture preference:",
                "own_high": "You'll surely know the texture you personally prefer. Right?",
                "own_low": "Preferred texture:"
            },

           "recommendation": {
            "flow_high": "Based on everything you've shared — your {skin_type} skin, focus on {skin_concern}, and current routine — the <span style='color:#780741; font-size:20px; font-weight:700;'>Hydra-Glow Satin Serum</span> looks like a great fit for you, {name}.",
            "flow_low": "Recommended product: <span style='color:#780741; font-size:16px; font-weight:700;'>AquaLuxe Ultra Nectar</span>.",
            "own_high": "{name}: You chose {skin_type} skin, prioritised {skin_concern}, and described your routine as '{routine_level}'. Based on the choices you made, the <span style='color:#780741; font-size:20px; font-weight:700;'>GlowMist Silky Essence</span> matches your profile.",
            "own_low": "Recommended product: <span style='color:#780741; font-size:16px; font-weight:700;'>AloeVelvet Lumi Shine</span>."
            },

            "closing": {
                "flow_high": "It was lovely interacting with you, {name}!. I hope this helps you feel better in your skincare journey.",
                "flow_low": "End of chat.",
                "own_high": "{name}, you were well aware about your skin - that certainly helped in arriving at a solution for your skincare profile.",
                "own_low": "End of chat."
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
























