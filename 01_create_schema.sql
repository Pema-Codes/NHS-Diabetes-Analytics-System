USE Diabetes_AnalyticsDB;
GO

-- 1. Create Patients Table (Demographics & History)
CREATE TABLE Patients(
	PatientID INT PRIMARY KEY IDENTITY(1,1),
	Gender VARCHAR(20),
	Age FLOAT,
	SmokingHistory VARCHAR(50)
);
GO

-- 2. Create Clinical Metrics Table (Clinical Observations)
CREATE TABLE ClinicalMetrics(
	MetricID INT PRIMARY KEY IDENTITY(1,1),
	PatientID INT FOREIGN KEY REFERENCES Patients(PatientID),
	Hypertension BIT,
	HeartDisease BIT,
	BMI FLOAT,
	HbA1cLevel FLOAT,
	BloodGlucoseLevel INT,
	Diabetes BIT
);
GO




