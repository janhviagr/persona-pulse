import streamlit as st

st.set_page_config(page_title="Overview | PersonaPulse", page_icon=":material/home:", layout="wide")

st.markdown(
    """
    <section class="pp-hero">
      <div class="pp-hero-copy">
        <div class="pp-eyebrow">AI-powered consumer intelligence</div>
        <h1>Know who <span class="pp-highlight">your product</span> is for.</h1>
        <p>Explore how thoughtfully designed synthetic audiences might respond to your product before you invest in the next launch.</p>
        <div><span class="pp-pill">Persona discovery</span><span class="pp-pill">AI simulations</span><span class="pp-pill">Decision-ready insights</span></div>
      </div>
      <div class="pp-hero-art" aria-hidden="true">
        <div class="pp-orbit"></div>
        <div class="pp-node one"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="8" r="3.2"/><path d="M5.5 20c.5-3.5 2.7-5.3 6.5-5.3s6 1.8 6.5 5.3"/></svg></div>
        <div class="pp-node two"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 18 9 12l3 3 7-9"/><path d="M14 6h5v5"/></svg></div>
        <div class="pp-node center"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="2.2" fill="currentColor"/><circle cx="5" cy="6" r="1.4"/><circle cx="19" cy="7" r="1.4"/><circle cx="6" cy="18" r="1.4"/><circle cx="18" cy="18" r="1.4"/><path d="m6.3 7 4 3.5m7.4-2.8-4 3m-6.5 6.2 4-3.1m6.5 3.1-4-3"/></svg></div>
        <div class="pp-node three"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 19V5m0 14h16M8 15v-4m4 4V7m4 8V9"/></svg></div>
        <div class="pp-node four"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 3 4.5 7v5c0 4.5 3 7.5 7.5 9 4.5-1.5 7.5-4.5 7.5-9V7L12 3Z"/><path d="m9 12 2 2 4-4"/></svg></div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

if st.button("Start a Simulation →", type="primary", key="overview-start-simulation"):
    st.switch_page("pages/1_Product_Submission.py")

st.subheader("A focused workflow for product discovery")
st.caption("Move from a product concept to a clearer view of its audience in three considered steps.")
st.markdown(
    """
    <div class="pp-workflow-grid">
      <article class="pp-workflow-card">
        <div class="pp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"><path d="m3 7 9-4 9 4-9 4-9-4Z"/><path d="M3 7v10l9 4 9-4V7M12 11v10"/></svg></div>
        <span class="pp-step">01 · Define</span><h3>Product context</h3>
        <p>Set the product story, price, features, and audience you want to explore.</p><span class="pp-explore">Explore the product brief →</span>
      </article>
      <article class="pp-workflow-card">
        <div class="pp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="9" cy="8" r="3.2"/><path d="M3.5 20c.4-3.6 2.3-5.4 5.5-5.4s5.1 1.8 5.5 5.4M16 5.2a3 3 0 0 1 0 5.7m1 3.9c2.2.5 3.4 2.2 3.6 5.2"/></svg></div>
        <span class="pp-step">02 · Discover</span><h3>Audience profiles</h3>
        <p>Build a varied synthetic panel grounded in your target segments.</p><span class="pp-explore">Explore the audience →</span>
      </article>
      <article class="pp-workflow-card">
        <div class="pp-card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20h18M5 17V9m5 8V4m5 13v-5m5 5V7"/></svg></div>
        <span class="pp-step">03 · Learn</span><h3>Product signals</h3>
        <p>Review purchase intent, perceived value, and recurring feedback.</p><span class="pp-explore">Explore the insights →</span>
      </article>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("PersonaPulse uses simulated insights for exploration. They are not a substitute for customer research.")
