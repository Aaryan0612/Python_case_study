# 🚗 Vehicle Service Reminder System (v4.0)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> **An intelligent, automated Python system for tracking vehicle maintenance, predicting service schedules, and analyzing maintenance costs through a robust CLI interface.**

---

## 📖 Overview

Vehicle owners often lose track of maintenance schedules, resulting in reduced vehicle lifespan, safety risks, and unexpected expenses.  
The **Vehicle Service Reminder System** eliminates manual tracking by providing a **smart, automated Command Line Interface (CLI)**.

Unlike basic reminder tools, this system uses a **Smart Scheduler** that reasons about:
- missed mileage milestones  
- skipped service history  
- future service predictions  

It is designed to reflect **real-world usage**, not ideal data.

---

## ✨ Key Features

| Feature | Description |
|------|------------|
| 🧠 **Intelligent Scheduling** | Uses a **Triple-Check Algorithm** to classify services as `DUE NOW`, `MISSED`, or `UPCOMING`. |
| 📊 **Visual Analytics** | Generates bar and pie charts for cost breakdown and service frequency using **Matplotlib**. |
| 💾 **Persistent Storage** | All vehicle and service data is stored in CSV files and survives across sessions. |
| 🛡️ **Robust Error Handling** | Handles corrupted files, missing data, and invalid inputs gracefully. |
| 🖥️ **CLI Dashboard** | Displays fleet summary, urgent services, and recent logs in one view. |

---

## 📂 Project Structure

```
Vehicle-Service-System/
│
├── automation.py           # Controller: CLI menu & orchestration
├── vehicle_class.py        # Blueprint: Vehicle object & persistence
├── service_scheduler.py    # Brain: Service prediction logic
├── maintenance_report.py   # Analyst: Graphs & cost reports
│
├── data/
│   ├── vehicles.csv            # Registered vehicles database
│   ├── service_history.csv     # Complete service log
│   └── reminders_log.txt       # Alert and audit log
│
└── README.md               # Project documentation
```

---

## 🔄 System Logic & Architecture

### 1️⃣ High-Level Module Interaction

```mermaid
graph TD
    User((User)) -->|Runs| Automation[automation.py]

    subgraph "Logic and Processing"
        Automation -->|Creates Objects| Vehicle[vehicle_class.py]
        Automation -->|Queries Status| Scheduler[service_scheduler.py]
        Automation -->|Requests Reports| Report[maintenance_report.py]
    end

    subgraph "Data Storage"
        Vehicle -->|Writes| CSV1[(vehicles.csv)]
        CSV1 -->|Reads| Vehicle

        Automation -->|Writes| CSV2[(service_history.csv)]
        CSV2 -->|Reads| Automation

        Automation -->|Appends| Log[(reminders_log.txt)]
    end

    Report -->|Reads Data| CSV2
    Report -->|Generates| Visuals[Matplotlib Graphs]
```

---

### 2️⃣ User Interaction Flow (Detailed Menu Logic)

```mermaid
flowchart TD
    Start([Start automation script]) --> Menu{Main Menu}

    Menu -->|Register Vehicle| Input1[Enter Vehicle Details]
    Input1 --> CreateObj[Create Vehicle Object]
    CreateObj --> SaveVeh[Save to vehicles csv]
    SaveVeh --> Menu

    Menu -->|Check Reminders| ReadVeh[Read vehicles csv]
    ReadVeh --> LoopVeh{For Each Vehicle}
    LoopVeh --> GetHist[Get Service History]
    GetHist --> SchedCalc[Calculate Status]
    SchedCalc --> CheckStatus{Status Type}
    CheckStatus -->|Urgent or Missed| Alert[Print Alert]
    CheckStatus -->|OK| Safe[Print OK]
    Alert --> LogAlert[Save to reminders log]
    LogAlert --> LoopVeh
    Safe --> LoopVeh
    LoopVeh --> Menu

    Menu -->|Log Maintenance| InputReg[Enter Registration Number]
    InputReg --> FindCar{Car Found}
    FindCar -->|No| Error[Print Error]
    Error --> Menu
    FindCar -->|Yes| ShowDue[Show Due Services]
    ShowDue --> AskLog{Log This Service}
    AskLog -->|Yes| InputDetails[Enter Service Details]
    InputDetails --> SaveHist[Append to service history]
    SaveHist --> AskLog
    AskLog -->|No| Skip[Skip Item]
    Skip --> AskLog
    AskLog --> Menu

    Menu -->|View Graphs| InputReg2[Enter Registration Number]
    InputReg2 --> GenReport[Call report module]
    GenReport --> Plot[Generate Charts]
    Plot --> Menu

    Menu -->|View Schedule| InputReg3[Enter Registration Number]
    InputReg3 --> GetFull[Get Full Status]
    GetFull --> PrintTable[Print Schedule Table]
    PrintTable --> Menu

    Menu -->|Dashboard| ReadAll[Read All Data]
    ReadAll --> PrintDash[Print Fleet Summary]
    PrintDash --> Menu

    Menu -->|Exit| End([End Program])
```

---

## 🧠 Module Deep Dive

### Module: service_scheduler.py (The Brain)

```mermaid
flowchart TD
   Start([Start Check]) --> Input[Get Current Mileage and History]
   Input --> LoopService{For Each Service Rule}

   LoopService --> HistoryCheck{History Exists}

   HistoryCheck -->|No| MileageCheck{Current greater than Interval}
   MileageCheck -->|Yes Missed| CalcMissed[Calculate Passed Milestone]
   CalcMissed --> StatusMissed[Status MISSED]

   MileageCheck -->|No| ExactCheck{Current modulo Interval equals zero}
   ExactCheck -->|Yes| StatusDue[Status DUE NOW]
   ExactCheck -->|No| CalcFut[Calculate Future Due Date]
   CalcFut --> StatusOK[Status OK or DUE SOON]

   HistoryCheck -->|Yes| ReadLast[Get Last Mileage and Date]
   ReadLast --> CalcNext[Next Due equals Last plus Interval]
   CalcNext --> TimeCheck{Time Limit Passed}
   TimeCheck -->|Yes| StatusTime[Status OVERDUE by Time]
   TimeCheck -->|No| DistCheck{Next minus Current within Threshold}

   DistCheck -->|Yes| StatusSoon[Status DUE SOON]
   DistCheck -->|No| StatusOK2[Status OK]

   StatusMissed --> Collect[Add to Schedule List]
   StatusDue --> Collect
   StatusOK --> Collect
   StatusTime --> Collect
   StatusSoon --> Collect
   StatusOK2 --> Collect

   Collect --> NextService{More Services}
   NextService -->|Yes| LoopService
   NextService -->|No| Return[Return Full Schedule]
```

---

### Module: maintenance_report.py (The Analyst)

```mermaid
flowchart TD
   Start([Start Report Generation]) --> FileCheck{File Exists}

   FileCheck -->|No| Error1[Print No History Found]
   Error1 --> End([End])

   FileCheck -->|Yes| LoadCSV[Load service history into DataFrame]
   LoadCSV --> ColCheck{Columns Valid}

   ColCheck -->|No| Error2[Print Corrupted File]
   Error2 --> End

   ColCheck -->|Yes| Filter{Registration Number Provided}
   Filter -->|Yes| FilterDF[Filter DataFrame by Registration]
   Filter -->|No| AllData[Use All Data]

   FilterDF --> EmptyCheck{Is DataFrame Empty}
   AllData --> EmptyCheck

   EmptyCheck -->|Yes| Error3[Print No Data for Vehicle]
   Error3 --> End

   EmptyCheck -->|No| Calcs[Calculate Total Cost]
   Calcs --> Group[Group by Service Type]

   Group --> Plot1[Create Bar Chart]
   Group --> Plot2[Create Pie Chart]

   Plot1 --> Show[Display Plots]
   Plot2 --> Show
   Show --> End
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher

```bash
pip install pandas matplotlib
```

### Installation & Run

```bash
git clone https://github.com/Aaryan0612/Python_case_study.git
cd Python_case_study
python automation.py
```

---

## 👨‍💻 Author

**Aaryan Kuchekar**  
B.Tech Computer Science & Engineering (2025–2029)  
ITM Skills University  

📘 Case Study 27 – Python Programming (Semester I)

---

*Built with ❤️ and Python.*
