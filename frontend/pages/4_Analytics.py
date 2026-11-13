
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from theme import apply_theme


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="PersonaPulse | Analytics",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main page */

.stApp {
    background-color: #F5F7FC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Streamlit headings */

.stApp [data-testid="stHeading"] h1,
.stApp [data-testid="stHeading"] h2,
.stApp [data-testid="stHeading"] h3,
.stApp h1:not(.hero h1),
.stApp h2,
.stApp h3 {
    color: #172554 !important;
    font-weight: 750 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

.stApp [data-testid="stHeading"] {
    opacity: 1 !important;
    visibility: visible !important;
}

.stApp h2 {
    font-size: 26px !important;
}

.stApp h3 {
    font-size: 20px !important;
}

/* Hero banner */

.hero {
    background: linear-gradient(115deg, #172554, #4338CA);
    padding: 30px;
    border-radius: 18px;
    color: white !important;
    margin-bottom: 25px;
}

.hero h1 {
    color: white !important;
    font-size: 32px !important;
}

.hero p {
    color: #DBEAFE !important;
    font-size: 15px;
}

/* KPI cards */

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E2E8F0;
    padding: 19px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
}

[data-testid="stMetricValue"] {
    color: #172554 !important;
}

/* Tabs */

button[data-baseweb="tab"] {
    color: #334155 !important;
    font-weight: 700 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #4338CA !important;
}

/* Normal text */

.stMarkdown p,
.stCaption {
    color: #334155;
}

/* Insight cards */

.insight-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #6366F1;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: #334155 !important;
}

.insight-title {
    color: #172554 !important;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 6px;
}

</style>
""", unsafe_allow_html=True)

apply_theme()


# --------------------------------------------------
# CHART FORMATTING FUNCTION
# --------------------------------------------------

def show_chart(fig, height=390):

    fig.update_layout(
        height=height,
        font=dict(
            family="Arial",
            size=14,
            color="#334155"
        ),
        title_font=dict(
            size=19,
            color="#172554"
        ),
        margin=dict(
            l=45,
            r=30,
            t=65,
            b=65
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial"
        ),
        hovermode="closest"
    )

    fig.update_xaxes(
        showline=True,
        linecolor="#CBD5E1",
        gridcolor="#E2E8F0",
        tickfont=dict(
            size=12,
            color="#334155"
        )
    )

    fig.update_yaxes(
        showline=False,
        gridcolor="#E2E8F0",
        tickfont=dict(
            size=12,
            color="#334155"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "responsive": True
        }
    )


# --------------------------------------------------
# CHECK SIMULATION DATA
# --------------------------------------------------

if "simulation_results" not in st.session_state:
    st.warning(
        "No simulation results found. "
        "Please complete a simulation first."
    )

    if st.button("Go to Simulation"):
        st.switch_page("pages/3_Simulation.py")

    st.stop()


results = st.session_state["simulation_results"]

if not results:
    st.warning("Your simulation does not contain any results.")
    st.stop()


product = st.session_state.get("product", {})


# --------------------------------------------------
# NORMALISE RESULTS
# Supports both flattened results and nested persona data.
# --------------------------------------------------

records = []

for item in results:

    if "persona" in item and isinstance(item["persona"], dict):
        persona = item["persona"]
    else:
        persona = item

    record = {
        "ID": persona.get("id", ""),
        "Name": persona.get("name", "Unknown"),
        "Age": persona.get("age", 0),
        "Occupation": persona.get("occupation", "Unknown"),
        "Location": persona.get("location", "Unknown"),
        "Interests": ", ".join(persona.get("interests", []))
            if isinstance(persona.get("interests", []), list)
            else str(persona.get("interests", "")),

        "Sentiment": persona.get("sentiment", "Unknown"),

        "Purchase Intent": item.get(
            "purchase_intent",
            persona.get("purchase_likelihood", 0)
        ),

        "Product Appeal": item.get(
            "product_appeal",
            0
        ),

        "Price Acceptance": item.get(
            "price_acceptance",
            0
        ),

        "Recommendation Intent": item.get(
            "recommendation_intent",
            0
        ),

        "Usability Score": item.get(
            "usability_score",
            0
        ),

        "Purchase Motivation": persona.get(
            "purchase_motivation",
            "Not specified"
        ),

        "Purchase Barrier": persona.get(
            "purchase_barrier",
            "Not specified"
        ),

        "Purchase Frequency": persona.get(
            "purchase_frequency",
            "Not specified"
        ),

        "Preferred Channel": persona.get(
            "preferred_channel",
            "Not specified"
        ),

        "Price Sensitivity": persona.get(
            "price_sensitivity",
            "Not specified"
        ),

        "Budget": persona.get("budget", 0),

        "Customer Feedback": persona.get(
            "feedback",
            "No feedback available"
        )
    }

    response = item.get("response", {})
    record["Age"] = persona.get("age", 0)
    record["Location"] = persona.get("location", persona.get("location_type", "Unknown"))
    record["Product Appeal"] = response.get("interest_score", item.get("product_appeal", 0))
    record["Purchase Intent"] = response.get("purchase_intent", item.get("purchase_intent", 0))
    record["Price Acceptance"] = response.get("price_acceptance", item.get("price_acceptance", 0))
    record["Recommendation Intent"] = 100 if response.get("would_recommend") else 0
    record["Usability Score"] = response.get("perceived_usefulness", item.get("usability_score", 0))
    record["Sentiment"] = "Positive" if record["Purchase Intent"] >= 70 else "Neutral" if record["Purchase Intent"] >= 45 else "Negative"
    record["Customer Feedback"] = response.get("reasoning", persona.get("feedback", "No feedback available"))

    records.append(record)


df = pd.DataFrame(records)


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

numeric_columns = [
    "Age",
    "Purchase Intent",
    "Product Appeal",
    "Price Acceptance",
    "Recommendation Intent",
    "Usability Score",
    "Budget"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)

df["Purchase Intent"] = df["Purchase Intent"].clip(0, 100)

df["Product Appeal"] = df["Product Appeal"].clip(0, 100)

df["Price Acceptance"] = df["Price Acceptance"].clip(0, 100)

df["Recommendation Intent"] = df["Recommendation Intent"].clip(0, 100)

df["Usability Score"] = df["Usability Score"].clip(0, 100)


# --------------------------------------------------
# CALCULATE KEY METRICS
# --------------------------------------------------

total_customers = len(df)

average_purchase_intent = df["Purchase Intent"].mean()

average_product_appeal = df["Product Appeal"].mean()

average_price_acceptance = df["Price Acceptance"].mean()

average_recommendation = df["Recommendation Intent"].mean()

average_usability = df["Usability Score"].mean()

# Define outperformers as personas in the top 25%
# based on purchase intent.

outperformer_threshold = df["Purchase Intent"].quantile(0.75)

outperformers = df[
    df["Purchase Intent"] >= outperformer_threshold
]

outperformer_count = len(outperformers)

outperformer_percentage = (
    outperformer_count / total_customers * 100
    if total_customers > 0 else 0
)


# --------------------------------------------------
# PRODUCT AND BUSINESS ESTIMATES
# --------------------------------------------------

product_price = float(product.get("price", 0) or 0)

currency = product.get("currency", "₹")

# AOV proxy:
# Assumes one purchase of the submitted product.

aov_proxy = product_price

# Illustrative annual repeat-purchase assumptions.
# These are modelling assumptions, not observed transactions.

repeat_purchase_assumptions = {
    "Weekly": 12,
    "Monthly": 6,
    "Occasionally": 3,
    "Rarely": 1
}

frequency_counts = df["Purchase Frequency"].value_counts()

weighted_repeat_purchases = 0

for frequency, count in frequency_counts.items():

    assumed_purchases = repeat_purchase_assumptions.get(
        frequency,
        1
    )

    weighted_repeat_purchases += assumed_purchases * count

average_repeat_purchases = (
    weighted_repeat_purchases / total_customers
    if total_customers > 0 else 0
)

# Illustrative LTV proxy:
# Product price multiplied by assumed annual purchase frequency.

ltv_proxy = product_price * average_repeat_purchases

# Potential initial revenue under the simplifying assumption
# that every persona with purchase intent >= 50 converts.
# This is a scenario estimate, not a sales forecast.

potential_buyers = int(
    (df["Purchase Intent"] >= 50).sum()
)

potential_initial_revenue = potential_buyers * product_price


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

product_name = product.get(
    "name",
    "Your Product"
)

st.markdown(f"""
<div class="pp-hero">
    <div class="pp-eyebrow">04 · Decision signals</div>
    <h1>Read the response.</h1>
    <p>Explore synthetic audience feedback and product signals for <b>{product_name}</b>.</p>
    <p><span class="pp-pill">Synthetic responses</span><span class="pp-pill">Directional analysis</span></p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------

st.subheader("Executive Overview")

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Total Customers Evaluated",
    f"{total_customers:,}"
)

metric2.metric(
    "Average Purchase Intent",
    f"{average_purchase_intent:.1f}%"
)

metric3.metric(
    "Product Appeal",
    f"{average_product_appeal:.1f}%"
)

metric4.metric(
    "Outperformers",
    f"{outperformer_count:,}",
    f"{outperformer_percentage:.1f}% of personas"
)


metric5, metric6, metric7, metric8 = st.columns(4)

metric5.metric(
    "Price Acceptance",
    f"{average_price_acceptance:.1f}%"
)

metric6.metric(
    "Recommendation Intent",
    f"{average_recommendation:.1f}%"
)

metric7.metric(
    "Usability Score",
    f"{average_usability:.1f}%"
)

metric8.metric(
    "Potential Buyers",
    f"{potential_buyers:,}",
    "Purchase intent >= 50%"
)


st.caption(
    "These scores represent synthetic simulation outputs, "
    "not actual customer transactions or market survey results."
)


st.divider()


# --------------------------------------------------
# TABS
# --------------------------------------------------

overview_tab, audience_tab, behaviour_tab, business_tab = st.tabs([
    "📈 Overview",
    "👥 Audience Intelligence",
    "🛒 Purchase Behaviour",
    "💼 Business Insights"
])


# ==================================================
# TAB 1: OVERVIEW
# ==================================================

with overview_tab:

    st.subheader("Customer Evaluation Performance")

    col1, col2 = st.columns(2)

    with col1:

        score_data = pd.DataFrame({
            "Metric": [
                "Purchase Intent",
                "Product Appeal",
                "Price Acceptance",
                "Recommendation Intent",
                "Usability"
            ],

            "Score": [
                average_purchase_intent,
                average_product_appeal,
                average_price_acceptance,
                average_recommendation,
                average_usability
            ]
        })

        fig = px.bar(
            score_data,
            x="Metric",
            y="Score",
            color="Score",
            color_continuous_scale="Purples",
            title="Average Product Evaluation Scores",
            text_auto=".1f"
        )

        fig.update_yaxes(
            range=[0, 100],
            title="Average Score (%)"
        )

        fig.update_xaxes(
            title=""
        )

        show_chart(fig)

    with col2:

        sentiment_counts = df["Sentiment"].value_counts().reset_index()

        sentiment_counts.columns = [
            "Sentiment",
            "Customers"
        ]

        fig = px.pie(
            sentiment_counts,
            names="Sentiment",
            values="Customers",
            hole=0.48,
            title="Customer Sentiment Distribution"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        show_chart(fig)


    st.subheader("Purchase Intent Distribution")

    fig = px.histogram(
        df,
        x="Purchase Intent",
        nbins=12,
        title="How Purchase Intent Is Distributed Across Personas",
        labels={
            "Purchase Intent": "Purchase Intent (%)",
            "count": "Number of Personas"
        }
    )

    show_chart(fig)


    st.subheader("Individual Persona Performance")

    display_columns = [
        "Name",
        "Age",
        "Sentiment",
        "Purchase Intent",
        "Product Appeal",
        "Price Acceptance",
        "Recommendation Intent"
    ]

    st.dataframe(
        df[display_columns].sort_values(
            "Purchase Intent",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# TAB 2: AUDIENCE INTELLIGENCE
# ==================================================

with audience_tab:

    st.subheader("Who Is Your Target Audience?")

    col1, col2 = st.columns(2)

    with col1:

        age_bins = [0, 20, 30, 40, 50, 100]

        age_labels = [
            "Under 20",
            "20–29",
            "30–39",
            "40–49",
            "50+"
        ]

        df["Age Group"] = pd.cut(
            df["Age"],
            bins=age_bins,
            labels=age_labels,
            right=False
        )

        age_data = (
            df["Age Group"]
            .value_counts()
            .reindex(age_labels, fill_value=0)
            .reset_index()
        )

        age_data.columns = [
            "Age Group",
            "Customers"
        ]

        fig = px.bar(
            age_data,
            x="Age Group",
            y="Customers",
            title="Customer Distribution by Age",
            text="Customers"
        )

        show_chart(fig)

    with col2:

        location_data = (
            df["Location"]
            .value_counts()
            .reset_index()
        )

        location_data.columns = [
            "Location",
            "Customers"
        ]

        fig = px.bar(
            location_data,
            x="Location",
            y="Customers",
            title="Customer Distribution by Location",
            text="Customers"
        )

        show_chart(fig)


    st.subheader("Interest Analysis")

    interest_list = []

    for interests in df["Interests"].dropna():

        for interest in str(interests).split(","):

            interest = interest.strip()

            if interest:
                interest_list.append(interest)

    if interest_list:

        interest_data = (
            pd.Series(interest_list)
            .value_counts()
            .reset_index()
        )

        interest_data.columns = [
            "Interest",
            "Customers"
        ]

        fig = px.bar(
            interest_data,
            x="Interest",
            y="Customers",
            title="Most Common Customer Interests",
            text="Customers"
        )

        show_chart(fig)

    else:
        st.info("No customer interest information available.")


    st.subheader("Top Performing Audience Segments")

    segment_data = (
        df.groupby("Location", observed=False)
        .agg(
            Customers=("Name", "count"),
            Average_Purchase_Intent=("Purchase Intent", "mean"),
            Average_Product_Appeal=("Product Appeal", "mean")
        )
        .reset_index()
    )

    segment_data = segment_data.sort_values(
        "Average_Purchase_Intent",
        ascending=False
    )

    segment_data["Average_Purchase_Intent"] = (
        segment_data["Average_Purchase_Intent"].round(1)
    )

    segment_data["Average_Product_Appeal"] = (
        segment_data["Average_Product_Appeal"].round(1)
    )

    st.dataframe(
        segment_data,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "These are simulated audience segments. "
        "A larger real-world sample would be needed "
        "to establish reliable market-wide patterns."
    )


# ==================================================
# TAB 3: PURCHASE BEHAVIOUR
# ==================================================

with behaviour_tab:

    st.subheader("Understanding Customer Purchase Behaviour")

    col1, col2 = st.columns(2)

    with col1:

        motivation_data = (
            df["Purchase Motivation"]
            .value_counts()
            .reset_index()
        )

        motivation_data.columns = [
            "Motivation",
            "Customers"
        ]

        fig = px.bar(
            motivation_data,
            x="Customers",
            y="Motivation",
            orientation="h",
            title="What Motivates Customers to Buy?",
            text="Customers"
        )

        show_chart(fig)

    with col2:

        barrier_data = (
            df["Purchase Barrier"]
            .value_counts()
            .reset_index()
        )

        barrier_data.columns = [
            "Barrier",
            "Customers"
        ]

        fig = px.bar(
            barrier_data,
            x="Customers",
            y="Barrier",
            orientation="h",
            title="What Prevents Customers from Buying?",
            text="Customers"
        )

        show_chart(fig)


    st.subheader("Preferred Shopping Channels")

    channel_data = (
        df["Preferred Channel"]
        .value_counts()
        .reset_index()
    )

    channel_data.columns = [
        "Channel",
        "Customers"
    ]

    fig = px.pie(
        channel_data,
        names="Channel",
        values="Customers",
        hole=0.45,
        title="Where Customers Prefer to Shop"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    show_chart(fig)


    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Purchase Frequency")

        frequency_data = (
            df["Purchase Frequency"]
            .value_counts()
            .reset_index()
        )

        frequency_data.columns = [
            "Frequency",
            "Customers"
        ]

        fig = px.bar(
            frequency_data,
            x="Frequency",
            y="Customers",
            title="How Often Customers Shop",
            text="Customers"
        )

        show_chart(fig)

    with col2:

        st.subheader("Price Sensitivity")

        sensitivity_data = (
            df["Price Sensitivity"]
            .value_counts()
            .reset_index()
        )

        sensitivity_data.columns = [
            "Price Sensitivity",
            "Customers"
        ]

        fig = px.pie(
            sensitivity_data,
            names="Price Sensitivity",
            values="Customers",
            hole=0.45,
            title="Customer Sensitivity to Price"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        show_chart(fig)


    st.subheader("Purchase Intent by Price Sensitivity")

    sensitivity_performance = (
        df.groupby("Price Sensitivity")
        .agg(
            Customers=("Name", "count"),
            Average_Purchase_Intent=("Purchase Intent", "mean"),
            Average_Price_Acceptance=("Price Acceptance", "mean")
        )
        .reset_index()
    )

    fig = px.bar(
        sensitivity_performance,
        x="Price Sensitivity",
        y=[
            "Average_Purchase_Intent",
            "Average_Price_Acceptance"
        ],
        barmode="group",
        title="How Price Sensitivity Relates to Buying Intent",
        labels={
            "value": "Average Score (%)",
            "variable": "Metric"
        }
    )

    show_chart(fig)


# ==================================================
# TAB 4: BUSINESS INSIGHTS
# ==================================================

with business_tab:

    st.subheader("Business Performance Indicators")

    st.markdown("""
    The following business indicators are illustrative estimates
    calculated from the submitted product price and simulated
    customer behaviour. They are not actual sales or customer
    lifetime revenue.
    """)

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Average Order Value (AOV) Proxy",
            f"{currency} {aov_proxy:,.2f}"
        )

        st.caption(
            "Assumes one purchase of the submitted product. "
            "Actual AOV requires real order data."
        )

    with col2:

        st.metric(
            "Illustrative Customer Lifetime Value",
            f"{currency} {ltv_proxy:,.2f}"
        )

        st.caption(
            f"Assumes an average of {average_repeat_purchases:.1f} "
            "purchases per persona over the modelled period."
        )


    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Potential Initial Revenue",
            f"{currency} {potential_initial_revenue:,.2f}"
        )

        st.caption(
            f"Scenario estimate: {potential_buyers} personas "
            "with purchase intent of at least 50%, each making "
            "one purchase."
        )

    with col2:

        st.metric(
            "Average Assumed Repeat Purchases",
            f"{average_repeat_purchases:.1f}"
        )

        st.caption(
            "Based on synthetic purchase-frequency categories "
            "and the assumptions described below."
        )


    st.divider()

    st.subheader("Business Estimate Assumptions")

    assumptions = pd.DataFrame({
        "Purchase Frequency": [
            "Weekly",
            "Monthly",
            "Occasionally",
            "Rarely"
        ],

        "Assumed Purchases in Modelled Period": [
            12,
            6,
            3,
            1
        ]
    })

    st.dataframe(
        assumptions,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "These are simplified modelling assumptions for demonstration. "
        "They are not measured customer retention or repeat-purchase rates."
    )


    st.divider()

    st.subheader("Outperforming Personas")

    st.markdown(
        f"""
        Personas with purchase intent at or above
        **{outperformer_threshold:.1f}%** are classified as
        outperformers in this simulation.
        """
    )

    if not outperformers.empty:

        outperformer_display = outperformers[
            [
                "Name",
                "Age",
                "Location",
                "Interests",
                "Purchase Intent",
                "Price Acceptance",
                "Purchase Motivation"
            ]
        ].sort_values(
            "Purchase Intent",
            ascending=False
        )

        st.dataframe(
            outperformer_display,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No outperforming personas were identified.")


    st.divider()

    st.subheader("Customer-Level Evaluation Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

st.divider()

st.subheader("Export Simulation Results")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Complete Analytics as CSV",
    data=csv_data,
    file_name="personapulse_analytics.csv",
    mime="text/csv",
    use_container_width=False
)


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "← Back to Simulation",
        use_container_width=True
    ):
        st.switch_page("pages/3_Simulation.py")

with col2:

    if st.button(
        "Go to Product Submission",
        use_container_width=True
    ):
        st.switch_page("pages/1_Product_Submission.py")
