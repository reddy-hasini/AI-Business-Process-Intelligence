# AI Business Process Intelligence

A project for analyzing Procure-to-Pay (P2P) procurement data and finding delays, bottlenecks, process deviations, and high-risk cases.

The project uses Python for data processing and analysis, machine learning for delay prediction, a recommendation system for suggesting actions, and Power BI for the final dashboard.

---

## About the Project

Procurement involves several steps such as purchase orders, goods receipts, invoices, and payments. If one of these steps takes longer than expected, it can affect the overall procurement process.

The main idea of this project was to take procurement event data and answer questions like:

* Where are delays happening?
* Which parts of the process are taking more time?
* Which procurement cases are likely to be delayed?
* Which cases have higher risk?
* What action can be recommended for those cases?
* How can the final results be presented in a simple business dashboard?

The project was developed in multiple stages, starting from raw event data and ending with a Power BI dashboard.

---

## Main Objectives

* Extract and understand the procurement event data.
* Clean and prepare the data for analysis.
* Build a structured procurement event log.
* Analyze the procurement process and identify bottlenecks.
* Identify process deviations.
* Create a target for procurement delay prediction.
* Train and validate machine learning models.
* Generate delay predictions for procurement cases.
* Assign risk and priority levels.
* Generate recommendations based on the analysis.
* Create a Power BI dashboard using the final results.

---

## Project Workflow


Raw Procurement Data
        ↓
Data Extraction
        ↓
Data Cleaning & Preparation
        ↓
Process Analysis
        ↓
Delay Prediction
        ↓
Recommendation Generation
        ↓
Validation
        ↓
Power BI Dashboard


---

# Project Stages

## Stage 1 — Data Extraction

The first stage focused on understanding the raw procurement dataset and extracting the information required for further analysis.

The work included:

* Inspecting the original dataset
* Understanding the available events and objects
* Validating the input data
* Extracting procurement-related information
* Discovering the structure of the process

The raw dataset used in the project is stored under:

data/raw/


---

## Stage 2 — Data Cleaning and Preparation

After understanding the raw data, the next step was to convert it into datasets that could be used for process analysis and machine learning.

This stage included:

* Creating the event log
* Connecting related transactions
* Building case relationships
* Calculating process times
* Preparing procurement timing features
* Creating structured datasets for later stages

The processed files are available under:

data/processed/

---

## Stage 3 — Procurement Process Analysis

This stage focuses on understanding how the procurement process behaves.

The analysis includes:

### Process Performance

The process timing of procurement cases was analyzed to understand how long different activities take.

### Bottleneck Detection

The project identifies activities or parts of the procurement process that are associated with higher delays or longer processing times.

### Deviation Analysis

Procurement cases were checked for patterns that differ from the expected process flow.

### Process Flow

The event data was also used to understand how procurement cases move through different activities.

The scripts for this stage are located in:

src/process_analysis/

---

## Stage 4 — Delay Prediction

The next stage uses machine learning to predict whether a procurement case is likely to be delayed.

The workflow was:

Procurement Data
       ↓
Create Delay Target
       ↓
Prepare Features
       ↓
Train Model
       ↓
Validate Model
       ↓
Generate Predictions

The stage includes:

* Delay target creation
* Feature preparation
* Baseline model
* Model validation
* Random Forest analysis
* Final prediction pipeline

The prediction scripts are located in:

src/prediction/


The final prediction data is stored in:

data/processed/


---

## Stage 5 — Recommendation System

After generating the delay predictions, the project uses the available procurement information to generate recommendations.

The recommendation stage considers factors such as:

* Predicted delay
* Risk level
* Priority
* Procurement process conditions
* Identified bottlenecks

The recommendations are then validated to check whether the assigned priorities are consistent with the corresponding risk levels.

The recommendation scripts are located in:

src/recommendations/


---

## Stage 6 — Final Analysis and Power BI Dashboard

The final stage combines the results from the previous stages and prepares them for business reporting.

The Power BI dashboard contains:

* Total Procurement Cases
* Recommendation Coverage
* Predicted Delayed Cases
* Predicted Delay Rate
* High-Risk Cases
* Risk Level Distribution
* Delay Prediction Distribution
* Priority Distribution
* Main Procurement Bottlenecks
* Recommended Actions

The Power BI file is:

AI_Business_Process_Intelligence_Dashboard.pbix


---

# Dashboard Results

The current dashboard contains 174 procurement cases.

| KPI                     | Result |
| ----------------------- | -----: |
| Total Procurement Cases |    174 |
| Recommendation Coverage |   100% |
| Predicted Delayed Cases |     49 |
| Predicted Delay Rate    | 28.16% |
| High-Risk Cases         |     36 |

The dashboard provides a single view of the prediction results, procurement risk, bottlenecks, priorities, and recommendations.

---

# Machine Learning

The project includes both baseline and Random Forest analysis as part of the delay prediction stage.

The final prediction pipeline produces:

* Predicted delay class
* Delay probability
* Risk level
* Priority information

These results are later used by the recommendation stage and Power BI dashboard.

---

# Recommendation Logic

The recommendation system connects the prediction results with procurement process information.

For example, cases identified as higher-risk can receive higher-priority recommendations, while process conditions such as bottlenecks can be used to provide more relevant actions.

The recommendation output is validated before being used in the final dashboard.

---

# Technology Used

### Programming

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* Logistic Regression
* Random Forest

### Data

* JSON
* CSV
* Procurement event data

### Visualization

* Microsoft Power BI

### Development

* Visual Studio Code
* Git
* GitHub
* Python virtual environment

---

# Project Structure


AI-Business-Process-Intelligence/
│
├── AI_Business_Process_Intelligence_Dashboard.pbix
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
│       └── visualizations/
│
└── src/
    ├── data_cleaning/
    ├── data_extraction/
    ├── final_analysis/
    ├── prediction/
    ├── process_analysis/
    └── recommendations/


---

# How to Run

## 1. Clone the repository

```bash
git clone https://github.com/reddy-hasini/AI-Business-Process-Intelligence.git
```

```bash
cd AI-Business-Process-Intelligence
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the environment

On Windows:

```bash
.venv\Scripts\activate
```

## 4. Install the main dependencies

```bash
pip install pandas numpy scikit-learn
```

Some scripts may require additional packages depending on the stage being executed.

## 5. Run the Python pipeline

The scripts are organized by stage under the `src` directory.

The general order is:


data_extraction
      ↓
data_cleaning
      ↓
process_analysis
      ↓
prediction
      ↓
recommendations
      ↓
final_analysis


## 6. Open the dashboard

Open the following file using Power BI Desktop:


AI_Business_Process_Intelligence_Dashboard.pbix


---

# Final Output

The final project produces:

* Cleaned procurement datasets
* Process analysis results
* Bottleneck analysis
* Delay prediction results
* Risk classifications
* Procurement recommendations
* Visualization datasets
* Power BI dashboard

The final files generated by the project are available under:


data/final/


---

# Limitations

The results depend on the procurement dataset used for the project. The predictions and recommendations are based on patterns available in the data and the logic implemented in the project.

The current dashboard is designed around the provided procurement data and would need additional configuration for use with a different organization's procurement system.

---

# Possible Future Improvements

Some possible improvements for a future version are:

* Add real-time procurement data
* Add automatic model retraining
* Add individual case-level explanations
* Add more detailed Power BI drill-downs
* Add automated alerts for high-risk cases
* Connect the system to an enterprise procurement system
* Deploy the prediction pipeline as an API
* Add cloud-based deployment
* Improve explainability of delay predictions

---

# What I Learned

Through this project, I worked with different parts of a complete data and analytics workflow, including:

* Working with event-based business data
* Data cleaning and transformation
* Process analysis
* Feature preparation
* Machine learning
* Model validation
* Recommendation logic
* Data visualization
* Power BI dashboard development
* Git and GitHub project management

The main focus of the project was to connect the technical analysis with a business problem rather than building a machine learning model separately from the business process.

---

## Author

Reddy Hasini Reddy

B.Tech — Information Technology
