class ScriptManager:
    def __init__(self):
        # Steps define the linear flow of the conversation
        self.steps = [
            "greeting",         # 0
            "ask_name",         # 1 (Text Input)
            "ask_skin_type",    # 2 (MCQ)
            "ask_concern",      # 3 (MCQ)
            "ask_duration",     # 4 (MCQ)
            "ask_routine",      # 5 (MCQ)
            "ask_makeup",       # 6 (New - MCQ)
            "ask_sun",          # 7 (New - MCQ)
            "ask_fragrance",    # 8 (New - MCQ)
            "ask_sensitivity",  # 9 (MCQ)
            "ask_preference",   # 10 (MCQ)
            "recommendation",   # 11
            "closing"           # 12
        ]
        
        # Define Options for MCQ steps
        # If options is None, it implies Text Input
        self.step_options = {
            "greeting": None,
            "ask_name": None,
            "ask_skin_type": ["Oily", "Dry", "Combination", "Normal"],
            "ask_concern": ["Acne / Blemishes", "Anti-aging / Wrinkles", "Hydration / Dryness", "Pigmentation / Spots"],
            "ask_duration": ["Just recently", "Assume 1-2 months", "Over a year", "Always had it"],
            "ask_routine": ["Just water", "Cleanser & Moisturizer", "Full multi-step routine", "Inconsistent"],
            "ask_makeup": ["Daily", "Occasionally", "Rarely / Never", "Only on weekends"],
            "ask_sun": ["High exposure (Outdoors often)", "Moderate exposure", "Low exposure (Mostly indoors)", "I wear sunscreen daily"],
            "ask_fragrance": ["I love scented products", "I prefer light/natural scents", "No fragrance / Unscented", "It doesn't matter"],
            "ask_sensitivity": ["Yes, very sensitive", "Sometimes react", "No, resilient skin", "Unsure"],
            "ask_preference": ["Lightweight Gel", "Rich Cream", "Oil-based", "Milky Lotion"]
        }
        
        # Scripts for each condition
        self.scripts = {
            "greeting": {
                "flow_high": "Hello! I'm **Heera**, your personal skincare assistant. I'm here to help you find the perfect match for your skin. I'm excited to get to know you!",
                "flow_low": "Welcome to Skincare Personal Assistance. I am the automated assistant.",
                "own_high": "Hi! I'm **Heera**. We're going to work together to find the best product for you today.",
                "own_low": "I am the system assistant. I will determine the best product for your skin."
            },
            "ask_name": {
                "flow_high": "To start off, may I know your name so I can address you properly?",
                "flow_low": "State your name.",
                "own_high": "What should I call you as we collaborate on this?",
                "own_low": "Input name:"
            },
            "ask_skin_type": {
                "flow_high": "Lovely to meet you, {name}! Let's dive in. How would you describe your skin type?",
                "flow_low": "Select skin type:",
                "own_high": "{name}, help me understand your skin. Which of these best describes you?",
                "own_low": "Select category:"
            },
            "ask_concern": {
                "flow_high": "Got it. And what is the main skin concern you're hoping to tackle today?",
                "flow_low": "Select primary skin concern:",
                "own_high": "What is the main goal you want us to focus on today?",
                "own_low": "Identify concern:"
            },
            "ask_duration": {
                "flow_high": "I see. How long has this been bothering you? I want to get the full picture.",
                "flow_low": "Duration of symptoms:",
                "own_high": "How long have you been dealing with this? This helps us narrow down the solution.",
                "own_low": "Select duration:"
            },
            "ask_routine": {
                "flow_high": "Thanks for sharing. What does your current skincare routine look like?",
                "flow_low": "Current routine status:",
                "own_high": "What does your current routine look like? We want to find something that fits into what you already do.",
                "own_low": "Select routine complexity:"
            },
            "ask_makeup": {
                "flow_high": "Good to know. How often do you wear makeup? This helps with cleanser recommendations.",
                "flow_low": "Makeup usage frequency:",
                "own_high": "How does makeup fit into your week? We'll factor that in.",
                "own_low": "Select usage frequency:"
            },
            "ask_sun": {
                "flow_high": "And what about user sun exposure? Do you spend a lot of time outdoors?",
                "flow_low": "Sun exposure level:",
                "own_high": "How much sun does your skin get? We should consider protection needs.",
                "own_low": "Select exposure level:"
            },
            "ask_fragrance": {
                "flow_high": "Some people love scents, others don't. What's your preference regarding fragrance in products?",
                "flow_low": "Fragrance preference:",
                "own_high": "Do you have a preference for scents? We want you to enjoy using it.",
                "own_low": "Select option:"
            },
            "ask_sensitivity": {
                "flow_high": "One important question: Do you have any known skin sensitivities or allergies?",
                "flow_low": "Sensitivity status:",
                "own_high": "Do you have any sensitivities we need to avoid in your selection?",
                "own_low": "Select sensitivity:"
            },
            "ask_preference": {
                "flow_high": "Almost done! Do you prefer a specific texture for your products?",
                "flow_low": "Preferred texture:",
                "own_high": "What kind of texture do you personally prefer?",
                "own_low": "Select texture preference:"
            },
            "recommendation": {
                "flow_high": "Based on everything you've told me, {name}, I've found a great match! The **Hydra-Glow Serum** seems perfect for your needs. It targets your concern and fits your routine.",
                "flow_low": "Recommendation: **Hydra-Glow Serum**. Targets primary concern.",
                "own_high": "Based on the preferences you shared, the **Hydra-Glow Serum** matches the profile you built. It aligns with your texture choice and goals. What do you think?",
                "own_low": "The correct choice is the **Hydra-Glow Serum**. Use this product."
            },
            "closing": {
                "flow_high": "I hope that helps! It was wonderful chatting with you, {name}. Good luck with your skincare journey!",
                "flow_low": "Session end.",
                "own_high": "Great choice. I'm glad we could find the right solution for you.",
                "own_low": "End of recommendation."
            }
        }

    def get_message_data(self, step_index, condition, user_name="User"):
        """
        Returns (message_text, options_list)
        """
        if step_index >= len(self.steps):
            return None, None
        
        step_key = self.steps[step_index]
        
        # Map condition keys
        key_map = {
            "High Flow": "flow_high",
            "Low Flow": "flow_low",
            "High Ownership": "own_high",
            "Low Ownership": "own_low"
        }
        
        script_key = key_map.get(condition, "flow_low")
        message = self.scripts[step_key][script_key]
        
        # Formatting
        if "{name}" in message:
            message = message.format(name=user_name)
            
        options = self.step_options.get(step_key)
            
        return message, options

    def get_total_steps(self):
        return len(self.steps)
