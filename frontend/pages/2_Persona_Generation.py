
import streamlit as st

from ai_engine.personas import generate_personas
from theme import apply_theme, page_header

from components.persona_card import display_persona


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="PersonaPulse | Persona Generation",
    page_icon="👥",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1350px;
}

.stApp h1,
.stApp h2,
.stApp h3 {
    color: #172554 !important;
    font-weight: 750 !important;
}

.hero {
    background: linear-gradient(115deg, #172554, #4338CA);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white !important;
    font-size: 32px;
}

.hero p {
    color: #DBEAFE !important;
}

</style>
""", unsafe_allow_html=True)

apply_theme()


# --------------------------------------------------
# CHECK PRODUCT SUBMISSION
# --------------------------------------------------

if "product" not in st.session_state:

    st.warning(
        "Please submit a product before generating personas."
    )

    if st.button("Go to Product Submission"):
        st.switch_page("pages/1_Product_Submission.py")

    st.stop()


product = st.session_state["product"]


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

page_header("02 · Audience discovery", "Meet your synthetic panel.", "Explore a diverse set of audience profiles shaped around your product brief.")


# --------------------------------------------------
# PRODUCT SUMMARY
# --------------------------------------------------

st.subheader("Product brief")

col1, col2 = st.columns([2, 1])

with col1:

    st.markdown(f"### {product.get('name', 'Unnamed Product')}")

    st.write(
        product.get(
            "description",
            "No product description provided."
        )
    )

    st.write(
        f"**Category:** {product.get('category', 'Not specified')}"
    )

    features = product.get("features", [])

    if isinstance(features, str):
        features = [
            x.strip()
            for x in features.replace("\n", ",").split(",")
            if x.strip()
        ]

    if features:

        st.write("**Product Features:**")

        for feature in features:
            st.write(f"- {feature}")

with col2:

    st.metric(
        "Product Price",
        f"{product.get('currency', '₹')} "
        f"{float(product.get('price', 0) or 0):,.2f}"
    )

    st.metric(
        "Personas Requested",
        product.get("persona_count", 50)
    )


# --------------------------------------------------
# TARGET AUDIENCE
# --------------------------------------------------

st.divider()

st.subheader("Target Audience")

target_ages = product.get("target_audience", product.get("age_groups", []))

target_interests = product.get("interests", [])

if target_ages:
    st.write("**Selected Age Groups:**", ", ".join(target_ages))
else:
    st.write("**Selected Age Groups:** Not specified")

if target_interests:
    st.write("**Selected Interests:**", ", ".join(target_interests))
else:
    st.write("**Selected Interests:** Not specified")


# --------------------------------------------------
# GENERATE PERSONAS
# --------------------------------------------------

st.divider()

st.subheader("Build the panel")

st.write(
    "Create a balanced panel from your selected age groups and interests. Feedback appears after the AI evaluation."
)

if st.button(
    "Generate audience panel",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "Generating product-specific customer personas..."
    ):

        try:

            persona_count = int(
                product.get("persona_count", 50)
            )

            # IMPORTANT:
            # Pass the entire product dictionary.
            # The generator uses it to create product-specific feedback.

            audience_config = {
                "age_groups": [age.replace("–", "-") for age in product.get("target_audience", [])],
                "interests": product.get("interests", []),
            }
            personas = generate_personas(audience_config, persona_count, seed=42)
            for persona in personas:
                persona.update({
                    "location": persona.get("location_type", "Unknown"),
                    "income": persona.get("income_level", "Unknown"),
                    "budget": int(product.get("price", 0) or 0),
                    "purchase_likelihood": 0,
                    "sentiment": "Not evaluated",
                    "purchase_frequency": "Not evaluated",
                    "preferred_channel": "Not evaluated",
                    "purchase_motivation": persona.get("primary_motivation") or "Not specified",
                    "purchase_barrier": ", ".join(persona.get("purchase_constraints", [])) or "Not specified",
                    "feedback": "Complete the simulation to see this persona's product evaluation.",
                })

            st.session_state["personas"] = personas

            # Clear previous simulation results because
            # these personas belong to a new generation.

            st.session_state.pop(
                "simulation_results",
                None
            )

            st.session_state.pop(
                "simulation_metrics",
                None
            )
            st.session_state.pop("simulation_report", None)
            st.session_state.pop("simulation_failures", None)

            st.success(
                f"Successfully generated {len(personas)} synthetic personas!"
            )

        except Exception as e:

            st.error(
                f"Persona generation failed: {e}"
            )


# --------------------------------------------------
# DISPLAY GENERATED PERSONAS
# --------------------------------------------------

personas = st.session_state.get("personas", [])


if personas:

    st.divider()

    st.subheader(
        f"Generated Customer Personas ({len(personas)})"
    )

    st.write(
        "Explore each persona's profile, interests, "
        "purchase behaviour and product-specific feedback."
    )

    # Summary metrics

    positive = sum(
        1 for p in personas
        if p.get("sentiment") == "Positive"
    )

    neutral = sum(
        1 for p in personas
        if p.get("sentiment") == "Neutral"
    )

    negative = sum(
        1 for p in personas
        if p.get("sentiment") == "Negative"
    )

    avg_intent = sum(
        p.get("purchase_likelihood", 0)
        for p in personas
    ) / len(personas)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Personas", len(personas))
    col2.metric("Positive", positive if st.session_state.get("simulation_results") else "—")
    col3.metric("Neutral", neutral if st.session_state.get("simulation_results") else "—")
    col4.metric("Negative", negative if st.session_state.get("simulation_results") else "—")

    st.metric(
        "Average Purchase Likelihood",
        f"{avg_intent:.1f}%" if st.session_state.get("simulation_results") else "Not evaluated"
    )

    # Persona cards

    for persona in personas:

        display_persona(persona)

    # Navigation

    st.divider()

    st.subheader("Ready for Simulation?")

    st.write(
        "Next, evaluate how these synthetic customers "
        "respond to your product."
    )

    if st.button(
        "Continue to Product Simulation →",
        type="primary",
        use_container_width=True
    ):

        st.switch_page("pages/3_Simulation.py")


else:

    st.info(
        "No personas generated yet. Click "
        "'Generate Sample Personas' to get started."
    )


# --------------------------------------------------
# BACK NAVIGATION
# --------------------------------------------------

st.divider()

if st.button("← Back to Product Submission"):

    st.switch_page("pages/1_Product_Submission.py")
