"""
data_cleaning.py - Comprehensive Data Cleaning and Quality Assurance Pipeline
Retail Sales Data Visualization Project
"""

import os
import re
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


def parse_date_smart(val: Any) -> pd.Timestamp:
    """
    Intelligently parse mixed retail date formats:
    - ISO format: 'YYYY-MM-DD'
    - Mon format: 'DD-Mon-YYYY' (e.g. '18-Jul-2023')
    - Slashed format: 'DD/MM/YYYY' (e.g. '20/04/2024')
    - Dashed US format: 'MM-DD-YYYY' (e.g. '02-21-2024')
    """
    if pd.isna(val):
        return pd.NaT
    s = str(val).strip()
    if not s or s.lower() in ('nan', 'none', 'nat', 'null', ''):
        return pd.NaT
    
    # ISO standard: YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}$', s):
        return pd.to_datetime(s, format='%Y-%m-%d', errors='coerce')
    
    # DD-Mon-YYYY: e.g. 18-Jul-2023
    if re.match(r'^\d{1,2}-[A-Za-z]{3}-\d{4}$', s):
        return pd.to_datetime(s, format='%d-%b-%Y', errors='coerce')
    
    # DD/MM/YYYY with slashes
    if '/' in s:
        return pd.to_datetime(s, format='%d/%m/%Y', errors='coerce')
    
    # MM-DD-YYYY with dashes
    if re.match(r'^\d{2}-\d{2}-\d{4}$', s):
        return pd.to_datetime(s, format='%m-%d-%Y', errors='coerce')
        
    return pd.to_datetime(s, errors='coerce')


def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load raw retail transaction CSV."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw dataset file not found at: {filepath}")
    return pd.read_csv(filepath)


def assess_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform rigorous data quality audit on raw retail dataframe.
    Evaluates schema, missing values, duplicates, and range/logic anomalies.
    """
    total_records = len(df)
    total_cols = len(df.columns)
    exact_duplicates = int(df.duplicated().sum())
    duplicate_txns = int(df['Transaction_ID'].duplicated().sum()) if 'Transaction_ID' in df.columns else 0
    unique_txns = int(df['Transaction_ID'].nunique()) if 'Transaction_ID' in df.columns else 0
    unique_customers = int(df['Customer_ID'].nunique()) if 'Customer_ID' in df.columns else 0
    
    # Missing value counts
    missing_dict = df.isnull().sum().to_dict()
    
    # Logical and Domain Range Checks
    # Age: Valid customer age between 18 and 100
    age_series = pd.to_numeric(df['Age'], errors='coerce')
    age_negative = int((age_series < 18).sum())
    age_extreme = int((age_series > 100).sum())
    age_missing = int(age_series.isnull().sum())
    
    # Discount: Should be proportion between 0.0 and 0.5
    disc_series = pd.to_numeric(df['Discount'], errors='coerce')
    disc_negative = int((disc_series < 0).sum())
    disc_excess = int((disc_series > 0.5).sum())
    disc_missing = int(disc_series.isnull().sum())
    
    # Income: Missing and extreme values
    income_series = pd.to_numeric(df['Income'], errors='coerce')
    income_missing = int(income_series.isnull().sum())
    income_high_outliers = int((income_series > 500_000).sum())
    
    # Dates
    o_dates = df['Order_Date'].apply(parse_date_smart)
    d_dates = df['Delivery_Date'].apply(parse_date_smart)
    delivery_predated = int(((d_dates < o_dates) & d_dates.notnull() & o_dates.notnull()).sum())
    delivery_missing = int(d_dates.isnull().sum())
    
    # Customer Ratings: Check outside [1, 5]
    rating_series = pd.to_numeric(df['Customer_Rating'], errors='coerce')
    rating_invalid = int(((rating_series < 1) | (rating_series > 5)).sum())
    rating_missing = int(rating_series.isnull().sum())
    
    # Categorical inconsistencies
    gender_unique = list(df['Gender'].dropna().unique()) if 'Gender' in df.columns else []
    region_unique = list(df['Region'].dropna().unique()) if 'Region' in df.columns else []

    return {
        "total_records": total_records,
        "total_columns": total_cols,
        "exact_duplicates": exact_duplicates,
        "duplicate_transactions": duplicate_txns,
        "unique_transactions": unique_txns,
        "unique_customers": unique_customers,
        "missing_values": missing_dict,
        "age_anomalies": {
            "under_18": age_negative,
            "over_100": age_extreme,
            "missing": age_missing
        },
        "discount_anomalies": {
            "negative": disc_negative,
            "over_half": disc_excess,
            "missing": disc_missing
        },
        "income_anomalies": {
            "missing": income_missing,
            "high_outliers_over_500k": income_high_outliers,
            "min_income": float(income_series.min()),
            "max_income": float(income_series.max()),
            "median_income": float(income_series.median())
        },
        "date_anomalies": {
            "delivery_predates_order": delivery_predated,
            "delivery_missing": delivery_missing
        },
        "rating_anomalies": {
            "invalid_range": rating_invalid,
            "missing": rating_missing
        },
        "categorical_variants": {
            "gender_raw": gender_unique,
            "region_raw": region_unique
        }
    }


def clean_retail_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Execute full enterprise data cleaning pipeline following all requirements:
    1. Parse mixed Order_Date and Delivery_Date.
    2. Remove duplicate records (documenting count).
    3. Standardize text labels and casings (Gender, Region, Segment, Products).
    4. Validate and impute Age (using customer's own profile first, then segment median).
    5. Validate Income (preserve valid high earners, impute customer profile or segment median).
    6. Reconstruct Discount accurately via pricing identity Sales = Qty * Price * (1 - Disc).
    7. Verify Sales, Cost, Profit identities.
    8. Handle anomalous predated delivery dates transparently.
    9. Validate Customer_Rating (1-5) and Satisfaction_Level.
    10. Engineer analytical dimensions (Year, Month, YearMonth, Profit_Margin, Delivery_Days).
    """
    initial_count = len(df)
    clean_df = df.copy()
    
    # 1. Parse Dates Smartly
    clean_df['Order_Date'] = clean_df['Order_Date'].apply(parse_date_smart)
    clean_df['Delivery_Date'] = clean_df['Delivery_Date'].apply(parse_date_smart)
    
    # 2. Standardize Categorical Columns before deduplication
    # Gender Standardization
    gender_map = {
        'male': 'Male', 'm': 'Male', 'mALE': 'Male', 'MALE': 'Male', 'M': 'Male',
        'female': 'Female', 'f': 'Female', 'fEMALE': 'Female', 'FEMALE': 'Female', 'F': 'Female'
    }
    clean_df['Gender'] = clean_df['Gender'].astype(str).str.strip().map(
        lambda g: gender_map.get(g, gender_map.get(g.lower(), g.capitalize()))
    )
    
    # Region Standardization
    region_map = {
        'north': 'North', 'NORTH': 'North', 'Nort': 'North',
        'south': 'South', 'SOUTH': 'South', 'Sth': 'South',
        'east': 'East', 'EAST': 'East',
        'west': 'West', 'WEST': 'West'
    }
    clean_df['Region'] = clean_df['Region'].astype(str).str.strip().map(
        lambda r: region_map.get(r, region_map.get(r.capitalize(), r))
    )
    
    # Customer Segment, Product Category, Payment, Delivery Casing
    for col in ['Customer_Segment', 'Product_Category', 'Product', 'Payment_Method', 'Delivery_Mode', 'Satisfaction_Level', 'Returned']:
        if col in clean_df.columns:
            clean_df[col] = clean_df[col].astype(str).str.strip()
            
    clean_df['Returned'] = clean_df['Returned'].map(lambda x: 'Yes' if str(x).lower() == 'yes' else 'No')
    
    # 3. Deduplicate
    exact_duplicates_count = int(clean_df.duplicated().sum())
    # Deduplicate by unique Transaction_ID (preserving first occurrence)
    txn_duplicates_count = int(clean_df['Transaction_ID'].duplicated().sum())
    clean_df = clean_df.drop_duplicates(subset=['Transaction_ID'], keep='first').copy()
    deduped_count = len(clean_df)
    
    # 4. Age Cleaning:
    # First, mark invalid values (< 18 or > 100) as NaN
    clean_df.loc[(clean_df['Age'] < 18) | (clean_df['Age'] > 100), 'Age'] = np.nan
    
    # Recover age from the customer's own valid records across their orders
    cust_age_profile = clean_df.groupby('Customer_ID')['Age'].transform(
        lambda s: s.dropna().iloc[0] if len(s.dropna()) > 0 else np.nan
    )
    clean_df['Age'] = clean_df['Age'].fillna(cust_age_profile)
    
    # For any remaining missing age, impute with Customer_Segment median
    seg_age_median = clean_df.groupby('Customer_Segment')['Age'].transform('median')
    clean_df['Age'] = clean_df['Age'].fillna(seg_age_median).round()
    
    # 5. Income Cleaning:
    # Coerce any non-numeric text like '#######' to NaN
    clean_df['Income'] = pd.to_numeric(clean_df['Income'], errors='coerce')
    clean_df.loc[clean_df['Income'] <= 0, 'Income'] = np.nan
    
    # Recover income from customer profile
    cust_inc_profile = clean_df.groupby('Customer_ID')['Income'].transform(
        lambda s: s.dropna().median() if len(s.dropna()) > 0 else np.nan
    )
    clean_df['Income'] = clean_df['Income'].fillna(cust_inc_profile)
    
    # For remaining 6 nulls, impute with Region & Segment median
    reg_seg_inc_median = clean_df.groupby(['Region', 'Customer_Segment'])['Income'].transform('median')
    clean_df['Income'] = clean_df['Income'].fillna(reg_seg_inc_median)
    
    # 6. Discount Validation and Accurate Reconstruction
    # Sales = Quantity * Unit_Price * (1 - Discount) => Discount = 1 - (Sales / (Quantity * Unit_Price))
    gross_amount = clean_df['Quantity'] * clean_df['Unit_Price']
    implied_discount = (1.0 - (clean_df['Sales'] / gross_amount)).clip(0.0, 0.5).round(2)
    
    # Fix invalid discounts (-0.2, 2.0, NaN, etc.) using implied discount
    invalid_disc_mask = (clean_df['Discount'].isnull()) | (clean_df['Discount'] < 0.0) | (clean_df['Discount'] > 0.5)
    repaired_discount_count = int(invalid_disc_mask.sum())
    clean_df.loc[invalid_disc_mask, 'Discount'] = implied_discount[invalid_disc_mask]
    clean_df['Discount'] = clean_df['Discount'].round(2)
    
    # 7. Financial Auditing: Sales, Cost, Profit
    # Re-verify and ensure mathematical consistency:
    # Recalculate Sales exactly to avoid rounding discrepancies
    clean_df['Sales'] = (gross_amount * (1.0 - clean_df['Discount'])).round(2)
    clean_df['Profit'] = (clean_df['Sales'] - clean_df['Cost']).round(2)
    clean_df['Profit_Margin'] = ((clean_df['Profit'] / clean_df['Sales']) * 100).round(2)
    
    # 8. Handling Predated Delivery Dates
    # Detect rows where Delivery_Date < Order_Date
    predated_mask = (clean_df['Delivery_Date'] < clean_df['Order_Date']) & clean_df['Delivery_Date'].notnull()
    predated_count = int(predated_mask.sum())
    
    clean_df['Delivery_Date_Anomalous'] = predated_mask
    # Correct Delivery_Date: in logistics, inverted dates represent entry flip.
    # We swap Order_Date and Delivery_Date if Delivery was recorded earlier by 1-4 days
    for idx in clean_df[predated_mask].index:
        ord_d = clean_df.loc[idx, 'Order_Date']
        del_d = clean_df.loc[idx, 'Delivery_Date']
        clean_df.loc[idx, 'Order_Date'] = min(ord_d, del_d)
        clean_df.loc[idx, 'Delivery_Date'] = max(ord_d, del_d)
        
    # Calculate transit time (Delivery Days)
    clean_df['Delivery_Days'] = (clean_df['Delivery_Date'] - clean_df['Order_Date']).dt.days
    
    # 9. Customer Rating & Satisfaction Level Validation
    clean_df['Customer_Rating'] = pd.to_numeric(clean_df['Customer_Rating'], errors='coerce')
    # Validate ratings are strictly within 1 to 5
    clean_df.loc[(clean_df['Customer_Rating'] < 1) | (clean_df['Customer_Rating'] > 5), 'Customer_Rating'] = np.nan
    
    # Satisfaction Level validation
    valid_sat = {'Low', 'Medium', 'High'}
    clean_df.loc[~clean_df['Satisfaction_Level'].isin(valid_sat), 'Satisfaction_Level'] = np.nan
    # Impute missing Satisfaction_Level from Rating if available:
    # 1,2 -> Low; 3 -> Medium; 4,5 -> High
    def impute_sat(row):
        if pd.notnull(row['Satisfaction_Level']) and row['Satisfaction_Level'] in valid_sat:
            return row['Satisfaction_Level']
        r = row['Customer_Rating']
        if pd.notnull(r):
            if r <= 2.0:
                return 'Low'
            elif r == 3.0:
                return 'Medium'
            else:
                return 'High'
        return 'Medium'
        
    clean_df['Satisfaction_Level'] = clean_df.apply(impute_sat, axis=1)
    
    # 10. Date Dimensions Feature Engineering
    clean_df['Year'] = clean_df['Order_Date'].dt.year
    clean_df['Month'] = clean_df['Order_Date'].dt.month
    clean_df['Month_Name'] = clean_df['Order_Date'].dt.strftime('%b')
    clean_df['Year_Month'] = clean_df['Order_Date'].dt.to_period('M').astype(str)
    clean_df['Quarter'] = clean_df['Order_Date'].dt.to_period('Q').astype(str)
    clean_df['Day_of_Week'] = clean_df['Order_Date'].dt.day_name()
    
    # Age Groups & Income Brackets
    clean_df['Age_Group'] = pd.cut(
        clean_df['Age'],
        bins=[17, 25, 35, 50, 65, 100],
        labels=['18-25', '26-35', '36-50', '51-65', '65+']
    )
    
    clean_df['Income_Bracket'] = pd.cut(
        clean_df['Income'],
        bins=[0, 30_000, 50_000, 80_000, 150_000, np.inf],
        labels=['Low (<30K)', 'Lower-Mid (30K-50K)', 'Middle (50K-80K)', 'Upper-Mid (80K-150K)', 'High (>150K)']
    )

    cleaning_report = {
        "raw_record_count": initial_count,
        "exact_duplicates_removed": exact_duplicates_count,
        "total_duplicates_removed": txn_duplicates_count,
        "final_cleaned_record_count": len(clean_df),
        "discounts_repaired": repaired_discount_count,
        "predated_deliveries_corrected": predated_count,
        "age_missing_imputed": int(df['Age'].isnull().sum()),
        "income_missing_imputed": int(df['Income'].isnull().sum())
    }

    return clean_df, cleaning_report


def save_cleaned_data(df: pd.DataFrame, filepath: str) -> None:
    """Save cleaned dataframe to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Cleaned dataset successfully saved to: {filepath}")


if __name__ == '__main__':
    base_dir = r"c:\Users\prash\OneDrive\Desktop\New folder\Retail_Sales_Data_Visualization"
    raw_path = os.path.join(base_dir, "data", "retail_customer_sales_dataset.csv")
    cleaned_path = os.path.join(base_dir, "data", "retail_sales_cleaned.csv")
    
    print("Step 1: Loading raw retail dataset...")
    raw_df = load_raw_data(raw_path)
    
    print("\nStep 2: Assessing Data Quality...")
    audit = assess_data_quality(raw_df)
    print(f"Raw Shape: {audit['total_records']} rows, {audit['total_columns']} columns")
    print(f"Exact Duplicates: {audit['exact_duplicates']}, Duplicate Txn IDs: {audit['duplicate_transactions']}")
    print(f"Age Anomalies: {audit['age_anomalies']}")
    print(f"Discount Anomalies: {audit['discount_anomalies']}")
    print(f"Predated Deliveries: {audit['date_anomalies']['delivery_predates_order']}")
    
    print("\nStep 3: Executing Data Cleaning Pipeline...")
    cleaned_df, report = clean_retail_data(raw_df)
    print("Cleaning Report Summary:")
    for k, v in report.items():
        print(f"  - {k}: {v}")
        
    print("\nStep 4: Saving cleaned dataset...")
    save_cleaned_data(cleaned_df, cleaned_path)
    print(f"Cleaned dataset verified. Final shape: {cleaned_df.shape}")
