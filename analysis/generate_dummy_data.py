import pandas as pd
import numpy as np
import random

def generate_dummy_data(n_per_condition=150):
    """
    Generates dummy data for the Skincare Chatbot Experiment.
    Creates two CSV files: experiment_flow.csv and experiment_ownership.csv.
    """
    
    # --- Shared Control Variables ---
    def get_controls(n):
        return {
            'age': np.random.randint(18, 65, n),
            'gender': np.random.choice(['Male', 'Female', 'Non-binary', 'Prefer not to say'], n, p=[0.3, 0.68, 0.01, 0.01]),
            'skin_concern_severity': np.random.randint(1, 6, n), # 1-5 Likert
            'skincare_involvement': np.random.randint(1, 6, n),
            'prior_chatbot_usage': np.random.choice(['Never', 'Rarely', 'Occasionally', 'Frequently'], n),
            'ai_familiarity': np.random.randint(1, 6, n),
            'online_shopping_freq': np.random.randint(1, 6, n)
        }

    # --- Experiment 1: Perceived Conversational Flow ---
    # Conditions: High Flow vs. Low Flow
    n_flow = n_per_condition * 2
    df_flow = pd.DataFrame(get_controls(n_flow))
    
    # Assign conditions randomly
    conditions = ['High Flow'] * n_per_condition + ['Low Flow'] * n_per_condition
    random.shuffle(conditions)
    df_flow['condition'] = conditions
    
    # Simulate Responses based on Condition (Effect Size)
    # High Flow should score higher on Flow-related questions and Outcomes
    
    def simulate_likert(condition, high_mean, low_mean, sd=0.8):
        if 'High' in condition:
            return np.clip(np.random.normal(high_mean, sd), 1, 5).round().astype(int)
        else:
            return np.clip(np.random.normal(low_mean, sd), 1, 5).round().astype(int)

    # Manipulation Checks (Flow)
    df_flow['flow_smooth'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 4.2, 2.5))
    df_flow['flow_understood'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 4.0, 2.8))
    df_flow['flow_connected'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 4.1, 2.4))
    df_flow['flow_natural'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 3.9, 2.2))
    df_flow['flow_track'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 4.3, 3.0))

    # Outcomes
    df_flow['purchase_intention'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 3.8, 2.5))
    df_flow['perceived_warmth'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 4.0, 2.2))
    df_flow['perceived_intelligence'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 3.9, 3.1))
    df_flow['satisfaction'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 4.1, 2.3))
    df_flow['recommend_intention'] = df_flow['condition'].apply(lambda c: simulate_likert(c, 4.0, 2.6))



    # --- Experiment 2: Psychological Ownership ---
    # Conditions: High Ownership vs. Low Ownership
    n_own = n_per_condition * 2
    df_own = pd.DataFrame(get_controls(n_own))
    
    conditions_own = ['High Ownership'] * n_per_condition + ['Low Ownership'] * n_per_condition
    random.shuffle(conditions_own)
    df_own['condition'] = conditions_own

    # Manipulation Checks (Ownership)
    # Questions: "I felt the choice was mine", "I felt ownership over the decision", etc.
    df_own['own_choice'] = df_own['condition'].apply(lambda c: simulate_likert(c, 4.1, 2.6))
    df_own['own_decision'] = df_own['condition'].apply(lambda c: simulate_likert(c, 4.0, 2.4))
    df_own['own_control'] = df_own['condition'].apply(lambda c: simulate_likert(c, 3.9, 2.5))
    df_own['own_personal'] = df_own['condition'].apply(lambda c: simulate_likert(c, 4.2, 2.7))
    df_own['own_identity'] = df_own['condition'].apply(lambda c: simulate_likert(c, 4.0, 2.6))


    # Outcomes
    df_own['purchase_intention'] = df_own['condition'].apply(lambda c: simulate_likert(c, 3.9, 2.7))
    df_own['perceived_warmth'] = df_own['condition'].apply(lambda c: simulate_likert(c, 3.7, 3.0)) # Maybe less effect on warmth
    df_own['perceived_intelligence'] = df_own['condition'].apply(lambda c: simulate_likert(c, 4.0, 3.5))
    df_own['satisfaction'] = df_own['condition'].apply(lambda c: simulate_likert(c, 4.0, 2.8))
    df_own['recommend_intention'] = df_own['condition'].apply(lambda c: simulate_likert(c, 4.1, 2.9))


    # Save to CSV
    df_flow.to_csv('experiment_flow_dummy.csv', index=False)
    df_own.to_csv('experiment_ownership_dummy.csv', index=False)
    
    print(f"Generated 'experiment_flow_dummy.csv' with {len(df_flow)} records.")
    print(f"Generated 'experiment_ownership_dummy.csv' with {len(df_own)} records.")

if __name__ == "__main__":
    generate_dummy_data()

