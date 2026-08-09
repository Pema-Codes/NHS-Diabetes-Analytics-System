# %%
pip install pyodbc pandas sqlalchemy

# %%
import pandas as pd
from sqlalchemy import create_engine

# --- 1. Connection Parameters ---
SERVER_NAME = "localhost"
DATABASE_NAME = "NHS_PracticeDB"

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
    p.FirstName,
    p.LastName,
    p.Age,
    a.AdmissionID,
    a.AdmissionDate,
    a.DischargeDate,
    a.AdmissionReason,
    DATEDIFF(day, a.AdmissionDate, a.DischargeDate) AS LengthOfStay
FROM Patients p
INNER JOIN Admissions a ON p.PatientID = a.PatientID;
"""

# Load dataset
df_admissions = pd.read_sql(query, con=engine)

# Display initial dataset review
print("\n--- Data Preview ---")
print(df_admissions.head())

print("\n--- Summary Info ---")
print(df_admissions.info())

# %%
import os
os.makedirs('data', exist_ok=True)

# Now save the file
df_admissions.to_csv('data/raw_admissions.csv', index=False)
print(" Saved successfully to data/raw_admissions.csv!")

# %%



