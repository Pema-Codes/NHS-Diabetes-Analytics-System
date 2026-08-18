# %%
%pip install pyodbc

# %%
import pandas as pd
import pyodbc 

# %%
# 1. Load CSV Data
df = pd.read_csv("C:\\Users\\Pema Sherpa\\Downloads\\diabetes_prediction_dataset.csv\\diabetes_prediction_dataset.csv")

# %%
# 2. Establish Connection to SSMS
conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=localhost;"
    r"DATABASE=Diabetes_AnalyticsDB;"
    r"Trusted_Connection=yes;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# %%
# Fast execution setting for batch operations
cursor.fast_executemany = True

print("Processing and inserting 100,000 patient records...")

# %%
# 3. Batch Insert into Patients & ClinicalMetrics
# We iterate or batch insert to maintain relational integrity
patients_data = list(df[['gender', 'age', 'smoking_history']].itertuples(index=False, name =None))

# %%
# Insert Patients & retrieve generated PatientIDs
cursor.executemany("""
    INSERT INTO Patients (Gender, Age, SmokingHistory)
    VALUES (?, ?, ?)
""", patients_data)

conn.commit()
print("Patients table populated successfully!")

# %%
# 4. Insert into ClinicalMetrics matching PatientIDs (1 to 100000)
# Since PatientID is IDENTITY(1,1), PatientID i corresponds to Row i
clinical_data = []
for i, row in enumerate(df.itertuples(index=False), start=1):
    clinical_data.append((
        i, # PatientID
        int(row.hypertension),
        int(row.heart_disease),
        float(row.bmi),
        float(row.HbA1c_level),
        int(row.blood_glucose_level),
        int(row.diabetes)
    ))

cursor.executemany("""
    INSERT INTO ClinicalMetrics (PatientID, Hypertension, HeartDisease, BMI, HbA1cLevel, BloodGlucoseLevel, Diabetes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", clinical_data)

conn.commit()
print("ClinicalMetrics table populated successfully!")

# %%
cursor.close()
conn.close()
print("Data Import Complete!")


