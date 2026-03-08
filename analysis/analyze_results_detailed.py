# =====================================================
# COMPLETE ANALYSIS SCRIPT
# Conversational Flow & Psychological Ownership Studies
# =====================================================

# =====================================================
##### module installations
# =====================================================

# pip install pandas
# pip install numpy
# pip install scipy
# pip install statsmodels
# pip install matplotlib
# pip install seaborn

##############

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import sys

output_file = open("analysis_results.txt", "w", encoding="utf-8")
sys.stdout = output_file

# =====================================================
# FUNCTIONS
# =====================================================

def cronbach_alpha(df):

    df = df.dropna()

    items = df.values

    item_var = items.var(axis=0, ddof=1)

    total_var = items.sum(axis=1).var(ddof=1)

    n_items = df.shape[1]

    alpha = (n_items/(n_items-1))*(1-item_var.sum()/total_var)

    return alpha


def cohens_d(x,y):

    nx = len(x)

    ny = len(y)

    pooled = np.sqrt(((nx-1)*np.var(x,ddof=1)+(ny-1)*np.var(y,ddof=1))/(nx+ny-2))

    d = (np.mean(x)-np.mean(y))/pooled

    return d


def interpret_ttest(outcome,t,p,d):

    print("\nOutcome:", outcome.replace("_"," "))

    print("t =",round(t,2),"p =",round(p,3),"Cohen's d =",round(d,2))

    if p < .05:

        print(
        "Interpretation: A statistically significant difference exists between the two experimental conditions."
        )

    else:

        print(
        "Interpretation: No statistically significant difference was observed between the experimental conditions."
        )



def regression_analysis(df,outcome):

    model = smf.ols(

        f"{outcome} ~ condition + age + ai_familiarity + skincare_involvement",

        data=df

    ).fit()

    print("\nRegression Model:", outcome)

    print(model.summary())

    print("\nInterpretation:")

    for var,p in model.pvalues.items():

        if var == "Intercept":
            continue

        if p < .05:

            print(var,"significantly predicts", outcome)

        else:

            print(var,"does not significantly predict", outcome)


def moderation(df,outcome,moderator):

    model = smf.ols(
        f"{outcome} ~ condition * {moderator}",
        data=df
    ).fit()

    print("\nModeration Test")
    print("Outcome:", outcome)
    print("Moderator:", moderator)

    # Find interaction term automatically
    interaction_term = None

    for term in model.pvalues.index:
        if "condition" in term and moderator in term:
            interaction_term = term
            break

    if interaction_term is None:
        print("Interaction term not found in model.")
        return

    p = model.pvalues[interaction_term]

    print("Interaction term:", interaction_term)
    print("Interaction p =", round(p,3))

    if p < 0.05:
        print(
        "Interpretation: The moderator significantly changes the effect of the experimental condition on the outcome variable."
        )
    else:
        print(
        "Interpretation: The moderator does not significantly influence the relationship between condition and the outcome variable."
        )



def simple_mediation(df,x,m,y):

    print("\nMediation Model:",x,"→",m,"→",y)

    m_model = smf.ols(f"{m} ~ {x}",data=df).fit()

    y_model = smf.ols(f"{y} ~ {x} + {m}",data=df).fit()

    a = m_model.params[x]

    b = y_model.params[m]

    indirect = a*b

    print("Indirect effect:",round(indirect,3))

    if abs(indirect) > 0:

        print("Interpretation: Evidence suggests a mediating relationship.")

    else:

        print("Interpretation: No mediation effect detected.")



def visualize(df,var,title):

    plt.figure()

    sns.boxplot(x="condition",y=var,data=df)

    plt.title(title)

    plt.show()



# =====================================================
# LOAD DATA
# =====================================================

flow_df = pd.read_excel("experiment_flow_d.xlsx")

own_df = pd.read_excel("experiment_ownership_d.xlsx")


outcomes = [

'purchase_intention',
'perceived_warmth',
'perceived_intelligence',
'satisfaction',
'recommend_intention'

]


moderators = [

'skincare_involvement',
'ai_familiarity',
'skin_concern_severity',
'prior_chatbot_usage'

]


# =====================================================
# STUDY 1: CONVERSATIONAL FLOW
# =====================================================

print("\n==============================")
print("STUDY 1: CONVERSATIONAL FLOW")
print("==============================")

flow_items = [

'flow_smooth',
'flow_understood',
'flow_connected',
'flow_natural',
'flow_track'

]

flow_df['flow_index'] = flow_df[flow_items].mean(axis=1)

alpha = cronbach_alpha(flow_df[flow_items])

print("\nReliability")

print("Cronbach alpha =",round(alpha,2))

print("Interpretation: Values above .70 indicate acceptable internal consistency.")



# Manipulation check

g = flow_df['condition'].unique()

x = flow_df[flow_df.condition==g[0]]['flow_index']

y = flow_df[flow_df.condition==g[1]]['flow_index']

t,p = ttest_ind(x,y,nan_policy='omit')

d = cohens_d(x,y)

print("\nManipulation Check")

interpret_ttest("flow_index",t,p,d)



# Means

print("\nCondition Means")

print(flow_df.groupby("condition")["flow_index"].mean())



# Main effects

print("\nMain Effects")

for o in outcomes:

    x = flow_df[flow_df.condition==g[0]][o]

    y = flow_df[flow_df.condition==g[1]][o]

    t,p = ttest_ind(x,y,nan_policy='omit')

    d = cohens_d(x,y)

    interpret_ttest(o,t,p,d)



# Regression

print("\nRegression Analyses")

for o in outcomes:

    regression_analysis(flow_df,o)



# Moderation

print("\nModeration Analyses")

for m in moderators:

    moderation(flow_df,'purchase_intention',m)



# Mediation

flow_df['condition_binary'] = flow_df['condition'].astype('category').cat.codes

simple_mediation(flow_df,'condition_binary','perceived_warmth','purchase_intention')

simple_mediation(flow_df,'condition_binary','satisfaction','recommend_intention')



# Correlation

print("\nCorrelations")

# print(flow_df[['flow_index']+outcomes].corr())

print(flow_df[['flow_index']+outcomes].corr().to_string())


print("\n==============================")
print("FIGURES TO FOLLOW NEXT")
print("==============================")

# Visualizations

visualize(flow_df,'flow_index',"Flow Manipulation")

for o in outcomes:

    visualize(flow_df,o,f"{o} by Condition")



# =====================================================
# STUDY 2: OWNERSHIP
# =====================================================

print("\n==============================")
print("STUDY 2: PSYCHOLOGICAL OWNERSHIP")
print("==============================")

own_items = [

'own_choice',
'own_decision',
'own_control',
'own_personal',
'own_identity'

]

own_df['ownership_index'] = own_df[own_items].mean(axis=1)

alpha = cronbach_alpha(own_df[own_items])

print("\nReliability")

print("Cronbach alpha =",round(alpha,2))

print("Interpretation: Values above .70 indicate acceptable internal consistency.")



g = own_df['condition'].unique()

x = own_df[own_df.condition==g[0]]['ownership_index']

y = own_df[own_df.condition==g[1]]['ownership_index']

t,p = ttest_ind(x,y,nan_policy='omit')

d = cohens_d(x,y)

print("\nManipulation Check")

interpret_ttest("ownership_index",t,p,d)



print("\nCondition Means")

print(own_df.groupby("condition")["ownership_index"].mean())



print("\nMain Effects")

for o in outcomes:

    x = own_df[own_df.condition==g[0]][o]

    y = own_df[own_df.condition==g[1]][o]

    t,p = ttest_ind(x,y,nan_policy='omit')

    d = cohens_d(x,y)

    interpret_ttest(o,t,p,d)



print("\nRegression Analyses")

for o in outcomes:

    regression_analysis(own_df,o)



print("\nModeration Analyses")

for m in moderators:

    moderation(own_df,'purchase_intention',m)



own_df['condition_binary'] = own_df['condition'].astype('category').cat.codes

simple_mediation(own_df,'condition_binary','satisfaction','purchase_intention')

simple_mediation(own_df,'condition_binary','perceived_warmth','recommend_intention')



print("\nCorrelations")

# print(own_df[['ownership_index']+outcomes].corr())
print(own_df[['ownership_index']+outcomes].corr().to_string())



visualize(own_df,'ownership_index',"Ownership Manipulation")

for o in outcomes:

    visualize(own_df,o,f"{o} by Condition")


print("\n==============================")
print("ANALYSIS COMPLETE")
print("==============================")

print("\n\nAll analyses completed successfully.")
output_file.close()