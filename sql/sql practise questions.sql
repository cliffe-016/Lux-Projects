-- Clean up existing tables

DROP TABLE IF EXISTS billing CASCADE;
DROP TABLE IF EXISTS admission CASCADE;
DROP TABLE IF EXISTS appointment CASCADE;
DROP TABLE IF EXISTS date CASCADE;
DROP TABLE IF EXISTS doctor CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS patient CASCADE;

-- CASCADE allows SQL to automatically remove or update all dependent objects 
-- (such as foreign key relationships) when a table or record is dropped or deleted, 
--instead of blocking the operation to protect data integrity.

-- CREATE PATIENT DIMENSION TABLE

CREATE TABLE patient (
    patient_key SERIAL PRIMARY KEY,
    patient_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    date_of_birth DATE,
    age INT,
    city VARCHAR(50),
    registration_date DATE
);

-- INSERT PATIENT DATA

INSERT INTO patient (patient_id, first_name, last_name, gender, date_of_birth, age, city, registration_date) VALUES
('P001','Brian','Kamau','Male','1995-06-10',30,'Nairobi','2025-01-05'),
('P002','Faith','Achieng','Female','2001-03-18',24,'Kisumu','2025-01-10'),
('P003','Kevin','Mutua','Male','1988-11-25',36,'Machakos','2025-01-15'),
('P004','Mercy','Wanjiku','Female','1992-07-14',32,'Nakuru','2025-01-18'),
('P005','John','Otieno','Male','1985-01-30',40,'Mombasa','2025-02-01'),
('P006','Susan','Naliaka','Female','1998-09-09',26,'Eldoret','2025-02-05'),
('P007','Peter','Mwangi','Male','1979-12-12',45,'Nairobi','2025-02-10'),
('P008','Alice','Chebet','Female','2003-05-22',21,'Kericho','2025-02-12'),
('P009','Daniel','Omondi','Male','1990-08-17',34,'Kisumu','2025-02-20'),
('P010','Janet','Muthoni','Female','1987-04-03',37,'Thika','2025-03-01');



-- CREATE DEPARTMENT TABLE

CREATE TABLE department (
    department_key SERIAL PRIMARY KEY,
    department_id VARCHAR(20) UNIQUE NOT NULL,
    department_name VARCHAR(100)
);

-- INSERT DEPARTMENT DATA

INSERT INTO department (department_id, department_name) VALUES
('D001','Cardiology'),
('D002','Pediatrics'),
('D003','Orthopedics'),
('D004','Radiology'),
('D005','General Medicine'),
('D006','Gynecology');



-- CREATE DOCTOR TABLE

CREATE TABLE doctor (
    doctor_key SERIAL PRIMARY KEY,
    doctor_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    specialization VARCHAR(100),
    department_key INT REFERENCES department(department_key),
    hire_date DATE
);

-- INSERT DOCTOR DATA

INSERT INTO doctor (doctor_id, first_name, last_name, specialization, department_key, hire_date) VALUES
('DR001','James','Mwangi','Cardiologist',1,'2023-01-15'),
('DR002','Mercy','Atieno','Pediatrician',2,'2022-07-11'),
('DR003','David','Otieno','Orthopedic Surgeon',3,'2021-05-20'),
('DR004','Ann','Wanjiku','General Physician',5,'2024-02-10'),
('DR005','Samuel','Kiptoo','Radiologist',4,'2020-10-05'),
('DR006','Grace','Njeri','Gynecologist',6,'2023-06-18'),
('DR007','Paul','Ochieng','General Physician',5,'2022-09-12'),
('DR008','Lydia','Chepkemoi','Pediatrician',2,'2021-11-01');


select * from doctor;
-- CREATE DATE DIMENSION TABLE

CREATE TABLE date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_number INT,
    day_name VARCHAR(20),
    week_number INT,
    month_number INT,
    month_name VARCHAR(20),
    quarter_number INT,
    year_number INT
);

-- INSERT DATE DATA

INSERT INTO date VALUES
(20250210,'2025-02-10',10,'Monday',7,2,'February',1,2025),
(20250211,'2025-02-11',11,'Tuesday',7,2,'February',1,2025),
(20250212,'2025-02-12',12,'Wednesday',7,2,'February',1,2025),
(20250301,'2025-03-01',1,'Saturday',9,3,'March',1,2025),
(20250303,'2025-03-03',3,'Monday',10,3,'March',1,2025),
(20250305,'2025-03-05',5,'Wednesday',10,3,'March',1,2025),
(20250308,'2025-03-08',8,'Saturday',10,3,'March',1,2025),
(20250310,'2025-03-10',10,'Monday',11,3,'March',1,2025),
(20250312,'2025-03-12',12,'Wednesday',11,3,'March',1,2025),
(20250315,'2025-03-15',15,'Saturday',11,3,'March',1,2025),
(20250318,'2025-03-18',18,'Tuesday',12,3,'March',1,2025);



-- CREATE APPOINTMENT FACT TABLE

CREATE TABLE appointment (
    appointment_key SERIAL PRIMARY KEY,
    appointment_id VARCHAR(20),
    patient_key INT REFERENCES patient(patient_key),
    doctor_key INT REFERENCES doctor(doctor_key),
    department_key INT REFERENCES department(department_key),
    appointment_date_key INT REFERENCES date(date_key),
    appointment_date DATE,
    appointment_time TIME,
    appointment_status VARCHAR(20),
    diagnosis VARCHAR(150),
    consultation_fee NUMERIC(10,2)
);

select * from patient;
-- INSERT APPOINTMENT DATA

INSERT INTO appointment VALUES
(DEFAULT,'A001',1,1,1,20250210,'2025-02-10','09:00','Completed','Hypertension',2500),
(DEFAULT,'A002',2,2,2,20250211,'2025-02-11','10:30','Completed','Malaria',1800),
(DEFAULT,'A003',3,4,5,20250212,'2025-02-12','14:00','Cancelled','General Checkup',1500),
(DEFAULT,'A004',1,4,5,20250301,'2025-03-01','11:00','Completed','Flu',1200),
(DEFAULT,'A005',4,6,6,20250303,'2025-03-03','08:30','Completed','Routine Review',2200),
(DEFAULT,'A006',5,3,3,20250305,'2025-03-05','13:15','Completed','Fracture',3000),
(DEFAULT,'A007',6,5,4,20250305,'2025-03-05','15:45','Completed','X-Ray Request',2000),
(DEFAULT,'A008',7,1,1,20250308,'2025-03-08','09:20','No-show','Chest Pain',2500),
(DEFAULT,'A009',8,8,2,20250310,'2025-03-10','10:10','Completed','Fever',1700),
(DEFAULT,'A010',9,7,5,20250312,'2025-03-12','12:40','Completed','Diabetes Review',2100);



-- CREATE BILLING FACT TABLE

CREATE TABLE billing (
    billing_key SERIAL PRIMARY KEY,
    bill_id VARCHAR(20),
    patient_key INT REFERENCES patient(patient_key),
    doctor_key INT REFERENCES doctor(doctor_key),
    department_key INT REFERENCES department(department_key),
    bill_date_key INT REFERENCES date(date_key),
    bill_date DATE,
    service_type VARCHAR(50),
    bill_status VARCHAR(20),
    total_amount NUMERIC(10,2),
    paid_amount NUMERIC(10,2),
    balance_amount NUMERIC(10,2),
    payment_method VARCHAR(30)
);

-- INSERT BILLING DATA

INSERT into billing VALUES
(DEFAULT,'B001',1,1,1,20250210,'2025-02-10','Consultation','Paid',4000,4000,0,'Cash'),
(DEFAULT,'B002',2,2,2,20250211,'2025-02-11','Consultation','Partial',3000,1500,1500,'Mobile Money'),
(DEFAULT,'B003',3,4,5,20250212,'2025-02-12','Consultation','Unpaid',1500,0,1500,'Cash'),
(DEFAULT,'B004',1,4,5,20250301,'2025-03-01','Consultation','Paid',1200,1200,0,'Card'),
(DEFAULT,'B005',4,6,6,20250303,'2025-03-03','Procedure','Paid',5000,5000,0,'Insurance'),
(DEFAULT,'B006',5,3,3,20250305,'2025-03-05','Procedure','Partial',8000,5000,3000,'Card'),
(DEFAULT,'B007',6,5,4,20250305,'2025-03-05','Lab','Paid',2500,2500,0,'Mobile Money'),
(DEFAULT,'B008',7,1,1,20250308,'2025-03-08','Consultation','Unpaid',2500,0,2500,'Cash'),
(DEFAULT,'B009',8,8,2,20250310,'2025-03-10','Consultation','Paid',1700,1700,0,'Cash'),
(DEFAULT,'B010',9,7,5,20250312,'2025-03-12','Consultation','Partial',4200,2000,2200,'Insurance');



-- CREATE ADMISSION FACT TABLE

CREATE TABLE admission (
    admission_key SERIAL PRIMARY KEY,
    admission_id VARCHAR(20),
    patient_key INT REFERENCES patient(patient_key),
    doctor_key INT REFERENCES doctor(doctor_key),
    department_key INT REFERENCES department(department_key),
    admission_date DATE,
    discharge_date DATE,
    ward_name VARCHAR(50),
    bed_number VARCHAR(20),
    admission_reason VARCHAR(150),
    discharge_status VARCHAR(30),
    length_of_stay INT,
    admission_cost NUMERIC(10,2)
);

-- INSERT ADMISSION DATA

INSERT INTO admission VALUES
(DEFAULT,'AD001',1,1,1,'2025-02-10','2025-02-14','Cardiac Ward','B01','Hypertension Monitoring','Discharged',4,18000),
(DEFAULT,'AD002',5,3,3,'2025-03-05','2025-03-10','Ortho Ward','B12','Fracture Management','Discharged',5,25000),
(DEFAULT,'AD003',10,6,6,'2025-03-12','2025-03-18','Maternity Ward','M03','Observation','Discharged',6,22000),
(DEFAULT,'AD004',7,1,1,'2025-03-08',NULL,'Cardiac Ward','B05','Chest Pain Observation','Ongoing',NULL,12000),
(DEFAULT,'AD005',9,7,5,'2025-03-10','2025-03-15','General Ward','G07','Diabetes Monitoring','Discharged',5,16000);

SELECT * FROM patient;

SELECT * FROM department;

SELECT * FROM doctor;

SELECT * FROM date;

SELECT * FROM appointment;

SELECT * FROM billing;

-- AGGREGATE FUNCTIONS

-- Q1 Determine the total number of patients registered in the hospital.
SELECT count(*) FROM patient;
-- Q2 Find the average age of patients in the system.
SELECT avg(age) FROM patient;
-- Q3 Calculate the total revenue generated from all hospital bills.
SELECT sum(total_amount) FROM billing;
-- Q4 Identify the highest single bill recorded in the hospital.
SELECT total_amount FROM billing ORDER BY total_amount DESC LIMIT 1;
-- Q5 Determine the total amount of money that has been paid by patients so far.
SELECT sum(paid_amount) FROM billing;
-- Q6 Calculate the total outstanding balance across all bills.
SELECT sum(balance_amount) FROM billing;
-- Q7 Find the average consultation fee charged during appointments.
SELECT avg(consultation_fee) FROM appointment;
-- Q8 Determine how many admissions have been recorded in the hospital.
SELECT count(*) FROM admission;

-- GROUP BY

-- Q9 Determine how many patients come from each city.
SELECT city, count(*) FROM patient GROUP BY city;
-- Q10 Find how many doctors work in each department.
SELECT e.department_name, count(DISTINCT d.doctor_key) 
FROM department e
	JOIN doctor d
		ON e.department_key = d.department_key
GROUP BY e.department_name;

-- Q11 Calculate the total number of appointments handled by each doctor.
SELECT concat(d.first_name, ' ', d.last_name) AS doctor_name, count(DISTINCT a.appointment_key) AS no_appointments
FROM doctor d
	JOIN appointment a
		ON d.doctor_key = a.doctor_key
GROUP BY d.doctor_key;		
-- Q12 Determine the number of appointments handled by each department.
SELECT d.department_name, count(DISTINCT a.appointment_key) AS no_appointments
FROM department d
	JOIN appointment a
		ON d.department_key = a.department_key
GROUP BY d.department_name;	
-- Q13 Calculate the total revenue generated by each department.
SELECT d.department_name, sum(b.total_amount)
FROM department d
	JOIN billing b
		ON d.department_key = a.department_key
GROUP BY d.department_name;
-- Q14 Determine the number of bills recorded under each billing status.
SELECT bill_status, count(DISTINCT bill_id) FROM billing group BY bill_status;
-- Q15 Find the total admission cost generated by each department.
SELECT d.department_name, sum(a.admission_cost )
FROM department d
	JOIN admission a
		ON d.department_key = a.department_key
GROUP BY d.department_name;


-- HAVING

-- Q16 Identify departments that have handled more than two appointments.
SELECT d.department_name, count(a.appointment_key)
FROM department d
	JOIN appointment a
		ON d.department_key = a.department_key
GROUP BY d.department_name
HAVING count(a.appointment_key) > 2;
-- Q17 Find doctors who have attended at least two patients.
SELECT concat(d.first_name, ' ', d.last_name) AS doctor_name, count(DISTINCT b.patient_key) AS no_patients
FROM doctor d
	JOIN billing b
		ON d.doctor_key = b.doctor_key
GROUP BY d.doctor_key
HAVING count(DISTINCT b.patient_key) >= 2;	 
-- Q18 Determine which cities have more than one registered patient.
SELECT city, count(*) FROM patient GROUP BY city HAVING count(*) > 1;
-- Q19 Identify departments whose total billing amount exceeds 5,000.
SELECT d.department_name, sum(b.total_amount)
FROM department d
	JOIN billing b
		ON d.department_key = b.department_key
GROUP BY d.department_name
HAVING sum(b.total_amount) > 5000;
-- Q20 Find doctors whose patients have generated more than 4,000 in billing.
SELECT concat(d.first_name, ' ', d.last_name) AS doctor_name, sum(b.total_amount) 
FROM doctor d
	JOIN billing b
		ON d.doctor_key = b.doctor_key
GROUP BY d.doctor_key
HAVING sum(b.total_amount) > 4000;

-- INNER JOINS

-- Q21 Produce a list showing each appointment along with the patient’s full name.
SELECT a.appointment_id, concat(p.first_name, ' ', p.last_name) AS patient_name
FROM appointment a
	JOIN patient p
		ON a.patient_key = p.patient_key;

-- Q22 Show the doctor responsible for each appointment together with the diagnosis.
SELECT concat(d.first_name, ' ', d.last_name) AS doctor_name, a.appointment_id, a.diagnosis 
FROM appointment a
	JOIN doctor d
		ON a.doctor_key = d.doctor_key;

-- Q23 Display the department name for each doctor.
SELECT e.department_name, concat(d.first_name, ' ', d.last_name) AS doctor_name 
FROM department e
	JOIN billing b
		ON b.department_key = e.department_key 
			JOIN doctor d
				ON b.doctor_key = d.doctor_key;

-- Q24 Produce a list showing patient names, their doctors, and the department visited during appointments.
SELECT concat(p.first_name, ' ', p.last_name) AS patient, concat(d.first_name, ' ', d.last_name) AS doctor, e.department_name
FROM department e
	JOIN billing b
		ON b.department_key = e.department_key 
			JOIN doctor d
				ON b.doctor_key = d.doctor_key
					JOIN patient p
						ON b.patient_key = p.patient_key ;
-- Q25 Show the bill details together with the patient names responsible for each bill.
SELECT b.*, concat(p.first_name, ' ', p.last_name) AS patient
FROM billing b
	JOIN patient p
		ON b.patient_key = p.patient_key;
-- Q26 Display the doctor who handled each billed service together with the total amount.
SELECT concat(d.first_name, ' ', d.last_name) AS patient, b.total_amount
FROM billing b
	JOIN doctor d
		ON b.doctor_key = d.doctor_key;


-- LEFT JOINS

-- Q27 Produce a list of all patients and indicate whether they have had an appointment.

-- Q28 Display all doctors and show the appointments they have handled, including those with none.
-- Q29 Show every department and any appointments associated with them.
-- Q30 Display all patients and their billing information, including patients who have never been billed.


-- CASE

-- Q31 Categorize bills into payment groups such as fully paid, partially paid, or unpaid.
-- Q32 Create a category showing whether a patient is considered young, middle-aged, or senior based on age.
-- Q33 Classify admissions into short stay or long stay depending on the length of stay.
-- Q34 Create a category that flags appointments as successful or unsuccessful based on their status.


-- ALIASES AND CALCULATED COLUMNS

-- Q35 Display patient names as a single column combining first and last name.
-- Q36 Create a column showing the total bill amount still owed for each billing record.
-- Q37 Calculate the percentage of each bill that has been paid.
-- Q38 Display the length of stay for each admission calculated from the admission and discharge dates.


-- SUBQUERIES

-- Q39 Find patients who are older than the average age of all patients.
-- Q40 Identify the doctor who handled the highest number of appointments.
-- Q41 Find the patient responsible for the highest bill in the system.
-- Q42 Identify patients who have at least one admission recorded.
-- Q43 Determine departments whose billing totals are above the hospital average.


-- CTES

-- Q44 Calculate total billing per department and determine which department generates the most revenue.
-- Q45 Calculate total appointments handled by each doctor and determine the top three doctors.
-- Q46 Compute the total payments received from each patient and list them in descending order.


-- WINDOW FUNCTIONS

-- Q47 Rank all doctors based on the number of appointments they have handled.
-- Q48 Rank departments based on the revenue they have generated.
-- Q49 Assign a rank to patients based on the total billing amount associated with them.
-- Q50 Determine how each bill compares to the average bill amount.
-- Q51 Display a running total of revenue collected over time based on bill dates.


-- STORED PROCEDURES OR FUNCTIONS

-- Q52 Create a routine that returns all billing records for a specific patient.
-- Q53 Build a routine that calculates the total revenue generated by a given department.
-- Q54 Create a routine that lists all appointments handled by a specific doctor.
-- Q55 Develop a routine that returns all unpaid bills in the hospital.
-- Q56 Create a routine that returns the top performing doctors based on number of appointments.


-- ADVANCED MULTI-CONCEPT QUESTIONS

-- Q57 Determine the total billing amount generated by each department and return the departments from highest to lowest revenue.
-- Which Department Generated the third highest income? and how much was it?
-- Q58 Find the total number of appointments handled by each doctor together with the department each doctor belongs to.
-- Q59 Identify patients whose total billing amount is greater than the overall average billing amount across all patients.
-- Q60 Find doctors whose total number of appointments is higher than the average number of appointments handled by all doctors.
-- Q61 Calculate the total billing amount for each patient and rank patients from highest to lowest total billing.
-- Q62 Compute total revenue for each department and assign a dense rank from the highest earning department to the lowest.
-- Q63 Calculate the total number of appointments handled by each doctor and return the top three doctors based on workload.
-- Q64 Determine the total billing amount generated by each doctor, show the doctor's full name and department name, and rank doctors from highest to lowest revenue.
-- Q65 Calculate the total billing amount for each patient, include the patient's city, and rank patients within each city from highest spender to lowest.
-- Q66 Determine the total appointments handled by each doctor, include the department name, and identify the top doctor in each department.
-- Q67 Calculate the total revenue generated by each department and show the difference between each department’s revenue and the highest department revenue.
-- Q68 Calculate the total billing amount for each patient, include patient and doctor details, and rank patients by total billing within each doctor’s patient list.
-- Q69 For each patient, compare their total billing amount to the hospital-wide average patient billing amount and label them as Above Average or Below Average.
-- Q70 For each doctor, compare their total appointment count to the overall average appointment count and classify them as High Workload or Low Workload.
-- Q71 Display each bill together with the patient name and department name and assign a rank to the bills from the highest amount to the lowest amount.
