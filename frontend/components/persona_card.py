
import streamlit as st


def display_persona(persona):

    with st.container(border=True):
        st.markdown(f"<div class='pp-eyebrow'>{persona.get('persona_id', 'SYNTHETIC PROFILE')}</div>", unsafe_allow_html=True)
        st.subheader(f"{persona.get('name', 'Anonymous')} · {persona.get('age', '—')}")
        st.caption(f"{persona.get('occupation', 'Unknown')}  ·  {persona.get('location', 'Unknown')}")
        st.markdown("**Interests**")
        interests = persona.get("interests", [])
        st.markdown("".join(f"<span class='pp-pill'>{interest}</span>" for interest in interests), unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.metric("Price sensitivity", f"{persona.get('price_sensitivity', 0):.0%}" if isinstance(persona.get("price_sensitivity"), (float, int)) else persona.get("price_sensitivity", "—"))
        col2.metric("Purchase intent", f"{persona.get('purchase_likelihood', 0)}%" if persona.get("sentiment") != "Not evaluated" else "Pending")
        st.caption(f"Motivation · {persona.get('purchase_motivation', 'Not specified')}")
        if persona.get("sentiment") != "Not evaluated":
            st.markdown(f"<span class='pp-pill'>{persona.get('sentiment', '')} response</span>", unsafe_allow_html=True)
        with st.expander("Profile notes"):
            st.write(persona.get("feedback", "Evaluation feedback will appear here."))
