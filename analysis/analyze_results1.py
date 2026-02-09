import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

def analyze_experiment(filepath, experiment_name, iv_column, manipulation_check_cols, outcome_cols):
    print(f"\n{'='*20} Analysis for {experiment_name} {'='*20}\n")
    
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return

    # 1. Descriptive Statistics
    print(f"--- Descriptive Statistics by Condition ({iv_column}) ---")
    desc = df.groupby(iv_column)[outcome_cols].agg(['mean', 'std', 'count']).round(2)
    print(desc)
    print("\n")

    # 2. Manipulation Check (t-test)
    print("--- Manipulation Checks (Independent t-test) ---")
    # Create an aggregate score for manipulation check
    df['manipulation_score'] = df[manipulation_check_cols].mean(axis=1)
    
    groups = df[iv_column].unique()
    group1 = df[df[iv_column] == groups[0]]['manipulation_score']
    group2 = df[df[iv_column] == groups[1]]['manipulation_score']
    
    t_stat, p_val = stats.ttest_ind(group1, group2)
    print(f"Comparing {groups[0]} vs {groups[1]} on Manipulation Score:")
    print(f"t-statistic: {t_stat:.3f}, p-value: {p_val:.3e}")
    if p_val < 0.05:
        print(">> RESULT: Manipulation was SIGNIFICANT.")
    else:
        print(">> RESULT: Manipulation was NOT significant.")
    print("\n")

    # 3. Main Effects on Outcomes (ANOVA)
    print("--- Main Effects on Outcomes (ANOVA) ---")
    
    for outcome in outcome_cols:
        model = ols(f'{outcome} ~ C({iv_column})', data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        print(f"\nOutcome: {outcome}")
        print(anova_table.round(3))
        
        p_val_anova = anova_table['PR(>F)'][0]
        if p_val_anova < 0.05:
            print(f">> SIGNIFICANT effect of {iv_column} on {outcome}.")
        else:
            print(f">> NO significant effect of {iv_column} on {outcome}.")

    # 4. Interaction Effects (with Covariates) - Optional demo
    # Let's see if Skincare Involvement interacts with the Condition
    print("\n--- Interaction Analysis (Condition x Skincare Involvement) ---")
    outcome_target = 'purchase_intention'
    
    formula = f'{outcome_target} ~ C({iv_column}) * skincare_involvement + age + gender'
    model_interaction = ols(formula, data=df).fit()
    print(f"\nOutcome: {outcome_target} (with interactions & controls)")
    print(model_interaction.summary().tables[1]) # Print the coefficients table
    
    print("\n" + "="*60 + "\n")

def main():
    # --- Analyze Flow Experiment ---
    analyze_experiment(
        filepath='experiment_flow_dummy.csv',
        experiment_name='Experiment 1: Perceived Conversational Flow',
        iv_column='condition',
        manipulation_check_cols=['flow_smooth', 'flow_understood', 'flow_connected', 'flow_natural', 'flow_track'],
        outcome_cols=['purchase_intention', 'perceived_warmth', 'perceived_intelligence', 'satisfaction']
    )

    # --- Analyze Ownership Experiment ---
    analyze_experiment(
        filepath='experiment_ownership_dummy.csv',
        experiment_name='Experiment 2: Psychological Ownership',
        iv_column='condition',
        manipulation_check_cols=['own_choice', 'own_decision', 'own_control'],
        outcome_cols=['purchase_intention', 'perceived_warmth', 'perceived_intelligence', 'satisfaction']
    )

if __name__ == "__main__":
    main()
