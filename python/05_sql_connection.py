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


