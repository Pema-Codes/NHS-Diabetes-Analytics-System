# %%
pip install pyodbc pandas sqlalchemy

# %%
import pandas as pd
from sqlalchemy import create_engine

# --- 1. Connection Parameters ---
SERVER_NAME = "localhost"
DATABASE_NAME = "Diabetes_AnalyticsDB"

# --- 2. Create Connection Engine (Windows Authentication) ---
# Driver 17 or 18 for SQL Server is standard
connection_url = (
    f"mssql+pyodbc://@{SERVER_NAME}/{DATABASE_NAME}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

try:
    engine = create_engine(connection_url)
    print(" Engine created successfully!")
except Exception as e:
    print(f" Connection failed: {e}")

# %%
# --- 3. Execute Query & Load into Pandas DataFrame ---
query = """
SELECT 
    p.PatientID,
    p.Gender,
    p.Age,
    p.SmokingHistory,
    c.Hypertension,
    c.HeartDisease,
    c.BMI,
    c.HbA1cLevel,
    c.BloodGlucoseLevel,
    c.Diabetes  
FROM dbo.Patients p
INNER JOIN dbo.ClinicalMetrics c 
    ON p.PatientID = c.PatientID;
"""

# Load dataset
df_diabetes = pd.read_sql(query, con=engine)

# Display initial dataset review
print("\n--- Data Preview ---")
print(df_diabetes.head())

print("\n--- Summary Info ---")
print(df_diabetes.info())

# %%
# --- . Descriptive Statistics ---
print("--- Summary Statistics ---")
print(df_diabetes[['Age', 'BMI', 'HbA1cLevel', 'BloodGlucoseLevel']].describe())

# %%
# ---  Correlation Analysis ---
# Target variable is 'Diabetes' (1 = Yes, 0 = No)
numeric_cols = ['Age', 'Hypertension', 'HeartDisease', 'BMI', 'HbA1cLevel', 'BloodGlucoseLevel', 'Diabetes']

print("\n--- Correlation with Diabetes Outcome ---")
correlations = df_diabetes[numeric_cols].corr()['Diabetes'].sort_values(ascending=False)
print(correlations)

# %%
# ---  High-Risk Combination Analysis ---
# Clinical thresholds: HbA1c >= 6.5% (Diabetic threshold) AND BMI >= 30.0 (Obese)
df_diabetes['High_Risk_Combo'] = (df_diabetes['HbA1cLevel'] >= 6.5) & (df_diabetes['BMI'] >= 30.0)

combo_summary = df_diabetes.groupby('High_Risk_Combo')['Diabetes'].agg(
    Total_Patients='count',
    Diabetic_Cases='sum',
    Diabetes_Prevalence='mean'
).reset_index()

print("\n--- Impact of High HbA1c (>= 6.5) + High BMI (>= 30.0) ---")
print(combo_summary)

# %%
import pandas as pd
import numpy as np

# Define a function to calculate risk score per patient
def calculate_diabetes_risk(row):
    score = 0
    
    # 1. HbA1c Points (Weight: 40%)
    if row['HbA1cLevel'] >= 6.5:
        score += 40
    elif row['HbA1cLevel'] >= 5.7:
        score += 20
        
    # 2. Blood Glucose Points (Weight: 30%)
    if row['BloodGlucoseLevel'] >= 126:
        score += 30
    elif row['BloodGlucoseLevel'] >= 100:
        score += 15
        
    # 3. BMI Points (Weight: 20%)
    if row['BMI'] >= 30.0:
        score += 20
    elif row['BMI'] >= 25.0:
        score += 10
        
    # 4. Age & Comorbidities (Weight: 10%)
    if row['Age'] > 50 or row['Hypertension'] == 1 or row['HeartDisease'] == 1:
        score += 10
        
    return score

# Apply the risk score function across all rows
df_diabetes['Risk_Score'] = df_diabetes.apply(calculate_diabetes_risk, axis=1)

# Categorize into Risk Tiers
conditions = [
    (df_diabetes['Risk_Score'] >= 60),
    (df_diabetes['Risk_Score'] >= 30) & (df_diabetes['Risk_Score'] < 60),
    (df_diabetes['Risk_Score'] < 30)
]
choices = ['High Risk', 'Medium Risk', 'Low Risk']

df_diabetes['Risk_Category'] = np.select(conditions, choices, default='Low Risk')

# Review results
print("--- Risk Category Summary ---")
print(df_diabetes['Risk_Category'].value_counts())

print("\n--- Sample Patient Risk Profiles ---")
print(df_diabetes[['PatientID', 'Age', 'BMI', 'HbA1cLevel', 'BloodGlucoseLevel', 'Risk_Score', 'Risk_Category', 'Diabetes']].head(10))


