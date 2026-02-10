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
            "ask_time",
            "ask_sleep",
            "ask_stress",
            "ask_fragrance",
            "ask_sensitivity",
            "ask_preference",
            "ask_budget",
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
            "ask_makeup": ["Daily", "Occasionally", "Rarely / Never", "Only on weekends"],
            "ask_sun": ["High exposure", "Moderate exposure", "Low exposure", "I wear sunscreen daily"],
            "ask_time": ["Morning", "Night", "Both", "No fixed time"],
            "ask_sleep": ["Great", "Okay", "Poor", "Irregular"],
            "ask_stress": ["High", "Moderate", "Low", "Prefer not to say"],
            "ask_fragrance": ["Love fragrance", "Light fragrance", "No fragrance", "Doesn't matter"],
            "ask_sensitivity": ["Very sensitive", "Sometimes react", "Resilient", "Unsure"],
            "ask_preference": ["Lightweight Gel", "Rich Cream", "Oil-based", "Milky Lotion"],
            "ask_budget": ["Budget-friendly", "Mid-range", "Premium", "Open"]
        }

        self.scripts = {

            "greeting": {
                "flow_high": "Hello! I'm **Heera**, your personal skincare assistant. I'm excited to learn about your skin and guide you step by step.",
                "flow_low": "Welcome. I am the automated skincare assistant.",
                "own_high": "Hi! I'm **Heera**. We'll build your skincare solution together based on the choices you make.",
                "own_low": "I am the system assistant."
            },

            "ask_name": {
                "flow_high": "To begin, may I know your name so I can speak with you more naturally?",
                "flow_low": "State your name.",
                "own_high": "What should I call you as we work on your skincare plan together?",
                "own_low": "Enter name."
            },

            "ask_skin_type": {
                "flow_high": "Lovely to meet you, {name}! Let's start with your skin. How would you describe your skin type?",
                "flow_low": "Select skin type:",
                "own_high": "{name}, you’ll guide this process. Which skin type best represents you?",
                "own_low": "Select category:"
            },

            "ask_concern": {
                "flow_high": "I understand you have {skin_type} skin. What is the main concern you'd like to focus on first?",
                "flow_low": "Select concern:",
                "own_high": "You identified your skin type as {skin_type}. What goal would you like to work on?",
                "own_low": "Identify concern:"
            },

            "ask_duration": {
                "flow_high": "Since you mentioned {concern}, how long has this been affecting your skin?",
                "flow_low": "Select duration:",
                "own_high": "You chose {concern}. How long have you been dealing with it?",
                "own_low": "Select duration:"
            },

            "ask_routine": {
                "flow_high": "Thanks for sharing that. What does your current skincare routine look like right now?",
                "flow_low": "Select routine:",
                "own_high": "Tell me about your routine — we'll build something that fits what you already do.",
                "own_low": "Select routine:"
            },

            "ask_makeup": {
                "flow_high": "Given your routine of '{routine}', how often do you wear makeup? This helps me understand cleansing needs.",
                "flow_low": "Makeup usage:",
                "own_high": "With your routine in mind, how does makeup fit into your week?",
                "own_low": "Select frequency:"
            },

            "ask_sun": {
                "flow_high": "Since you're focusing on {concern} and follow a '{routine}' routine, how much sun exposure does your skin usually get?",
                "flow_low": "Sun exposure:",
                "own_high": "You mentioned your routine is '{routine}'. How much sun does your skin get daily?",
                "own_low": "Select exposure:"
            },

            "ask_time": {
                "flow_high": "Considering your {sun} exposure, when do you usually prefer doing skincare — morning or night?",
                "flow_low": "Preferred time:",
                "own_high": "When do YOU prefer doing skincare? Morning or night?",
                "own_low": "Select time:"
            },

            "ask_sleep": {
                "flow_high": "Skin repair often happens at night. How has your sleep been lately?",
                "flow_low": "Sleep quality:",
                "own_high": "How would you describe your sleep pattern? This helps tailor your routine.",
                "own_low": "Select sleep:"
            },

            "ask_stress": {
                "flow_high": "Sleep and skin health are closely linked. Would you say stress has been affecting you recently?",
                "flow_low": "Stress level:",
                "own_high": "Do you feel stress is influencing your skin lately?",
                "own_low": "Select stress:"
            },

            "ask_fragrance": {
                "flow_high": "Got it. One more thing — do you enjoy scented products or prefer fragrance-free ones?",
                "flow_low": "Fragrance preference:",
                "own_high": "What scent preference would you like us to follow?",
                "own_low": "Select option:"
            },

            "ask_sensitivity": {
                "flow_high": "Since you mentioned sleep as '{sleep}' and stress as '{stress}', do you also experience skin sensitivity?",
                "flow_low": "Sensitivity:",
                "own_high": "Do you have any sensitivities we should avoid while building your selection?",
                "own_low": "Select sensitivity:"
            },

            "ask_preference": {
                "flow_high": "Almost done! What kind of texture do you enjoy applying on your skin?",
                "flow_low": "Texture preference:",
                "own_high": "Which texture do YOU personally enjoy the most?",
                "own_low": "Select texture:"
            },

            "ask_budget": {
                "flow_high": "Last thing — what budget range feels comfortable for you?",
                "flow_low": "Select budget:",
                "own_high": "What price range would you like us to stay within?",
                "own_low": "Select budget:"
            },

            "recommendation": {
                "flow_high": "Thank you, {name}. Based on your {skin_type} skin, focus on {concern}, and your current routine, I’ve found a great match. The **Hydra-Glow Serum** fits your needs beautifully.",
                
                "flow_low": "Recommendation: Hydra-Glow Serum.",

                "own_high": "Here's what YOU built, {name}: You chose {skin_type} skin, prioritised {concern}, described your routine as '{routine}', and shared your preferences clearly. Based on the profile YOU created, the **Hydra-Glow Serum** matches your choices and goals.",
                
                "own_low": "The correct product is Hydra-Glow Serum."
            },

            "closing": {
                "flow_high": "It was wonderful chatting with you, {name}. I hope this helps your skincare journey!",
                "flow_low": "Session end.",
                "own_high": "Great work shaping your skincare profile. I’m glad we built this together.",
                "own_low": "End."
            }
        }

    def get_message_data(self, step_index, condition, **kwargs):

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

        try:
            message = message.format(**kwargs)
        except:
            pass

        options = self.step_options.get(step_key)
        return message, options

    def get_total_steps(self):
        return len(self.steps)
