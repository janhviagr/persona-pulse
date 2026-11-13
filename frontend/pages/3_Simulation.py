
import streamlit as st
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from ai_engine.agents import AgentFactory
from ai_engine.agents.agent_runner import run_agents
from ai_engine.evaluation import generate_report
from ai_engine.llm import GeminiProvider
from theme import apply_theme, page_header

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPOSITORY_ROOT / ".env")

st.set_page_config(
    page_title="PersonaPulse - Simulation",
    page_icon="🧪",
    layout="wide"
)

apply_theme()
page_header("03 · AI evaluation", "Test the product story.", "Your panel will evaluate relevance, purchase intent, perceived value, and recommendation likelihood.")

# Check whether product and personas exist
product = st.session_state.get("product")
personas = st.session_state.get("personas", [])

if not product or not personas:
    st.warning("Please submit a product and generate personas first.")
    if st.button("Go to Persona Generation"):
        st.switch_page("pages/2_Persona_Generation.py")
    st.stop()

with st.container(border=True):
    st.markdown("<div class='pp-eyebrow'>Product under evaluation</div>", unsafe_allow_html=True)
    st.subheader(product.get("name", "Unnamed Product"))
    st.caption(product.get("description", "No description"))
    st.markdown(f"<span class='pp-pill'>{product.get('category', 'Product')}</span><span class='pp-pill'>{product.get('currency', '')} {product.get('price', 0):,.2f}</span><span class='pp-pill'>{len(personas)} synthetic personas</span>", unsafe_allow_html=True)

st.subheader("Ready to run")
st.caption("Each persona is evaluated independently. Provider limits and panel size affect completion time.")

# Run simulation
if st.button("🚀 Start Simulation", type="primary"):

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Set GEMINI_API_KEY in the repository .env file, then restart Streamlit.")
        st.stop()

    progress = st.progress(0)
    status = st.empty()
    llm = GeminiProvider()
    agents = AgentFactory.create_agents(personas, llm)

    def on_progress(completed, failed, total):
        progress.progress(completed / total if total else 1.0)
        status.write(f"Evaluated {completed} of {total} personas ({failed} failed)...")

    try:
        with st.spinner("Running AI evaluations. Timing depends on panel size and provider limits."):
            responses = asyncio.run(run_agents(agents, product, on_progress=on_progress))
    except Exception as error:
        st.error(f"The simulation could not complete: {error}")
        st.stop()

    report = generate_report("streamlit-session", product, personas, responses)
    results = []
    for persona, response in zip(personas, responses):
        if response.get("status") == "ok":
            persona.update({
                "purchase_likelihood": response["purchase_intent"],
                "sentiment": "Positive" if response["purchase_intent"] >= 70 else "Neutral" if response["purchase_intent"] >= 45 else "Negative",
                "purchase_motivation": ", ".join(response.get("positive_factors", [])) or persona.get("primary_motivation", "Not specified"),
                "purchase_barrier": ", ".join(response.get("negative_factors", [])) or "Not specified",
                "feedback": response.get("reasoning", ""),
            })
            results.append({"persona": persona, "purchase_intent": response["purchase_intent"],
                "product_appeal": response["interest_score"], "price_acceptance": response["price_acceptance"],
                "recommendation_intent": 100 if response.get("would_recommend") else 0,
                "usability_score": response["perceived_usefulness"], "response": response})

    st.session_state["simulation_results"] = results
    st.session_state["simulation_report"] = report
    st.session_state["simulation_failures"] = [r for r in responses if r.get("status") != "ok"]

    status.success(f"Simulation completed: {len(results)} valid evaluations, {len(responses) - len(results)} failed.")
    st.rerun()


# Display results after simulation
results = st.session_state.get("simulation_results")

if results:

    st.divider()
    st.subheader("Simulation results")

    total = len(results)

    avg_purchase = sum(
        r["purchase_intent"] for r in results
    ) / total

    avg_appeal = sum(
        r["product_appeal"] for r in results
    ) / total

    avg_price = sum(
        r["price_acceptance"] for r in results
    ) / total

    avg_recommendation = sum(
        r["recommendation_intent"] for r in results
    ) / total

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Personas Evaluated", total)
    col2.metric("Purchase Intent", f"{avg_purchase:.1f}%")
    col3.metric("Product Appeal", f"{avg_appeal:.1f}%")
    col4.metric("Price Acceptance", f"{avg_price:.1f}%")

    st.metric("Recommendation intent", f"{avg_recommendation:.1f}%")
    failures = st.session_state.get("simulation_failures", [])
    if failures:
        st.warning(f"{len(failures)} of {len(personas)} evaluations could not be completed. The metrics below include successful evaluations only.")

    st.divider()
    st.subheader("Individual Persona Evaluations")

    for result in results:

        persona = result["persona"]

        with st.expander(
            f"{persona['name']} — "
            f"{result['purchase_intent']}% Purchase Intent"
        ):

            st.write(
                f"**Occupation:** {persona.get('occupation', 'N/A')}"
            )

            st.write(
                f"**Purchase Motivation:** "
                f"{persona.get('purchase_motivation', 'N/A')}"
            )

            st.write(
                f"**Purchase Barrier:** "
                f"{persona.get('purchase_barrier', 'N/A')}"
            )

            st.write(
                f"**Purchase Intent:** {result['purchase_intent']}%"
            )

            st.write(
                f"**Product Appeal:** {result['product_appeal']}%"
            )

            st.write(
                f"**Price Acceptance:** {result['price_acceptance']}%"
            )

            st.write(
                f"**Recommendation Intent:** "
                f"{result['recommendation_intent']}%"
            )

            st.write(
                f"**Usability Score:** {result['usability_score']}%"
            )

    st.divider()

    if st.button("📊 Continue to Analytics Dashboard", type="primary"):
        st.switch_page("pages/4_Analytics.py")
