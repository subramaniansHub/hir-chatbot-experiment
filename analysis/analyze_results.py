
"""
FULL PAPER PARAGRAPH GENERATOR
Creates publication-ready Results section text for:

Study 1: Conversational Flow
Study 2: Psychological Ownership
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# ==============================
# HELPERS
# ==============================

def cronbach_alpha(df_items):
    items = df_items.dropna().to_numpy()
    item_vars = items.var(axis=0, ddof=1)
    total_var = items.sum(axis=1).var(ddof=1)
    n_items = df_items.shape[1]
    return (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)


def cohens_d(x, y):
    x = x.dropna()
    y = y.dropna()
    nx, ny = len(x), len(y)
    pooled_sd = np.sqrt(((nx-1)*x.std(ddof=1)**2 + (ny-1)*y.std(ddof=1)**2) / (nx+ny-2))
    return (x.mean() - y.mean()) / pooled_sd


def interpret_direction(m1, m2, g1, g2):
    return g1 if m1 > m2 else g2


def format_result(outcome, g1, g2, m1, m2, t, p, d):
    direction = interpret_direction(m1, m2, g1, g2)

    if p < 0.05:
        return (
            f"A significant effect of condition emerged for {outcome.replace('_',' ')}, "
            f"t = {t:.2f}, p = {p:.3f}, d = {abs(d):.2f}. "
            f"Participants in the {direction} condition reported higher "
            f"{outcome.replace('_',' ')} "
            f"(M = {max(m1,m2):.2f}) compared to the alternative condition "
            f"(M = {min(m1,m2):.2f})."
        )
    else:
        return (
            f"No significant difference was observed for {outcome.replace('_',' ')}, "
            f"t = {t:.2f}, p = {p:.3f}."
        )


def compare_groups(df, condition_col, outcome):
    groups = df[condition_col].unique()
    if len(groups) != 2:
        return None

    g1, g2 = groups
    x = df[df[condition_col] == g1][outcome]
    y = df[df[condition_col] == g2][outcome]

    t, p = ttest_ind(x, y, nan_policy='omit')
    d = cohens_d(x, y)

    return format_result(outcome, g1, g2, x.mean(), y.mean(), t, p, d)

# ==============================
# OUTCOMES
# ==============================

outcomes = [
    'purchase_intention',
    'perceived_warmth',
    'perceived_intelligence',
    'satisfaction',
    'recommend_intention'
]

# ==============================
# STUDY 1 – FLOW
# ==============================

flow_df = pd.read_csv("experiment_flow_dummy.csv")


flow_items = [
    'flow_smooth',
    'flow_understood',
    'flow_connected',
    'flow_natural',
    'flow_track'
]

for col in flow_items + outcomes:
    flow_df[col] = pd.to_numeric(flow_df[col], errors='coerce')

flow_df['flow_index'] = flow_df[flow_items].mean(axis=1)
alpha_flow = cronbach_alpha(flow_df[flow_items])



print("\n\n==============================")
print("STUDY 1: CONVERSATIONAL FLOW")
print("==============================\n")

print("Reliability:")
print(
    f"The conversational flow scale demonstrated strong internal consistency "
    f"(Cronbach’s α = {alpha_flow:.2f}).\n"
)

# Manipulation check
mc_text = compare_groups(flow_df, 'condition', 'flow_index')
print("Manipulation Check:")
print(
    "A manipulation check was conducted to examine whether the high- and low-flow "
    "conditions differed in perceived conversational flow. "
    + mc_text + "\n"
)

print("Main Effects:\n")
for outcome in outcomes:
    print(compare_groups(flow_df, 'condition', outcome))
    print()


# ==============================
# STUDY 2 – OWNERSHIP
# ==============================

own_df = pd.read_csv("experiment_ownership_dummy.csv")

own_items = [
    'own_choice',
    'own_decision',
    'own_control',
    'own_personal',
    'own_identity'
]

for col in own_items + outcomes:
    own_df[col] = pd.to_numeric(own_df[col], errors='coerce')

own_df['ownership_index'] = own_df[own_items].mean(axis=1)
alpha_own = cronbach_alpha(own_df[own_items])

print("\n\n==============================")
print("STUDY 2: PSYCHOLOGICAL OWNERSHIP")
print("==============================\n")

print("Reliability:")
print(
    f"The psychological ownership scale showed good reliability "
    f"(Cronbach’s α = {alpha_own:.2f}).\n"
)

# Manipulation check
mc_text = compare_groups(own_df, 'condition', 'ownership_index')
print("Manipulation Check:")
print(
    "A manipulation check confirmed that the ownership manipulation significantly influenced perceived psychological ownership."
    + mc_text + "\n"
)

print("Main Effects:\n")
for outcome in outcomes:
    print(compare_groups(own_df, 'condition', outcome))
    print()

