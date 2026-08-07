USE Diabetes_AnalyticsDB;
GO

-- ===================================================================
-- NHS Data Quality Audit Script
-- Purpose: Validate data completeness and detect clinical anomalies
-- ===================================================================

-- Audit 1: Missing/Unknown Smoking History (NHS Data Governance Check)
SELECT
	SmokingHistory,
	COUNT(*) AS PatientCount,
	CAST(COUNT(*)* 100.0 / (SELECT COUNT (*) FROM Patients) AS DECIMAL(5,2)) AS Percentage
FROM Patients
GROUP BY SmokingHistory
ORDER BY PatientCount DESC;

-- Audit 2: Clinical Metric Boundaries & Outlier Search
SELECT
	MIN(AGE) AS MinAge, MAX(AGE) AS MaxAge,
	MIN(BMI) AS MinBMI, MAX(BMI) AS MaxBMI,
	MIN(HbA1cLevel) AS MinHbA1c, MAX(HbA1cLevel) AS MaxHba1c,
	MIN(BloodGlucoseLevel) AS MinGlucose, MAX(BloodGlucoseLevel) AS MaxGlucose
FROM Patients p
INNER JOIN ClinicalMetrics c 
	ON p.PatientID = c.PatientID;
GO

-- Audit 3: Age Group Binning & Diabetes Prevalence Rate Audit
SELECT
	CASE	
		WHEN p.Age < 18 THEN 'Pediatric (<18)'
		WHEN p.Age BETWEEN 18 AND 65 THEN 'Adult(18-64)'
		ELSE 'Elderly (65+)'
	END AS AgeGroup,
	COUNT(*) AS TotalPatients,
	SUM(CAST(c.Diabetes AS INT)) AS DiabeticPatients,
	CAST(SUM(CAST(c.Diabetes AS FLOAT)) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS PrevalenceRatepct
FROM Patients p
INNER JOIN ClinicalMetrics c ON p.PatientID = c.PatientID
GROUP BY
	CASE	
		WHEN p.Age < 18 THEN 'Pediatric (<18)'
		WHEN p.Age BETWEEN 18 AND 65 THEN 'Adult(18-64)'
		ELSE 'Elderly (65+)'
	END 
ORDER BY PrevalenceRatepct DESC;
GO