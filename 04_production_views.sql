USE Diabetes_AnalyticsDB;
GO

-- ===================================================================
-- NHS Production Analytics Views
-- Purpose: Expose reporting-ready views for Power BI / Excel
-- ===================================================================

CREATE OR ALTER VIEW vw_PatientRiskProfiles AS 
SELECT
    p.PatientID,
    p.Gender,
    p.Age,
    p.SmokingHistory,
    c.BMI,
    c.HbA1cLevel,
    c.BloodGlucoseLevel,
    c.Hypertension,
    c.HeartDisease,
    c.Diabetes,
    CASE
        WHEN c.BloodGlucoseLevel >= 200 OR c.HbA1cLevel >= 6.5 THEN 'High Clinical Risk'
        WHEN c.BloodGlucoseLevel BETWEEN 140 AND 199 OR c.HbA1cLevel BETWEEN 5.7 AND 6.4 THEN 'Elevated Risk'
        ELSE 'Normal Risk'
    END AS ClinicalRiskCategory
 FROM Patients p 
 INNER JOIN ClinicalMetrics c ON p.PatientID = c.PatientID;
 GO

 -- 2. Demographic Prevalence Summary View
CREATE OR ALTER VIEW vw_DiabetesPrevalenceSummary AS
SELECT 
    p.Gender,
    p.SmokingHistory,
    COUNT(*) AS TotalPatients,
    SUM(CAST(c.Diabetes AS INT)) AS TotalDiabeticCases,
    CAST(SUM(CAST(c.Diabetes AS FLOAT)) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS PrevalencePct
FROM Patients p
INNER JOIN ClinicalMetrics c ON p.PatientID = c.PatientID
GROUP BY p.Gender, p.SmokingHistory;
GO

SELECT TOP 5 * 
FROM vw_PatientRiskProfiles;

SELECT *
FROM vw_DiabetesPrevalenceSummary
ORDER BY PrevalencePct DESC;