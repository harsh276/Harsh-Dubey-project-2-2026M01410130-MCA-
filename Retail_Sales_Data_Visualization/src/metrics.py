"""
metrics.py - Business Metrics and Formatting Utilities
Retail Sales Data Visualization Project
"""

from typing import Union, Dict, Any


def format_currency(value: Union[int, float], symbol: str = "₹", decimals: int = 2) -> str:
    """Format numeric values into standard Indian / International currency representation."""
    if value is None or (isinstance(value, float) and (value != value)):  # NaN check
        return "N/A"
    
    abs_val = abs(value)
    sign = "-" if value < 0 else ""
    
    if abs_val >= 10_000_000:
        return f"{sign}{symbol}{abs_val / 10_000_000:.{decimals}f} Cr"
    elif abs_val >= 100_000:
        return f"{sign}{symbol}{abs_val / 100_000:.{decimals}f} L"
    elif abs_val >= 1_000:
        return f"{sign}{symbol}{abs_val / 1_000:.{decimals}f} K"
    else:
        return f"{sign}{symbol}{abs_val:,.{decimals}f}"


def format_currency_full(value: Union[int, float], symbol: str = "₹") -> str:
    """Format numeric values with full comma separators."""
    if value is None or (isinstance(value, float) and (value != value)):
        return "N/A"
    return f"{symbol}{value:,.2f}"


def format_percentage(value: Union[int, float], decimals: int = 1) -> str:
    """Format float proportion or percentage to string."""
    if value is None or (isinstance(value, float) and (value != value)):
        return "N/A"
    return f"{value:.{decimals}f}%"


def format_number(value: Union[int, float]) -> str:
    """Format integer or float with thousand commas."""
    if value is None or (isinstance(value, float) and (value != value)):
        return "N/A"
    if isinstance(value, int) or value.is_integer():
        return f"{int(value):,}"
    return f"{value:,.2f}"


def compute_kpis(df) -> Dict[str, Any]:
    """
    Compute core retail performance KPIs:
    1. Total Sales
    2. Total Profit
    3. Profit Margin (%)
    4. Average Order Value (AOV)
    5. Total Orders / Transactions
    6. Unique Customers
    7. Return Rate (%)
    8. Average Customer Rating
    """
    total_sales = float(df['Sales'].sum()) if 'Sales' in df.columns else 0.0
    total_profit = float(df['Profit'].sum()) if 'Profit' in df.columns else 0.0
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0
    total_orders = int(len(df))
    aov = (total_sales / total_orders) if total_orders > 0 else 0.0
    
    unique_customers = int(df['Customer_ID'].nunique()) if 'Customer_ID' in df.columns else 0
    
    if 'Returned' in df.columns:
        return_count = int((df['Returned'].astype(str).str.strip().str.lower() == 'yes').sum())
        return_rate = (return_count / total_orders * 100) if total_orders > 0 else 0.0
    else:
        return_rate = 0.0
        
    if 'Customer_Rating' in df.columns:
        valid_ratings = df['Customer_Rating'].dropna()
        avg_rating = float(valid_ratings.mean()) if len(valid_ratings) > 0 else 0.0
    else:
        avg_rating = 0.0
        
    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "profit_margin": profit_margin,
        "aov": aov,
        "total_orders": total_orders,
        "unique_customers": unique_customers,
        "return_rate": return_rate,
        "avg_rating": avg_rating
    }
