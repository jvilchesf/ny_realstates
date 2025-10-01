# NYC Real Estate Trends Analysis

Interactive data visualization and analysis of New York City real estate trends using DOB (Department of Buildings) job application filings data.

[![Tableau Dashboard](https://img.shields.io/badge/Tableau-Dashboard-blue)](https://public.tableau.com/app/profile/jose.miguel.vilches.fierro/viz/Job_application_filling/Dashboard1)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)

## 📊 Project Overview

This project explores and visualizes real estate trends in New York City to help building owners, prospective buyers, and other stakeholders understand current market dynamics, regulatory approvals, and construction activities. By leveraging publicly available datasets from NYC Open Data, the analysis sheds light on how economic conditions, city policies, and neighborhood characteristics influence the permitting process and building trends throughout NYC.

### Target Audience

- Real estate professionals and investors
- Building owners and property managers
- NYC residents interested in neighborhood development
- Data analysts and researchers studying urban development
- Policymakers and urban planners

## 🎯 Key Features

- **Interactive Dashboard**: Explore NYC real estate trends through an intuitive Tableau interface
- **Multi-dimensional Analysis**: Filter by borough, year, job type, building class, and more
- **Geospatial Visualization**: Map-based views of permit approvals across NYC
- **Cost Analysis**: Track construction costs and investment patterns
- **Time Series Trends**: Monitor approval patterns over 2023-2024

## 🛠️ Tools and Technologies

- **Python Libraries**:
  - `pandas` - Data manipulation and analysis
  - `polars` - High-performance data processing
  - `seaborn` - Statistical data visualization
  - `matplotlib` - Plotting and visualization

- **Visualization Platform**:
  - `Tableau Public` - Interactive dashboard creation

## 📁 Dataset

### Source
- **NYC DOB Job Application Filings Dataset**
- Public dataset from NYC Open Data
- [View Dataset](https://data.cityofnewyork.us/Housing-Development/DOB-Job-Application-Filings/ic3t-wcy2/about_data)

### Dataset Characteristics

- **Size**: Thousands of rows with 96 columns
- **Time Period**: Focused on approvals in 2023-2024
- **Key Fields**:
  - `Borough` - NYC borough (Manhattan, Brooklyn, Queens, The Bronx, Staten Island)
  - `Job Type` - Type of job application (new building, alteration, etc.)
  - `Job Status` - Current application status (Approved, Filed, etc.)
  - `Approved` - Date of job application approval
  - `Job #` - Unique identifier for each application
  - `Building Type` - Classification (Residential, Mixed-use, etc.)
  - `Initial Cost` - Estimated project cost
  - `GIS_LATITUDE` / `GIS_LONGITUDE` - Geospatial coordinates
  - `BUILDING_CLASS` - NYC Department of Finance classification code

## 🔄 Data Processing Workflow

### 1. Data Extraction
```python
# Load raw data using polars for efficient processing
df = pl.read_csv('DOB_Job_Application_Filings.csv', 
                 schema_overrides=schema_overrides,
                 ignore_errors=True)
```

### 2. Data Cleaning
- Parse datetime fields
- Handle null values
- Filter by approval years (2023-2024)
- Convert data types for compatibility

### 3. Data Transformation
- Group by key dimensions (Borough, Job Type, Status)
- Aggregate geospatial coordinates (mean latitude/longitude)
- Sum initial costs by category
- Generate clean export for visualization

### 4. Data Export
- Export processed CSV for Tableau ingestion
- Ensure data quality and consistency

## 📂 Repository Structure

```
nyc-real-estate-trends/
├── README.md                          # This file
├── data/
│   ├── raw/                          # Original dataset (not included due to size)
│   └── processed/                    # Cleaned and aggregated data
├── scripts/
│   └── data_processing.py            # Python script for ETL pipeline
├── notebooks/
│   └── exploratory_analysis.ipynb    # Jupyter notebook for exploration
└── requirements.txt                  # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8 or higher
pip package manager
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nyc-real-estate-trends.git
cd nyc-real-estate-trends
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download the dataset:
- Visit [NYC Open Data Portal](https://data.cityofnewyork.us/Housing-Development/DOB-Job-Application-Filings/ic3t-wcy2/about_data)
- Download the CSV file
- Place it in the `data/raw/` directory

### Usage

Run the data processing script:

```bash
python scripts/data_processing.py
```

This will:
- Load the raw dataset
- Clean and transform the data
- Generate aggregated metrics
- Export processed data to `data/processed/`

## 📈 Visualization

### Interactive Tableau Dashboard

Explore the full interactive dashboard here:
**[NYC Real Estate Trends Dashboard](https://public.tableau.com/app/profile/jose.miguel.vilches.fierro/viz/Job_application_filling/Dashboard1)**

The dashboard enables users to:
- Filter by borough, time period, and building attributes
- Visualize geographic distribution of permits
- Analyze cost trends and construction patterns
- Compare job types and approval statuses

## 💡 Key Insights

- **Neighborhood Trends**: Identify areas with increasing construction activity
- **Market Dynamics**: Understand how economic conditions affect approvals
- **Cost Analysis**: Track investment patterns across boroughs
- **Regulatory Patterns**: Monitor approval timelines and success rates
- **Building Types**: Analyze trends in residential vs. commercial development

## 🎯 Impact

### For Stakeholders
- **Informed Decision-Making**: Quickly identify neighborhood-level construction trends
- **Market Intelligence**: Track approvals, costs, and building types for strategic planning
- **Time Savings**: Automated pipelines reduce manual data wrangling

### For Analysts
- **Reproducible Analysis**: Clear documentation and code for transparency
- **Extensible Framework**: Easy to adapt for other cities or datasets
- **Best Practices**: Modern data processing techniques using polars and pandas

## 🔧 Challenges and Solutions

**Challenge**: Understanding complex dataset with numerous building classes, job types, and borough-level nuances.

**Solution**: Extensive data exploration combined with stakeholder communication to clarify data elements and align with business objectives.

