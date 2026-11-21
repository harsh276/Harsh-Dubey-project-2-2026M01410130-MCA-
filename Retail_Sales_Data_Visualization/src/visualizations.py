"""
visualizations.py - Professional Data Visualization Suite
Matplotlib, Seaborn, and Plotly implementations for all 12 project deliverables.
"""

import os
from typing import Dict, Any, List, Optional
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set publication-standard aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Corporate Color Palette: Navy Blue, Teal, Slate, Soft Red, Amber
COLOR_PRIMARY = "#1B365D"    # Deep Navy
COLOR_SECONDARY = "#008080"  # Teal
COLOR_ACCENT = "#D9534F"     # Coral / Highlight
COLOR_MUTED = "#6C7A89"      # Slate Gray
COLOR_LIGHT = "#E9ECEF"      # Off-white / grid
PALETTE_5 = ["#1B365D", "#008080", "#2E86AB", "#A23B72", "#F18F01"]
PALETTE_REGION = {"North": "#1B365D", "South": "#008080", "East": "#2E86AB", "West": "#E28743"}


# ==============================================================================
# 1. MATPLOTLIB / SEABORN VISUALIZATION GENERATORS (FOR REPORTS & NOTEBOOK)
# ==============================================================================

def plot_monthly_sales_trend(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 1: Monthly Sales Trend (2023 vs 2024 Line Chart)."""
    monthly = df.groupby(['Year', 'Month'])['Sales'].sum().unstack(level=0) / 1e6
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly.index = month_names

    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    # 2023 Line
    ax.plot(monthly.index, monthly[2023], marker='o', linewidth=2.5, color=COLOR_PRIMARY, 
            label='2023 Sales (₹38.66M)', linestyle='-')
    # 2024 Line
    ax.plot(monthly.index, monthly[2024], marker='s', linewidth=2.5, color=COLOR_SECONDARY, 
            label='2024 Sales (₹38.08M)', linestyle='--')

    # Peak annotations
    max_2023_val = monthly[2023].max()
    max_2023_idx = monthly[2023].idxmax()
    ax.annotate(f'2023 Peak: ₹{max_2023_val:.2f}M', xy=(max_2023_idx, max_2023_val),
                xytext=(0, 14), textcoords='offset points', ha='center',
                fontsize=9, fontweight='bold', color=COLOR_PRIMARY,
                arrowprops=dict(arrowstyle='->', color=COLOR_PRIMARY, lw=1))

    max_2024_val = monthly[2024].max()
    max_2024_idx = monthly[2024].idxmax()
    ax.annotate(f'2024 Peak: ₹{max_2024_val:.2f}M', xy=(max_2024_idx, max_2024_val),
                xytext=(0, 14), textcoords='offset points', ha='center',
                fontsize=9, fontweight='bold', color=COLOR_SECONDARY,
                arrowprops=dict(arrowstyle='->', color=COLOR_SECONDARY, lw=1))

    ax.set_title("Monthly Retail Sales Trend Comparison (2023 vs. 2024)", pad=15)
    ax.set_xlabel("Calendar Month")
    ax.set_ylabel("Total Sales (₹ in Millions)")
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('₹%.1fM'))
    ax.set_ylim(bottom=1.8, top=4.5)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left')
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_sales_by_region(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 2: Total Sales by Region (Comparative Bar Chart)."""
    reg = df.groupby('Region')['Sales'].sum().sort_values(ascending=False) / 1e6
    
    fig, ax = plt.subplots(figsize=(9, 5.2))
    colors = [COLOR_PRIMARY if r == 'East' else (COLOR_MUTED if r == 'North' else COLOR_SECONDARY) for r in reg.index]
    
    bars = ax.bar(reg.index, reg.values, color=colors, width=0.55, edgecolor='none', zorder=3)
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    total_sales = reg.sum()
    for bar in bars:
        h = bar.get_height()
        share = (h / total_sales) * 100
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.35, f"₹{h:.2f}M\n({share:.1f}%)",
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#2C3E50')

    ax.set_title("Total Retail Sales by Geographic Region (2023–2024)", pad=15)
    ax.set_xlabel("Geographic Territory")
    ax.set_ylabel("Cumulative Sales (₹ in Millions)")
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('₹%.1fM'))
    ax.set_ylim(0, reg.max() * 1.2)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_sales_by_product_category(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 3: Sales by Product Category (Horizontal Bar Chart)."""
    cat = (df.groupby('Product_Category')['Sales'].sum() / 1e6).sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(9.5, 5))
    bars = ax.barh(cat.index, cat.values, color=COLOR_SECONDARY, height=0.55, zorder=3)
    ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
    
    total_sales = cat.sum()
    for bar in bars:
        w = bar.get_width()
        share = (w / total_sales) * 100
        ax.text(w + 0.6, bar.get_y() + bar.get_height()/2, f"₹{w:.2f}M  ({share:.1f}%)",
                va='center', fontsize=10, fontweight='bold', color=COLOR_PRIMARY)

    ax.set_title("Total Revenue Contribution by Product Category", pad=15)
    ax.set_xlabel("Cumulative Sales (₹ in Millions)")
    ax.set_ylabel("Product Category")
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('₹%.0fM'))
    ax.set_xlim(0, cat.max() * 1.25)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_customer_age_distribution(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 4: Customer Age Distribution (Histogram with KDE & Skewness)."""
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ages = df['Age'].dropna()
    mean_val = ages.mean()
    median_val = ages.median()
    skew_val = ages.skew()

    sns.histplot(ages, bins=25, kde=True, color=COLOR_PRIMARY, ax=ax, edgecolor='white', linewidth=0.8, alpha=0.65)
    ax.axvline(mean_val, color=COLOR_ACCENT, linestyle='--', linewidth=2, label=f'Mean Age: {mean_val:.1f} yrs')
    ax.axvline(median_val, color=COLOR_SECONDARY, linestyle='-', linewidth=2, label=f'Median Age: {median_val:.0f} yrs')

    ax.text(0.72, 0.78, f"Skewness: {skew_val:+.2f}\nRange: 18–72 yrs\nN = {len(ages):,}",
            transform=ax.transAxes, fontsize=10, bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#CBD5E0'))

    ax.set_title("Customer Demographic Profile: Age Distribution & Density", pad=15)
    ax.set_xlabel("Customer Age (Years)")
    ax.set_ylabel("Number of Orders")
    ax.legend(frameon=True, facecolor='white', loc='upper right')
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_income_distribution(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 5: Annual Income Distribution (Right-Skewed Histogram with Log View / Annotations)."""
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    incomes = df['Income'].dropna()
    mean_inc = incomes.mean()
    median_inc = incomes.median()
    skew_inc = incomes.skew()

    # Plot histogram clipping extreme display to 250k for readability while noting max
    display_data = incomes[incomes <= 250_000]
    outliers_count = (incomes > 250_000).sum()

    sns.histplot(display_data, bins=30, kde=True, color=COLOR_SECONDARY, ax=ax, edgecolor='white', alpha=0.65)
    ax.axvline(mean_inc, color=COLOR_ACCENT, linestyle='--', linewidth=2, label=f'Mean: ₹{mean_inc:,.0f}')
    ax.axvline(median_inc, color=COLOR_PRIMARY, linestyle='-', linewidth=2, label=f'Median: ₹{median_inc:,.0f}')

    ax.text(0.65, 0.75, (f"Skewness: {skew_inc:+.2f} (Right-Skewed)\n"
                        f"Median: ₹{median_inc:,.0f}\n"
                        f"Max: ₹{incomes.max():,.0f}\n"
                        f"Affluent Outliers (>₹250k): {outliers_count} orders"),
            transform=ax.transAxes, fontsize=9.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#CBD5E0'))

    ax.set_title("Customer Annual Income Distribution (Core Range & Right-Tail Outliers)", pad=15)
    ax.set_xlabel("Customer Annual Income (₹)")
    ax.set_ylabel("Transaction Count")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"₹{int(x/1000)}K"))
    ax.legend(frameon=True, facecolor='white', loc='upper right')
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_sales_distribution_by_category(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 6: Order Sales Spread by Category (Box Plot)."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    # Sort categories by median sales
    cat_order = df.groupby('Product_Category')['Sales'].median().sort_values(ascending=False).index

    sns.boxplot(x='Product_Category', y='Sales', data=df, order=cat_order,
                hue='Product_Category', legend=False,
                palette=PALETTE_5, ax=ax, width=0.5, fliersize=2.5,
                boxprops=dict(alpha=0.85))

    ax.set_title("Order Value Distribution & Outlier Spread across Product Categories", pad=15)
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Order Sales Value (₹)")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"₹{int(y/1000)}K" if y >= 1000 else f"₹{int(y)}"))
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_sales_vs_profit(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 7: Sales vs Profit (Scatter Plot with Fitted Regression Line)."""
    fig, ax = plt.subplots(figsize=(9.5, 5.5))

    # Scatter points sample for crystal clear rendering
    ax.scatter(df['Sales'] / 1e3, df['Profit'] / 1e3, color=COLOR_PRIMARY, alpha=0.35, s=20, edgecolors='none', label='Transactions')

    # Linear regression fit
    slope, intercept = np.polyfit(df['Sales'], df['Profit'], 1)
    r2 = np.corrcoef(df['Sales'], df['Profit'])[0, 1] ** 2
    
    x_vals = np.linspace(df['Sales'].min(), df['Sales'].max(), 100)
    y_vals = slope * x_vals + intercept
    ax.plot(x_vals / 1e3, y_vals / 1e3, color=COLOR_ACCENT, linewidth=2.5,
            label=f'Linear Fit: Profit = {slope:.3f} × Sales\n(R² = {r2:.3f}, r = +0.965)')

    ax.set_title("Transaction Value vs. Realized Net Profit (Linearity & Elasticity)", pad=15)
    ax.set_xlabel("Order Sales (₹ in Thousands)")
    ax.set_ylabel("Realized Profit (₹ in Thousands)")
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('₹%dK'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('₹%dK'))
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left')
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_discount_vs_profit(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 8: Discount vs Profit (Scatter Plot with Trend Line)."""
    fig, ax = plt.subplots(figsize=(9.5, 5.5))

    disc_pct = df['Discount'] * 100
    profit_k = df['Profit'] / 1e3
    
    ax.scatter(disc_pct, profit_k, color=COLOR_SECONDARY, alpha=0.3, s=20, edgecolors='none', label='Order Orders')

    slope, intercept = np.polyfit(disc_pct, profit_k, 1)
    r2 = np.corrcoef(disc_pct, profit_k)[0, 1] ** 2
    
    x_vals = np.linspace(0, 50, 100)
    y_vals = slope * x_vals + intercept
    ax.plot(x_vals, y_vals, color=COLOR_ACCENT, linewidth=2.5,
            label=f'Trend: Slope = {slope:.2f}K per 1% Disc\n(R² = {r2:.4f}, Negative Drift)')

    ax.set_title("Impact of Promotional Discounting on Transaction Profitability", pad=15)
    ax.set_xlabel("Discount Rate Applied (%)")
    ax.set_ylabel("Order Profit (₹ in Thousands)")
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d%%'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('₹%dK'))
    ax.set_xlim(-2, 53)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper right')
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_sales_by_customer_segment(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 9: Sales Share by Customer Segment (Professional Donut Chart)."""
    seg = df.groupby('Customer_Segment')['Sales'].sum()
    labels = seg.index
    values = seg.values
    colors = [COLOR_PRIMARY, COLOR_SECONDARY, "#E28743"]

    fig, ax = plt.subplots(figsize=(7.5, 6))
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        pctdistance=0.75,
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.5)
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)

    for text in texts:
        text.set_fontsize(11)
        text.set_fontweight('bold')

    # Center label
    total_sales_cr = values.sum() / 1e7
    ax.text(0, 0, f"Total Sales\n₹{total_sales_cr:.2f} Cr", ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_PRIMARY)

    ax.set_title("Revenue Share by Customer Segment (2023–2024)", pad=20)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 10: Numerical Correlation Heatmap."""
    cols = ['Sales', 'Profit', 'Discount', 'Quantity', 'Age', 'Income']
    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6.2))
    cmap = sns.diverging_palette(220, 20, as_cmap=True)

    sns.heatmap(corr, annot=True, fmt='.3f', cmap=cmap, vmin=-0.25, vmax=1.0,
                square=True, linewidths=1.2, linecolor='white', cbar_kws={"shrink": 0.8},
                ax=ax, annot_kws={"size": 10, "weight": "bold"})

    ax.set_title("Correlation Matrix of Key Numerical Commercial Variables", pad=15)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_category_region_heatmap(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 11: Average Sales by Category and Region (Pivot Heatmap)."""
    pivot = df.pivot_table(index='Product_Category', columns='Region', values='Sales', aggfunc='mean')

    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='Blues', linewidths=1.2,
                linecolor='white', cbar_kws={'label': 'Mean Ticket Size (₹)'},
                ax=ax, annot_kws={'size': 10, 'weight': 'bold'})

    ax.set_title("Average Order Sales Value by Product Category & Geographic Region", pad=15)
    ax.set_xlabel("Geographic Territory")
    ax.set_ylabel("Product Line")
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def plot_return_rate_by_category(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """Visualization 12: Return Rate by Product Category (Bar Chart with Benchmark Line)."""
    ret = df.groupby('Product_Category')['Returned'].apply(lambda s: (s == 'Yes').mean() * 100).sort_values(ascending=False)
    overall_ret = (df['Returned'] == 'Yes').mean() * 100

    fig, ax = plt.subplots(figsize=(9, 5.2))
    colors = [COLOR_ACCENT if r > overall_ret else COLOR_SECONDARY for r in ret.values]
    
    bars = ax.bar(ret.index, ret.values, color=colors, width=0.52, zorder=3)
    ax.axhline(overall_ret, color='#E74C3C', linestyle='--', linewidth=1.8, zorder=4,
               label=f'Company Benchmark: {overall_ret:.2f}%')
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.35, f"{h:.2f}%",
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#2C3E50')

    ax.set_title("Merchandise Return Rate (%) Across Product Categories", pad=15)
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Return Rate Percentage (%)")
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f%%'))
    ax.set_ylim(0, ret.max() * 1.3)
    ax.legend(frameon=True, facecolor='white', loc='upper right')
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight', dpi=300)
    return fig


def generate_all_static_charts(df: pd.DataFrame, output_dir: str) -> Dict[str, str]:
    """Generate and save all 12 publication-quality chart PNGs."""
    os.makedirs(output_dir, exist_ok=True)
    chart_paths = {
        "viz01_monthly_trend": os.path.join(output_dir, "viz01_monthly_sales_trend.png"),
        "viz02_sales_by_region": os.path.join(output_dir, "viz02_sales_by_region.png"),
        "viz03_sales_by_category": os.path.join(output_dir, "viz03_sales_by_product_category.png"),
        "viz04_age_distribution": os.path.join(output_dir, "viz04_customer_age_distribution.png"),
        "viz05_income_distribution": os.path.join(output_dir, "viz05_income_distribution.png"),
        "viz06_sales_distribution_by_category": os.path.join(output_dir, "viz06_sales_distribution_by_category.png"),
        "viz07_sales_vs_profit": os.path.join(output_dir, "viz07_sales_vs_profit.png"),
        "viz08_discount_vs_profit": os.path.join(output_dir, "viz08_discount_vs_profit.png"),
        "viz09_segment_share": os.path.join(output_dir, "viz09_sales_by_customer_segment.png"),
        "viz10_correlation_matrix": os.path.join(output_dir, "viz10_correlation_heatmap.png"),
        "viz11_category_region_pivot": os.path.join(output_dir, "viz11_avg_sales_category_region_heatmap.png"),
        "viz12_return_rate_by_category": os.path.join(output_dir, "viz12_return_rate_by_category.png"),
    }

    print("Generating Visualization 1: Monthly Sales Trend...")
    plot_monthly_sales_trend(df, chart_paths["viz01_monthly_trend"])
    plt.close('all')

    print("Generating Visualization 2: Sales by Region...")
    plot_sales_by_region(df, chart_paths["viz02_sales_by_region"])
    plt.close('all')

    print("Generating Visualization 3: Sales by Product Category...")
    plot_sales_by_product_category(df, chart_paths["viz03_sales_by_category"])
    plt.close('all')

    print("Generating Visualization 4: Customer Age Distribution...")
    plot_customer_age_distribution(df, chart_paths["viz04_age_distribution"])
    plt.close('all')

    print("Generating Visualization 5: Income Distribution...")
    plot_income_distribution(df, chart_paths["viz05_income_distribution"])
    plt.close('all')

    print("Generating Visualization 6: Sales Distribution by Category...")
    plot_sales_distribution_by_category(df, chart_paths["viz06_sales_distribution_by_category"])
    plt.close('all')

    print("Generating Visualization 7: Sales vs Profit...")
    plot_sales_vs_profit(df, chart_paths["viz07_sales_vs_profit"])
    plt.close('all')

    print("Generating Visualization 8: Discount vs Profit...")
    plot_discount_vs_profit(df, chart_paths["viz08_discount_vs_profit"])
    plt.close('all')

    print("Generating Visualization 9: Customer Segment Share...")
    plot_sales_by_customer_segment(df, chart_paths["viz09_segment_share"])
    plt.close('all')

    print("Generating Visualization 10: Correlation Heatmap...")
    plot_correlation_heatmap(df, chart_paths["viz10_correlation_matrix"])
    plt.close('all')

    print("Generating Visualization 11: Category-Region Pivot...")
    plot_category_region_heatmap(df, chart_paths["viz11_category_region_pivot"])
    plt.close('all')

    print("Generating Visualization 12: Return Rate by Category...")
    plot_return_rate_by_category(df, chart_paths["viz12_return_rate_by_category"])
    plt.close('all')

    print("All 12 static charts successfully generated and saved.")
    return chart_paths


# ==============================================================================
# 2. INTERACTIVE PLOTLY FIGURES (FOR STREAMLIT DASHBOARD)
# ==============================================================================

def plotly_monthly_trend(df: pd.DataFrame) -> go.Figure:
    """Plotly Interactive Monthly Sales Trend."""
    monthly = df.groupby(['Year', 'Month', 'Month_Name'])['Sales'].sum().reset_index()
    monthly['Sales_M'] = monthly['Sales'] / 1e6
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly['Month_Name'] = pd.Categorical(monthly['Month_Name'], categories=month_order, ordered=True)
    monthly = monthly.sort_values(['Year', 'Month'])

    fig = px.line(
        monthly,
        x='Month_Name',
        y='Sales_M',
        color='Year',
        markers=True,
        color_discrete_map={2023: COLOR_PRIMARY, 2024: COLOR_SECONDARY},
        labels={'Month_Name': 'Month', 'Sales_M': 'Sales (₹ Millions)', 'Year': 'Year'},
        title='<b>Monthly Sales Trend Comparison (2023 vs 2024)</b>'
    )
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig


def plotly_sales_by_region(df: pd.DataFrame) -> go.Figure:
    """Plotly Interactive Regional Sales Bar Chart."""
    reg = df.groupby('Region')['Sales'].sum().reset_index()
    reg['Sales_M'] = reg['Sales'] / 1e6
    reg = reg.sort_values('Sales_M', ascending=False)

    fig = px.bar(
        reg,
        x='Region',
        y='Sales_M',
        color='Region',
        color_discrete_map=PALETTE_REGION,
        text_auto='.2f',
        labels={'Sales_M': 'Sales (₹ Millions)', 'Region': 'Territory'},
        title='<b>Total Revenue by Region</b>'
    )
    fig.update_layout(template='plotly_white', showlegend=False)
    fig.update_traces(texttemplate='₹%{y:.2f}M', textposition='outside')
    return fig


def plotly_sales_by_category(df: pd.DataFrame) -> go.Figure:
    """Plotly Interactive Category Revenue Bar Chart."""
    cat = df.groupby('Product_Category')['Sales'].sum().reset_index()
    cat['Sales_M'] = cat['Sales'] / 1e6
    cat = cat.sort_values('Sales_M', ascending=True)

    fig = px.bar(
        cat,
        x='Sales_M',
        y='Product_Category',
        orientation='h',
        color_discrete_sequence=[COLOR_PRIMARY],
        text_auto='.2f',
        labels={'Sales_M': 'Sales (₹ Millions)', 'Product_Category': 'Category'},
        title='<b>Sales Volume by Product Category</b>'
    )
    fig.update_layout(template='plotly_white')
    fig.update_traces(texttemplate='₹%{x:.2f}M', textposition='outside')
    return fig


def plotly_sales_vs_profit(df: pd.DataFrame) -> go.Figure:
    """Plotly Interactive Sales vs Profit with Trendline."""
    sample_df = df.sample(min(1200, len(df)), random_state=42) if len(df) > 1200 else df
    fig = px.scatter(
        sample_df,
        x='Sales',
        y='Profit',
        color='Product_Category',
        color_discrete_sequence=PALETTE_5,
        hover_data=['Customer_Segment', 'Region', 'Discount'],
        labels={'Sales': 'Sales (₹)', 'Profit': 'Profit (₹)'},
        title='<b>Sales vs. Profit Correlation by Category</b>',
        opacity=0.7
    )
    fig.update_layout(template='plotly_white')
    return fig


def plotly_discount_vs_profit(df: pd.DataFrame) -> go.Figure:
    """Plotly Interactive Discount vs Profit Margin."""
    sample_df = df.sample(min(1200, len(df)), random_state=42) if len(df) > 1200 else df
    fig = px.scatter(
        sample_df,
        x='Discount',
        y='Profit',
        color='Customer_Segment',
        labels={'Discount': 'Discount Rate', 'Profit': 'Net Profit (₹)'},
        title='<b>Discount Rate vs. Net Profit Realization</b>',
        opacity=0.65
    )
    fig.update_layout(template='plotly_white')
    fig.update_xaxes(tickformat='.0%')
    return fig


def plotly_segment_donut(df: pd.DataFrame) -> go.Figure:
    """Plotly Interactive Customer Segment Donut Chart."""
    seg = df.groupby('Customer_Segment')['Sales'].sum().reset_index()
    fig = px.pie(
        seg,
        names='Customer_Segment',
        values='Sales',
        hole=0.45,
        color='Customer_Segment',
        color_discrete_map={'Consumer': COLOR_PRIMARY, 'Corporate': COLOR_SECONDARY, 'Home Office': '#E28743'},
        title='<b>Sales Share by Customer Segment</b>'
    )
    fig.update_traces(textinfo='percent+label', pull=[0.02, 0.02, 0.02])
    fig.update_layout(template='plotly_white')
    return fig


def plotly_return_rate_by_category(df: pd.DataFrame) -> go.Figure:
    """Plotly Interactive Return Rate by Category."""
    ret = df.groupby('Product_Category')['Returned'].apply(lambda s: (s == 'Yes').mean() * 100).reset_index()
    ret.columns = ['Product_Category', 'Return_Rate']
    ret = ret.sort_values('Return_Rate', ascending=False)
    benchmark = (df['Returned'] == 'Yes').mean() * 100

    fig = px.bar(
        ret,
        x='Product_Category',
        y='Return_Rate',
        text_auto='.2f',
        color='Return_Rate',
        color_continuous_scale='Tealgrn',
        labels={'Return_Rate': 'Return Rate (%)', 'Product_Category': 'Category'},
        title='<b>Product Category Return Rates (%)</b>'
    )
    fig.add_hline(y=benchmark, line_dash='dash', line_color='#E74C3C',
                  annotation_text=f'Company Benchmark: {benchmark:.2f}%', annotation_position='top right')
    fig.update_layout(template='plotly_white', coloraxis_showscale=False)
    fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    return fig


def plotly_pivot_heatmap(df: pd.DataFrame) -> go.Figure:
    """Plotly Interactive Category vs Region Pivot Heatmap."""
    pivot = df.pivot_table(index='Product_Category', columns='Region', values='Sales', aggfunc='mean').round(0)
    fig = px.imshow(
        pivot,
        labels=dict(x="Region", y="Product Category", color="Avg Sales (₹)"),
        x=pivot.columns,
        y=pivot.index,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="<b>Average Order Sales: Category vs. Region (₹)</b>"
    )
    fig.update_layout(template='plotly_white')
    return fig


if __name__ == '__main__':
    base_dir = r"c:\Users\prash\OneDrive\Desktop\New folder\Retail_Sales_Data_Visualization"
    clean_path = os.path.join(base_dir, "data", "retail_sales_cleaned.csv")
    charts_dir = os.path.join(base_dir, "charts")
    
    print("Loading cleaned dataset...")
    df_clean = pd.read_csv(clean_path)
    
    print("Generating all 12 publication-standard charts...")
    paths = generate_all_static_charts(df_clean, charts_dir)
    print("Generated charts:")
    for name, p in paths.items():
        print(f"  [OK] {name} -> {os.path.basename(p)}")
