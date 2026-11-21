"""
app.py - Retail Sales Analytics Dashboard
A modern, industry-standard business intelligence web application built with Streamlit and Plotly.
"""

import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Ensure src modules are resolvable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from src.metrics import format_currency, format_percentage, format_number
from src.analysis import (
    compute_comprehensive_kpis,
    analyze_monthly_trends,
    analyze_regional_performance,
    analyze_category_performance,
    analyze_customer_segments,
    analyze_category_region_pivot,
    compute_regression_metrics,
    generate_data_insights
)

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Corporate CSS: Navy Blue & Teal palette, clean cards, modern typography
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* KPI Card styling */
    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 25px;
    }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #1B365D;
        flex: 1;
        min-width: 180px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    .kpi-card.teal {
        border-left-color: #008080;
    }
    .kpi-card.blue {
        border-left-color: #2E86AB;
    }
    .kpi-card.coral {
        border-left-color: #D9534F;
    }
    .kpi-card.amber {
        border-left-color: #F18F01;
    }
    .kpi-title {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 4px;
    }
    
    /* Section Headings */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1B365D;
        margin-top: 20px;
        margin-bottom: 15px;
        padding-bottom: 6px;
        border-bottom: 2px solid #E2E8F0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Insight Callout Box */
    .insight-box {
        background-color: #F1F5F9;
        border-left: 4px solid #008080;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 0.88rem;
        color: #334155;
        line-height: 1.45;
    }
    .insight-title {
        font-weight: 700;
        color: #008080;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    csv_file = os.path.join(CURRENT_DIR, "data", "retail_sales_cleaned.csv")
    if not os.path.exists(csv_file):
        # Fallback to cleaning on the fly if needed
        from src.data_cleaning import load_raw_data, clean_retail_data
        raw_path = os.path.join(CURRENT_DIR, "data", "retail_customer_sales_dataset.csv")
        raw_df = load_raw_data(raw_path)
        clean_df, _ = clean_retail_data(raw_df)
        clean_df.to_csv(csv_file, index=False)
        return clean_df
    
    df = pd.read_csv(csv_file)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])
    return df

df_master = load_data()


# -----------------------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🎛️ **Dashboard Filters**")
st.sidebar.markdown("<small style='color: #64748B;'>Drill down across dimensions:</small>", unsafe_allow_html=True)

# 1. Year Filter
years_available = sorted(df_master['Year'].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("📅 Select Year", ["All Years"] + [str(y) for y in years_available], index=0)

# 2. Month Filter
months_order = ['All Months', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
selected_month = st.sidebar.selectbox("🗓️ Select Month", months_order, index=0)

# 3. Region Filter
regions_available = sorted(df_master['Region'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("🌍 Select Region", ["All Regions"] + regions_available, index=0)

# 4. Product Category Filter
categories_available = sorted(df_master['Product_Category'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("📦 Product Category", ["All Categories"] + categories_available, index=0)

# 5. Customer Segment Filter
segments_available = sorted(df_master['Customer_Segment'].dropna().unique().tolist())
selected_segment = st.sidebar.selectbox("👥 Customer Segment", ["All Segments"] + segments_available, index=0)

# Clear Filters Action
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("#### ℹ️ **Dataset Specs**")
st.sidebar.markdown(f"""
- **Total Transactions:** {len(df_master):,}
- **Unique Customers:** {df_master['Customer_ID'].nunique():,}
- **Time Horizon:** 2023 – 2024
- **Coverage:** 4 Indian Regions, 16 States
""")

# Apply Filtering Logic
df_filtered = df_master.copy()

if selected_year != "All Years":
    df_filtered = df_filtered[df_filtered['Year'] == int(selected_year)]

if selected_month != "All Months":
    df_filtered = df_filtered[df_filtered['Month_Name'] == selected_month]

if selected_region != "All Regions":
    df_filtered = df_filtered[df_filtered['Region'] == selected_region]

if selected_category != "All Categories":
    df_filtered = df_filtered[df_filtered['Product_Category'] == selected_category]

if selected_segment != "All Segments":
    df_filtered = df_filtered[df_filtered['Customer_Segment'] == selected_segment]

# Safety check for empty slice
if len(df_filtered) == 0:
    st.warning("⚠️ No records match the selected filter combination. Please broaden your selection.")
    st.stop()


# -----------------------------------------------------------------------------
# MAIN DASHBOARD HEADER
# -----------------------------------------------------------------------------
st.markdown("<h1 style='margin-bottom: 0px; color: #1B365D;'>Retail Sales Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.05rem; color: #64748B; margin-top: 4px; margin-bottom: 25px;'>Turning Retail Transaction Data into Actionable Business Insights</p>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# DYNAMIC KPI CARDS
# -----------------------------------------------------------------------------
kpi_data = compute_comprehensive_kpis(df_filtered)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Revenue</div>
        <div class="kpi-value">{format_currency(kpi_data['total_sales'])}</div>
        <div class="kpi-sub">Total: ₹{kpi_data['total_sales']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card teal">
        <div class="kpi-title">Total Net Profit</div>
        <div class="kpi-value">{format_currency(kpi_data['total_profit'])}</div>
        <div class="kpi-sub">Total: ₹{kpi_data['total_profit']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-title">Net Profit Margin</div>
        <div class="kpi-value">{format_percentage(kpi_data['profit_margin'])}</div>
        <div class="kpi-sub">Return on Sales</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card amber">
        <div class="kpi-title">Avg Order Value (AOV)</div>
        <div class="kpi-value">₹{kpi_data['aov']:,.0f}</div>
        <div class="kpi-sub">Basket size per checkout</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Secondary Operational KPI row
scol1, scol2, scol3, scol4 = st.columns(4)
with scol1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Orders Processed</div>
        <div class="kpi-value">{format_number(kpi_data['total_orders'])}</div>
        <div class="kpi-sub">Fulfilled Transactions</div>
    </div>
    """, unsafe_allow_html=True)

with scol2:
    st.markdown(f"""
    <div class="kpi-card teal">
        <div class="kpi-title">Active Customers</div>
        <div class="kpi-value">{format_number(kpi_data['unique_customers'])}</div>
        <div class="kpi-sub">Distinct buyer accounts</div>
    </div>
    """, unsafe_allow_html=True)

with scol3:
    st.markdown(f"""
    <div class="kpi-card coral">
        <div class="kpi-title">Merchandise Return Rate</div>
        <div class="kpi-value">{format_percentage(kpi_data['return_rate'])}</div>
        <div class="kpi-sub">{kpi_data['total_returns']} items returned</div>
    </div>
    """, unsafe_allow_html=True)

with scol4:
    st.markdown(f"""
    <div class="kpi-card amber">
        <div class="kpi-title">Customer Satisfaction</div>
        <div class="kpi-value">⭐ {kpi_data['avg_rating']:.2f} <span style='font-size: 1rem; color: #94A3B8;'>/ 5.0</span></div>
        <div class="kpi-sub">Mean survey rating</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TABBED SECTIONS FOR SEAMLESS EXECUTIVE NAVIGATION
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "📈 Section A: Sales Overview",
    "📦 Section B: Product Performance",
    "👥 Section C: Customer Analytics",
    "💰 Section D: Profitability Analysis",
    "🔄 Section E: Returns & Satisfaction",
    "📋 Raw / Filtered Data View"
])


# =============================================================================
# SECTION A: SALES OVERVIEW
# =============================================================================
with tabs[0]:
    st.markdown("<div class='section-header'>📊 Section A: Sales Trends & Regional Performance</div>", unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns([1.6, 1.0])
    
    with col_a1:
        # Monthly Sales Trend
        monthly_trend_data = df_filtered.groupby(['Year', 'Month', 'Month_Name'])['Sales'].sum().reset_index()
        monthly_trend_data['Sales_M'] = monthly_trend_data['Sales'] / 1e6
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_trend_data['Month_Name'] = pd.Categorical(monthly_trend_data['Month_Name'], categories=month_order, ordered=True)
        monthly_trend_data = monthly_trend_data.sort_values(['Year', 'Month'])

        fig_m = px.line(
            monthly_trend_data,
            x='Month_Name',
            y='Sales_M',
            color='Year',
            markers=True,
            color_discrete_map={2023: "#1B365D", 2024: "#008080"},
            labels={'Month_Name': 'Month', 'Sales_M': 'Sales (₹ in Millions)', 'Year': 'Calendar Year'},
            title='<b>Visualization 1: Monthly Sales Trend (2023 vs. 2024)</b>'
        )
        fig_m.update_layout(template='plotly_white', hovermode='x unified', height=400)
        st.plotly_chart(fig_m, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Executive Insight — Monthly Momentum</div>
            Monthly sales demonstrate steady performance across both years with peak purchasing observed in August/October matching festive inventory build-ups. Mid-year sales in June and July remained resilient above ₹3.3M per month.
        </div>
        """, unsafe_allow_html=True)

    with col_a2:
        # Sales by Region
        reg_data = df_filtered.groupby('Region')['Sales'].sum().reset_index()
        reg_data['Sales_M'] = reg_data['Sales'] / 1e6
        reg_data = reg_data.sort_values('Sales_M', ascending=False)

        fig_r = px.bar(
            reg_data,
            x='Region',
            y='Sales_M',
            color='Region',
            color_discrete_map={"East": "#2E86AB", "West": "#E28743", "South": "#008080", "North": "#1B365D"},
            labels={'Sales_M': 'Sales (₹ in Millions)', 'Region': 'Territory'},
            title='<b>Visualization 2: Total Sales by Region</b>',
            text_auto='.2f'
        )
        fig_r.update_layout(template='plotly_white', showlegend=False, height=400)
        fig_r.update_traces(texttemplate='₹%{y:.2f}M', textposition='outside')
        st.plotly_chart(fig_r, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Executive Insight — Territorial Share</div>
            Revenue is exceptionally well-distributed across India: East leads with ₹20.02M (26.1%), followed closely by West (₹19.76M), South (₹18.89M), and North (₹18.06M).
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# SECTION B: PRODUCT PERFORMANCE
# =============================================================================
with tabs[1]:
    st.markdown("<div class='section-header'>📦 Section B: Product Category Performance & Regional Cross-Tabs</div>", unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        cat_data = df_filtered.groupby('Product_Category')[['Sales', 'Profit']].sum().reset_index()
        cat_data['Sales_M'] = cat_data['Sales'] / 1e6
        cat_data['Profit_M'] = cat_data['Profit'] / 1e6
        cat_data = cat_data.sort_values('Sales_M', ascending=True)

        fig_c = px.bar(
            cat_data,
            x='Sales_M',
            y='Product_Category',
            orientation='h',
            color_discrete_sequence=['#1B365D'],
            labels={'Sales_M': 'Sales (₹ in Millions)', 'Product_Category': 'Category'},
            title='<b>Visualization 3: Revenue by Product Category</b>',
            text_auto='.2f'
        )
        fig_c.update_layout(template='plotly_white', height=380)
        fig_c.update_traces(texttemplate='₹%{x:.2f}M', textposition='outside')
        st.plotly_chart(fig_c, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Executive Insight — Category Dominance</div>
            Electronics (₹37.64M, 49.0%) and Furniture (₹26.06M, 34.0%) drive 83.0% of total revenue. Clothing, Grocery, and Office Supplies generate lower revenue but drive repeat transaction frequency.
        </div>
        """, unsafe_allow_html=True)

    with col_b2:
        # Category by Region Pivot Heatmap
        pivot_avg = df_filtered.pivot_table(index='Product_Category', columns='Region', values='Sales', aggfunc='mean').round(0)
        fig_p = px.imshow(
            pivot_avg,
            labels=dict(x="Region", y="Product Category", color="Avg Order (₹)"),
            x=pivot_avg.columns,
            y=pivot_avg.index,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Blues",
            title="<b>Visualization 11: Average Order Value by Category & Region (₹)</b>"
        )
        fig_p.update_layout(template='plotly_white', height=380)
        st.plotly_chart(fig_p, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Executive Insight — Ticket Size Symmetry</div>
            Furniture commands the highest average ticket size (₹25K–₹27K) across all four territories, with Electronics averaging ₹18K–₹20K. Pricing power remains remarkably steady nation-wide.
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# SECTION C: CUSTOMER ANALYTICS
# =============================================================================
with tabs[2]:
    st.markdown("<div class='section-header'>👥 Section C: Demographic Profile & Customer Segmentation</div>", unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = st.columns([1.1, 1.1, 1.0])
    
    with col_c1:
        # Age Distribution
        fig_age = px.histogram(
            df_filtered,
            x='Age',
            nbins=25,
            color_discrete_sequence=['#1B365D'],
            marginal='box',
            title='<b>Visualization 4: Customer Age Distribution</b>',
            labels={'Age': 'Age (Years)', 'count': 'Orders'}
        )
        fig_age.update_layout(template='plotly_white', height=380, showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Age Demographic Insight</div>
            Customer age is symmetrically distributed (skewness +0.27) around a median of 36.0 years, showing strong appeal among young to mid-career professionals.
        </div>
        """, unsafe_allow_html=True)

    with col_c2:
        # Income Distribution (clipped for clean view, noting outliers)
        inc_data = df_filtered[df_filtered['Income'] <= 250_000]
        fig_inc = px.histogram(
            inc_data,
            x='Income',
            nbins=25,
            color_discrete_sequence=['#008080'],
            marginal='box',
            title='<b>Visualization 5: Annual Income Distribution</b>',
            labels={'Income': 'Annual Income (₹)'}
        )
        fig_inc.update_layout(template='plotly_white', height=380, showlegend=False)
        fig_inc.update_xaxes(tickformat=',.0f')
        st.plotly_chart(fig_inc, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Income Skewness Insight</div>
            Annual income is strongly right-skewed (+17.5) with a median of ₹48,816 and an affluent tail extending to ₹1.75M, validating high-ticket luxury product viability.
        </div>
        """, unsafe_allow_html=True)

    with col_c3:
        # Segment Share Donut
        seg_data = df_filtered.groupby('Customer_Segment')['Sales'].sum().reset_index()
        fig_seg = px.pie(
            seg_data,
            names='Customer_Segment',
            values='Sales',
            hole=0.45,
            color='Customer_Segment',
            color_discrete_map={'Consumer': '#1B365D', 'Corporate': '#008080', 'Home Office': '#E28743'},
            title='<b>Visualization 9: Sales by Segment</b>'
        )
        fig_seg.update_traces(textinfo='percent+label')
        fig_seg.update_layout(template='plotly_white', height=380, showlegend=False)
        st.plotly_chart(fig_seg, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Segment Share Insight</div>
            Individual Consumers drive 54.4% of volume, Corporate clients represent 30.7%, and Home Office generates 14.9%, highlighting corporate account expansion potential.
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# SECTION D: PROFITABILITY ANALYSIS
# =============================================================================
with tabs[3]:
    st.markdown("<div class='section-header'>💰 Section D: Margin Drivers, Pricing Elasticity & Correlation</div>", unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns(2)
    
    sample_size = min(1500, len(df_filtered))
    df_sample = df_filtered.sample(sample_size, random_state=42) if len(df_filtered) > sample_size else df_filtered
    
    with col_d1:
        # Sales vs Profit
        fig_sp = px.scatter(
            df_sample,
            x='Sales',
            y='Profit',
            color='Product_Category',
            color_discrete_sequence=['#1B365D', '#008080', '#2E86AB', '#A23B72', '#F18F01'],
            trendline='ols',
            hover_data=['Customer_Segment', 'Region', 'Discount'],
            labels={'Sales': 'Order Sales (₹)', 'Profit': 'Realized Profit (₹)'},
            title='<b>Visualization 7: Sales vs. Profit Relationship (OLS Fit)</b>'
        )
        fig_sp.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig_sp, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Profit Linearity Insight</div>
            Sales and profit correlate almost perfectly (r = +0.965, R² = 0.931). Every additional ₹1,000 in gross revenue yields approximately ₹327 in net operating profit.
        </div>
        """, unsafe_allow_html=True)

    with col_d2:
        # Discount vs Profit
        fig_dp = px.scatter(
            df_sample,
            x='Discount',
            y='Profit',
            color='Customer_Segment',
            color_discrete_sequence=['#1B365D', '#008080', '#E28743'],
            trendline='ols',
            labels={'Discount': 'Discount Rate', 'Profit': 'Order Profit (₹)'},
            title='<b>Visualization 8: Discount Rate Impact on Profitability</b>'
        )
        fig_dp.update_layout(template='plotly_white', height=400)
        fig_dp.update_xaxes(tickformat='.0%')
        st.plotly_chart(fig_dp, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Discount Elasticity Warning</div>
            Discounting has a negative slope on profit. Orders discounted above 35% deliver significantly reduced net cash yields without driving proportionate volume increases.
        </div>
        """, unsafe_allow_html=True)

    # Correlation Matrix
    corr_cols = ['Sales', 'Profit', 'Discount', 'Quantity', 'Age', 'Income']
    corr_df = df_filtered[corr_cols].corr().round(3)
    fig_corr = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-0.3, zmax=1.0,
        title="<b>Visualization 10: Inter-Variable Correlation Matrix</b>"
    )
    fig_corr.update_layout(template='plotly_white', height=380)
    st.plotly_chart(fig_corr, use_container_width=True)


# =============================================================================
# SECTION E: RETURNS & SATISFACTION
# =============================================================================
with tabs[4]:
    st.markdown("<div class='section-header'>🔄 Section E: Merchandise Returns & Customer Satisfaction Audit</div>", unsafe_allow_html=True)
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        # Return Rate by Category
        ret_df = df_filtered.groupby('Product_Category')['Returned'].apply(lambda s: (s == 'Yes').mean() * 100).reset_index()
        ret_df.columns = ['Product_Category', 'Return_Rate']
        ret_df = ret_df.sort_values('Return_Rate', ascending=False)
        company_benchmark = (df_master['Returned'] == 'Yes').mean() * 100

        fig_ret = px.bar(
            ret_df,
            x='Product_Category',
            y='Return_Rate',
            color='Return_Rate',
            color_continuous_scale='Reds',
            text_auto='.2f',
            labels={'Return_Rate': 'Return Rate (%)', 'Product_Category': 'Category'},
            title='<b>Visualization 12: Return Rates by Product Category (%)</b>'
        )
        fig_ret.add_hline(y=company_benchmark, line_dash='dash', line_color='#1B365D',
                          annotation_text=f'Benchmark: {company_benchmark:.2f}%', annotation_position='top right')
        fig_ret.update_layout(template='plotly_white', height=380, coloraxis_showscale=False)
        fig_ret.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
        st.plotly_chart(fig_ret, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Return Rate Risk Factor</div>
            Clothing (13.50%) and Furniture (13.18%) register the highest return rates due to sizing and fit issues, while Office Supplies enjoys the lowest return rate at 11.49%.
        </div>
        """, unsafe_allow_html=True)

    with col_e2:
        # Satisfaction Level & Rating Breakdown
        sat_data = df_filtered['Satisfaction_Level'].value_counts().reset_index()
        sat_data.columns = ['Satisfaction_Level', 'Orders']
        sat_order = ['High', 'Medium', 'Low']
        sat_data['Satisfaction_Level'] = pd.Categorical(sat_data['Satisfaction_Level'], categories=sat_order, ordered=True)
        sat_data = sat_data.sort_values('Satisfaction_Level')

        fig_sat = px.bar(
            sat_data,
            x='Satisfaction_Level',
            y='Orders',
            color='Satisfaction_Level',
            color_discrete_map={'High': '#008080', 'Medium': '#2E86AB', 'Low': '#D9534F'},
            text_auto=True,
            title='<b>Customer Satisfaction Level Distribution</b>',
            labels={'Satisfaction_Level': 'Reported Satisfaction', 'Orders': 'Count'}
        )
        fig_sat.update_layout(template='plotly_white', height=380, showlegend=False)
        st.plotly_chart(fig_sat, use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title'>📌 Customer Sentiment Analysis</div>
            High and Medium satisfaction cohorts encompass over 70% of respondents, strongly aligning with customer ratings of 3.0 to 5.0 stars.
        </div>
        """, unsafe_allow_html=True)

    # Order Value Spread Boxplot
    fig_box = px.box(
        df_filtered,
        x='Product_Category',
        y='Sales',
        color='Product_Category',
        color_discrete_sequence=['#1B365D', '#008080', '#2E86AB', '#A23B72', '#F18F01'],
        labels={'Sales': 'Sales (₹)', 'Product_Category': 'Category'},
        title='<b>Visualization 6: Order Value Spread & Outlier Analysis</b>'
    )
    fig_box.update_layout(template='plotly_white', height=400, showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)


# =============================================================================
# DATA EXPORT & AUDIT TRAIL TAB
# =============================================================================
with tabs[5]:
    st.markdown("<div class='section-header'>📋 Filtered Dataset Inspection & Data Export</div>", unsafe_allow_html=True)
    st.markdown(f"**Viewing {len(df_filtered):,} filtered transactions out of {len(df_master):,} total cleaned records.**")

    # Data preview table
    st.dataframe(
        df_filtered[[
            'Transaction_ID', 'Customer_ID', 'Order_Date', 'Delivery_Date', 'Region', 'State',
            'Customer_Segment', 'Product_Category', 'Product', 'Quantity', 'Sales', 'Profit',
            'Profit_Margin', 'Discount', 'Returned', 'Satisfaction_Level', 'Customer_Rating'
        ]].head(200),
        use_container_width=True,
        height=380
    )

    # Download Buttons
    csv_bytes = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name=f"retail_sales_filtered_{selected_year}_{selected_region}.csv",
        mime="text/csv",
        use_container_width=True
    )
