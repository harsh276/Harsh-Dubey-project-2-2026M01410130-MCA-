# Retail Sales Data Visualization & Interactive Analytics Dashboard

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![Visualizations](https://img.shields.io/badge/Charts-Plotly%20%7C%20Seaborn%20%7C%20Matplotlib-green.svg)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An enterprise-standard Business Intelligence and Data Analytics project built using Python, Pandas, Matplotlib, Seaborn, Plotly, Streamlit, and ReportLab.

This system converts 7,000 raw retail transaction records across India into strategic visual stories, dynamic web dashboards, publication-grade charts, and an executive PDF report. Suitable for MCA academic submission, professional portfolio presentation, and Data Analyst interview defense.

---

## 📌 Project Overview

Senior leadership in retail organizations need quick, clear visual summaries rather than dense spreadsheets. This project processes a simulated omnichannel retail transaction log spanning **two calendar years (2023–2024)** across **four Indian geographic regions** (North, South, East, West) and **16 states**.

### Headline Results (Verified from Dataset)
- **Total Revenue:** ₹76,731,189.27 (~₹7.67 Crores)
- **Total Net Profit:** ₹25,127,882.66 (~₹2.51 Crores)
- **Overall Profit Margin:** 32.75%
- **Average Order Value (AOV):** ₹10,961.60
- **Total Transactions:** 7,000 orders
- **Unique Customers:** 1,576
- **Merchandise Return Rate:** 12.57% (880 returns)
- **Average Customer Rating:** 3.09 / 5.0 stars

---

## 📂 Project Structure

```
Retail_Sales_Data_Visualization/
│
├── app.py                             # Interactive Streamlit Web Dashboard
├── requirements.txt                   # Project Python Dependencies
├── README.md                          # Full Project Documentation & Guide
│
├── data/
│   ├── retail_customer_sales_dataset.csv   # Raw Transactional Dataset (7,084 records)
│   └── retail_sales_cleaned.csv            # Cleaned Audited Dataset (7,000 records)
│
├── notebooks/
│   ├── Retail_Sales_Analysis.ipynb    # Executed 13-Section End-to-End Jupyter Notebook
│   └── build_notebook.py              # Notebook Generator Script
│
├── src/
│   ├── data_cleaning.py               # Robust Data Audit & Cleaning Pipeline
│   ├── analysis.py                    # KPI Aggregations & Statistical Calculations
│   ├── visualizations.py              # 12 Publication-Quality Charts (Matplotlib/Seaborn/Plotly)
│   └── metrics.py                     # Currency & Formatting Helpers
│
├── charts/                            # 12 Generated High-Resolution 300 DPI Chart Images
│   ├── viz01_monthly_sales_trend.png
│   ├── viz02_sales_by_region.png
│   ├── viz03_sales_by_product_category.png
│   ├── viz04_customer_age_distribution.png
│   ├── viz05_income_distribution.png
│   ├── viz06_sales_distribution_by_category.png
│   ├── viz07_sales_vs_profit.png
│   ├── viz08_discount_vs_profit.png
│   ├── viz09_sales_by_customer_segment.png
│   ├── viz10_correlation_heatmap.png
│   ├── viz11_avg_sales_category_region_heatmap.png
│   └── viz12_return_rate_by_category.png
│
├── reports/
│   ├── Retail_Sales_Visual_Report.pdf # Professional Multi-Page Executive PDF Report
│   ├── Project_Documentation.md       # Comprehensive Technical & Domain Report
│   └── generate_pdf_report.py         # Automated ReportLab PDF Report Compiler
│
└── assets/
    └── dashboard_assets/              # Visual Theme & Dashboard Assets
```

---

## 🛠️ Technology Stack

| Library | Version | Role in Project |
|:---|:---:|:---|
| **Python** | 3.10+ | Core language runtime environment |
| **Pandas** | ≥ 2.2.0 | Data wrangling, date parsing, auditing, and aggregations |
| **NumPy** | ≥ 1.26.0 | Mathematical and linear regression calculations |
| **Matplotlib** | ≥ 3.8.0 | Foundation plotting and publication styling |
| **Seaborn** | ≥ 0.13.0 | Statistical distribution histograms, box plots, and heatmaps |
| **Plotly** | ≥ 5.18.0 | Interactive web-based charts for dashboard slicing |
| **Streamlit** | ≥ 1.30.0 | Interactive web BI application with dynamic filters |
| **ReportLab** | ≥ 4.0.0 | Programmatic compilation of multi-page visual PDF report |
| **Jupyter** | ≥ 7.0.0 | Exploratory analysis, workflow documentation, and code execution |

---

## ⚙️ Installation & Setup

### 1. Clone or Open Project
Open a terminal in the project directory:
```bash
cd "c:\Users\prash\OneDrive\Desktop\New folder\Retail_Sales_Data_Visualization"
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Command Prompt:
.\venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Execution Guide

### Step 1: Run the Data Cleaning Pipeline
Audits raw transaction data, removes duplicates, fixes mixed dates, repairs discounts, imputes customer demographics, and saves `data/retail_sales_cleaned.csv`:
```bash
python src/data_cleaning.py
```

### Step 2: Generate All 12 Visualizations
Renders all publication-standard charts as 300 DPI PNGs into `charts/`:
```bash
python src/visualizations.py
```

### Step 3: Launch the Streamlit Dashboard
Launches the interactive analytics dashboard in your default browser:
```bash
streamlit run app.py
```
> The dashboard will automatically open at `http://localhost:8501`.

### Step 4: Re-generate the Executive PDF Report
Rebuilds the publication-grade PDF report `reports/Retail_Sales_Visual_Report.pdf`:
```bash
python reports/generate_pdf_report.py
```

### Step 5: Run or Inspect the Jupyter Notebook
Open the notebook in JupyterLab or VS Code:
```bash
jupyter notebook notebooks/Retail_Sales_Analysis.ipynb
```
> The notebook has been pre-executed from top to bottom with all 13 required sections and outputs embedded.

---

## 📊 Summary of the 12 Deliverable Visualizations

1. **Visualization 1: Monthly Sales Trend (2023 vs. 2024)**  
   *Line Chart:* Compares monthly revenues across 2023 (₹38.66M) and 2024 (₹38.08M), highlighting seasonal peaks in August and October.
2. **Visualization 2: Total Sales by Geographic Region**  
   *Comparative Bar Chart:* Analyzes revenue balance across East (26.1%), West (25.8%), South (24.6%), and North (23.5%).
3. **Visualization 3: Revenue by Product Category**  
   *Horizontal Bar Chart:* Demonstrates category concentration where Electronics (₹37.64M) and Furniture (₹26.06M) generate 83.0% of sales.
4. **Visualization 4: Customer Age Distribution**  
   *Histogram with KDE:* Evaluates age profile (Mean: 36.1 yrs, Median: 36.0 yrs, Skewness: +0.27).
5. **Visualization 5: Annual Income Distribution**  
   *Histogram:* Captures right-skewed purchasing power (Median: ₹48,816, Mean: ₹55,050, Skewness: +17.54, Max: ₹1.75M).
6. **Visualization 6: Order Value Spread & Outliers by Category**  
   *Categorical Box Plot:* Highlights ticket size variances from Furniture (~₹22K median) down to Grocery (~₹1.2K median).
7. **Visualization 7: Transaction Sales vs. Net Profit**  
   *Scatter Plot with OLS Fit:* Validates an exceptionally strong linear relationship ($r = +0.965, R^2 = 0.931$, Profit = 0.327 × Sales).
8. **Visualization 8: Discount Rate Impact on Profitability**  
   *Scatter Plot with Trendline:* Illustrates margin compression from heavy discounting (Slope: -₹5,111 per 1% discount).
9. **Visualization 9: Revenue Share by Customer Segment**  
   *Donut Chart:* Breaks down volume across Consumer (54.4%), Corporate (30.7%), and Home Office (14.9%).
10. **Visualization 10: Inter-Variable Correlation Heatmap**  
    *Matrix Heatmap:* Maps Pearson correlations across Sales, Profit, Discount, Quantity, Age, and Income.
11. **Visualization 11: Average Order Value by Category & Region**  
    *2D Pivot Heatmap:* Documents consistent cross-territorial average ticket sizes for every product category.
12. **Visualization 12: Merchandise Return Rates by Product Category**  
    *Comparative Bar Chart:* Identifies Clothing (13.50%) and Furniture (13.18%) as the primary return drivers above the 12.57% benchmark.

---

## 💡 Key Business Findings & Strategic Recommendations

1. **Protect Core High-Ticket Divisions:** Electronics and Furniture drive 83% of company revenue. Capital allocation and warranty bundling must focus on these two pillars.
2. **Cap Discretionary Discounts at 20%:** Discounts above 20% severely erode cash profit without driving proportionate volume elasticity.
3. **Apparel & Furniture Return Mitigation:** Introduce digital sizing fitment tools and room dimension checks to reduce the ~13.3% return rate in Clothing and Furniture, targeting ₹1.2M in annual reverse logistics savings.
4. **Expand B2B Corporate Procurement:** Formalize volume purchase agreements to expand the high-margin Corporate segment (currently 30.7%) toward 40%.

---

## ⚠️ Project Limitations

- **Simulated Retail Data:** The dataset is synthetic, designed for rigorous training and methodology testing.
- **Delivery Time Variances:** 106 records have missing delivery dates (orders currently in transit).
- **Subjective Survey Ratings:** Customer satisfaction ratings were completed for 93.9% of orders (428 unrated).

---

## 📄 License & Attribution

Developed for academic and professional portfolio presentation. Code and analysis are completely modular, original, and reproducible.
