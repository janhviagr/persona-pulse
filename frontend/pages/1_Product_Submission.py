
import streamlit as st
from uuid import uuid4
from theme import apply_theme, page_header

st.set_page_config(
    page_title="Product Submission | PersonaPulse",
    page_icon="📦",
    layout="wide"
)

apply_theme()
page_header("01 · Product brief", "Set the context.", "Give your synthetic audience a clear product story and a focused market to explore.")

# PRODUCT SUBMISSION FORM

with st.form("product_submission_form"):

    st.subheader("Product details")
    st.caption("Start with the essentials. Specific descriptions tend to produce more useful feedback.")

    product_name = st.text_input(
        "Product Name",
        placeholder="Example: FitTrack Smartwatch"
    )

    description = st.text_area(
        "Product Description",
        placeholder="Describe what your product does..."
    )

    category = st.selectbox(
        "Product Category",
        [
            "Wearable Technology",
            "Electronics",
            "Fashion",
            "Food and Beverage",
            "Healthcare",
            "Fitness",
            "Other"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        price = st.number_input(
            "Product Price",
            min_value=0.0,
            value=4999.0,
            step=100.0
        )

    with col2:
        currency = st.selectbox(
            "Currency",
            ["INR", "USD", "EUR"]
        )

    features = st.text_area(
        "Key Product Features",
        placeholder="Enter one feature per line..."
    )

    st.divider()

    st.subheader("Who are you trying to reach?")

    audience = st.multiselect(
        "Select target age groups",
        ["18–24", "25–34", "35–44", "45–54", "55+"],
        default=["18–24", "25–34"]
    )

    interests = st.multiselect(
        "Select consumer interests",
        [
            "Fitness",
            "Technology",
            "Fashion",
            "Health",
            "Lifestyle",
            "Budget Shopping"
        ]
    )

    st.divider()

    st.subheader("Panel size")

    persona_count = st.slider(
        "Number of synthetic personas",
        min_value=10,
        max_value=100,
        value=50,
        step=10
    )

    st.caption("Larger panels require more AI evaluations and may take longer to complete.")

    submitted = st.form_submit_button(
        "Submit Product",
        type="primary",
        use_container_width=True
    )


# PROCESS FORM SUBMISSION

if submitted:

    if not product_name.strip():
        st.error("Please enter a product name.")

    elif not description.strip():
        st.error("Please enter a product description.")

    elif not audience:
        st.error("Please select at least one target age group.")

    else:

        product = {
            "product_id": f"streamlit-{uuid4().hex[:12]}",
            "name": product_name,
            "description": description,
            "category": category,
            "price": price,
            "currency": currency,
            "features": [
                f.strip()
                for f in features.split("\n")
                if f.strip()
            ],
            "target_audience": audience,
            "interests": interests,
            "persona_count": persona_count
        }

        st.session_state["product"] = product

        # Clear previously generated personas
        st.session_state.pop("personas", None)

        st.success("Product submitted successfully!")


# DISPLAY SUBMITTED PRODUCT

if "product" in st.session_state:

    product = st.session_state["product"]

    st.divider()

    with st.container(border=True):
        st.markdown("<div class='pp-eyebrow'>Brief saved</div>", unsafe_allow_html=True)
        st.subheader(product["name"])
        st.caption(product["description"])
        col1, col2, col3 = st.columns(3)
        col1.metric("Category", product["category"])
        col2.metric("Price", f"{product['currency']} {product['price']:,.2f}")
        col3.metric("Panel size", f"{product['persona_count']} personas")
        st.markdown("**Audience**")
        st.write(" · ".join(product["target_audience"]))
        st.markdown("**Key features**")
        st.write(" · ".join(product["features"]) or "No features added")

    st.divider()

    if st.button(
        "Build the audience →",
        type="primary",
        use_container_width=True
    ):
        st.switch_page("pages/2_Persona_Generation.py")
