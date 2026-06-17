import streamlit as st
import joblib

from rank_companies import rank_companies, CATEGORY_MAP

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO



# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NiveshAI",
    layout="wide"
)

# ==========================================
# LOAD FILES
# ==========================================

mae_dict = joblib.load("mae_dict.pkl")

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
}

.top-card {
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 12px;
    padding: 20px;
    background-color: var(--secondary-background-color);
}

.card-title {
    font-size: 22px;
    font-weight: 700;
}

.card-text {
    font-size: 16px;
}
            
[data-testid="collapsedControl"] {
    transform: scale(2.5);
    background-color: rgba(22,163,74,0.15);
    border-radius: 10px;
    padding: 8px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<h1 style='text-align:center;'>
NiveshAI
</h1>

<h3 style='text-align:center; opacity:0.8;'>
AI-Powered Investment Intelligence for Indian Markets
</h3>

<p style='text-align:center; opacity:0.75; font-size:18px;'>
Discover High-Potential Investment Opportunities using Deep Learning, Confidence Scoring and Multi-Horizon Stock Forecasting.
</p>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## Investment Configuration")

    st.markdown(
        """Configure your investment preferences and identify the most promising opportunities."""
    )

    investment = st.number_input(
        "Investment Amount (₹)",
        min_value=1000,
        value=50000,
        step=1000,
        help="Amount you plan to invest."
    )

    category = st.selectbox(
        "Sector",
        list(CATEGORY_MAP.keys()),
        help="Choose a sector or select All Companies."
    )

    horizon = st.selectbox(
        "Investment Horizon",
        [
            "3M (3 Months)",
            "6M (6 Months)",
            "1Y (1 Year)",
            "2.5Y (2.5 Years)",
            "5Y (5 Years)"
        ],
        help="Forecast period for return prediction."
    )

    generate = st.button(
        "Generate Recommendations",
        use_container_width=True,
        type="primary"
    )

    st.caption(
        "Powered by Deep Learning models trained individually for each company."
    )

    horizon_map = {
    "3M (3 Months)": "3M",
    "6M (6 Months)": "6M",
    "1Y (1 Year)": "1Y",
    "2.5Y (2.5 Years)": "2.5Y",
    "5Y (5 Years)": "5Y"
    }

selected_horizon = horizon_map[horizon]

# ==========================================
# RECOMMENDATION DECORATOR
# ==========================================

def decorate_recommendation(rec):

    mapping = {
        "Strong Buy": "🟢 Strong Buy",
        "Buy": "🟩 Buy",
        "Hold": "🟨 Hold",
        "Sell": "🟧 Sell",
        "Strong Sell": "🔴 Strong Sell"
    }

    return mapping.get(rec, rec)

# ==========================================
# GENERATE RESULTS
# ==========================================

def create_pdf_report(df, category, horizon, investment):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "NiveshAI Investment Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Sector: {category}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Horizon: {horizon}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Investment Amount: {investment:,.0f}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    for _, row in df.iterrows():

        text = f"""
        <b>{row['Company']}</b><br/>
        Expected Return: {row['Expected Return (%)']}%<br/>
        Projected Value: {row['Projected Value ()']:,.0f}<br/>
        Confidence Score: {row['Confidence Score (%)']}%<br/>
        Recommendation: {row['Recommendation']}<br/>
        """

        elements.append(
            Paragraph(text, styles["BodyText"])
        )

        elements.append(
            Spacer(1, 10)
        )

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

if generate:

    with st.spinner("Analyzing market opportunities..."):

        result = rank_companies(
        category,
        selected_horizon,
        investment,
        mae_dict
        )

    # ======================================
    # KPI CARDS
    # ======================================

    st.subheader("Investment Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <b> Investment Amount</b>
        """, unsafe_allow_html=True)

        st.markdown(f"### {investment:,.0f}")

    with col2:
        st.markdown("""
        <b> Sector</b>
        """, unsafe_allow_html=True)

        st.markdown(category)

    with col3:
        st.markdown("""
        <b> Investment Period</b>
        """, unsafe_allow_html=True)

        st.markdown(f"### {horizon}")
        
    # ======================================
    # BEST OPPORTUNITY
    # ======================================

    best_company = result.iloc[0]

    st.markdown("""
    <h3>
    Top Recommendation
    </h3>
    """, unsafe_allow_html=True)

    st.success(
        f"""
    Company: {best_company['Company']}

    Expected Return: {best_company['Predicted Return (%)']}%

    Projected Value: {best_company['Future Value']:,.0f}

    Confidence Score: {best_company['Confidence (%)']}%
    """
    )

    st.divider()

    # ======================================
    # TOP 3 PICKS
    # ======================================

    st.markdown("""
    <h3>
    Top 3 Investment Opportunities
    </h3>
    """, unsafe_allow_html=True)

    top3 = result.head(3)

    cols = st.columns(3)

    for col, (_, row) in zip(cols, top3.iterrows()):

        with col:

            st.markdown(
                f"""
                <div class="top-card">

                <h3>{row['Company']}</h3>

                <p>
                <b>Expected Return:</b>
                {row['Predicted Return (%)']}%
                </p>

                <p>
                <b>Confidence:</b>
                {row['Confidence (%)']}%
                </p>

                <p>
                <b>Projected Value:</b>
                {row['Future Value']:,.0f}
                </p>

                <p>
                <b>Action:</b>
                {row['Recommendation']}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    # ======================================
    # TABLE
    # ======================================

    st.markdown("""
    <h3>
    Ranked Recommendations
    </h3>
    """, unsafe_allow_html=True)

    display_df = result.copy()

    display_df["Recommendation"] = (
        display_df["Recommendation"]
        .apply(decorate_recommendation)
    )

    # Hide internal ranking score
    display_df = display_df.drop(
        columns=["Score"]
    )

    # Better investor-friendly names
    display_df = display_df.rename(
        columns={
            "Predicted Return (%)":
                "Expected Return (%)",

            "Future Value":
                "Projected Value ()",

            "Confidence (%)":
                "Confidence Score (%)"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # DOWNLOAD PDF
    # ======================================

    pdf = create_pdf_report(
    display_df,
    category,
    horizon,
    investment
    )

    st.download_button(
        label="Download Investment Report (PDF)",
        data=pdf,
        file_name="Stock_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.divider()

    st.markdown("""
    <h3>
    Recommendation Methodology
    </h3>
    """, unsafe_allow_html=True)

    st.markdown("""
    Recommendations are ranked using:

    - Predicted Return Potential
    - Model Confidence Score
    - Risk-adjusted Ranking Score
    - Multi-Horizon Forecasting

    The system evaluates each company using its own trained deep learning model
    and identifies the most promising opportunities within the selected sector.
    """)

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:gray;">

    <b>NiveshAI • Financial Analytics Platform</b><br>

    Deep Learning Based Multi-Horizon Stock Recommendation Platform

    </div>
    """,
    unsafe_allow_html=True
)