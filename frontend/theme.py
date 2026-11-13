"""Shared visual system for PersonaPulse's Streamlit pages."""

import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        :root {
            --pp-bg: #F7F8FC;
            --pp-card: #FFFFFF;
            --pp-text: #171B32;
            --pp-muted: #64708A;
            --pp-primary: #2563EB;
            --pp-secondary: #60A5FA;
            --pp-cyan: #20BFD3;
            --pp-success: #16A58A;
            --pp-warning: #E9A23B;
            --pp-error: #E36B70;
            --pp-border: #E9EAF3;
            --pp-lavender: #EEF4FF;
        }
        html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
        .stApp { color: var(--pp-text); background: var(--pp-bg); }
        .block-container { max-width: 1320px; padding: 2.5rem 2.25rem 4rem !important; }
        h1, h2, h3, h4 { color: var(--pp-text); font-family: 'Space Grotesk', 'Segoe UI', sans-serif !important; letter-spacing: -.035em; }
        h1 { font-size: clamp(30px, 3.5vw, 36px) !important; line-height: 1.18 !important; font-weight: 700 !important; }
        h2 { font-size: 26px !important; font-weight: 650 !important; }
        h3 { font-size: 19px !important; font-weight: 650 !important; }
        p, label, .stCaption { color: var(--pp-muted); font-size: 15px; line-height: 1.65; }
        .stAppHeader, [data-testid="stHeader"] { background: rgba(247,248,252,.94) !important; border-bottom: 1px solid var(--pp-border); }
        [data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid var(--pp-border); }
        [data-testid="stSidebar"] > div:first-child { padding-top: 1.05rem; }
        [data-testid="stSidebarLogo"] { width:220px !important; max-width:100%; height:auto !important; margin:.25rem 0 .85rem; }
        .pp-brand { display:flex; align-items:center; gap:11px; padding: .3rem .2rem 1.3rem; }
        .pp-brand-mark { width:38px; height:38px; display:grid; place-items:center; border-radius:12px; background:#F1EFFF; color:var(--pp-primary); }
        .pp-brand-name { font:700 20px 'Space Grotesk',sans-serif; letter-spacing:-.04em; color:var(--pp-text); }
        .pp-brand-sub { font:600 9px 'Inter',sans-serif; letter-spacing:.13em; color:#8790A5; margin-top:3px; }
        [data-testid="stSidebarNav"] { padding-top:.25rem; }
        [data-testid="stSidebarNav"] li { margin:4px 0; }
        [data-testid="stSidebarNavLink"] { border-radius:10px; min-height:42px; padding:.55rem .7rem; transition:background .18s ease,color .18s ease; }
        [data-testid="stSidebarNavLink"]:hover { background:#F7F6FF; color:var(--pp-primary); }
        [data-testid="stSidebarNavLink"][aria-current="page"] { background:var(--pp-lavender); color:var(--pp-primary); font-weight:650; }
        [data-testid="stSidebarNavLink"][aria-current="page"] span { color:var(--pp-primary); }
        [data-testid="stSidebarNavLink"] svg { color:#8B7CF6; }
        [data-testid="stMetric"] { background:var(--pp-card); border:1px solid var(--pp-border); border-radius:14px; padding:1rem 1.1rem; box-shadow:0 3px 12px rgba(31,39,76,.035); }
        [data-testid="stMetricLabel"] { color:var(--pp-muted) !important; font-size:12px; font-weight:600; }
        [data-testid="stMetricValue"] { color:var(--pp-text) !important; font:600 25px 'Geist Mono',monospace; }
        .stButton > button, [data-testid="stFormSubmitButton"] > button { border-radius:9px; border:1px solid var(--pp-border); padding:.58rem 1rem; font-weight:600; transition:all .18s ease; }
        .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { transform:translateY(-1px); border-color:#CFC9FA; box-shadow:0 5px 14px rgba(102,84,232,.12); }
        [data-testid^="stBaseButton-primary"] { color:#FFFFFF !important; background:#2563EB !important; border-color:#2563EB !important; }
        [data-testid^="stBaseButton-primary"] *, [data-testid^="stBaseButton-primary"] p { color:#FFFFFF !important; }
        [data-testid^="stBaseButton-primary"]:hover { color:#FFFFFF !important; background:#1D4ED8 !important; border-color:#1D4ED8 !important; }
        [data-testid="stMultiSelect"] [data-tag] { background:#2563EB !important; color:#FFFFFF !important; }
        [data-testid="stMultiSelect"] [data-tag] * { color:#FFFFFF !important; }
        [data-testid="stSlider"] [data-orientation="horizontal"][style*="position: relative"] > div:first-child { background:#DDE7FB !important; background-image:none !important; }
        [data-testid="stSlider"] [data-orientation="horizontal"] > div[style*="left:"] { background:#2563EB !important; }
        [data-testid="stSliderThumbValue"], [data-testid="stSliderThumbValue"] p { border-color:#2563EB !important; color:#2563EB !important; }
        [data-testid="stTextInputRootElement"], [data-testid="stNumberInputRootElement"], [data-baseweb="select"], .stSelectbox [role="group"], .stMultiSelect [role="group"] { background:white !important; border:1px solid #DDE0EB !important; border-radius:9px !important; }
        .stApp input, .stApp textarea { background:white !important; color:var(--pp-text) !important; border-color:#DDE0EB !important; border-radius:9px !important; }
        [data-testid="stTextInputField"]::placeholder, textarea::placeholder { color:#8B93A7 !important; }
        .pp-cta { display:inline-flex; align-items:center; gap:10px; margin-top:.45rem; padding:.72rem 1.05rem; color:white !important; background:var(--pp-primary); border-radius:9px; text-decoration:none !important; font-size:14px; font-weight:650; box-shadow:0 5px 13px rgba(102,84,232,.19); transition:transform .18s ease,background .18s ease,box-shadow .18s ease; }
        .pp-cta:hover { color:white !important; background:#5745D5; transform:translateY(-1px); box-shadow:0 8px 18px rgba(102,84,232,.24); }
        [data-testid="stForm"] { background:white; border:1px solid var(--pp-border); border-radius:14px; padding:1.25rem 1.4rem; box-shadow:0 3px 12px rgba(31,39,76,.035); }
        [data-testid="stExpander"] { background:white; border:1px solid var(--pp-border); border-radius:12px; }
        hr { border-color:var(--pp-border); }

        .pp-eyebrow { color:var(--pp-primary); text-transform:uppercase; font:700 11px 'Inter',sans-serif; letter-spacing:.14em; margin:0 0 .65rem; }
        .pp-hero { position:relative; overflow:hidden; min-height:300px; display:grid; grid-template-columns:minmax(0,1.5fr) minmax(180px,.7fr); align-items:center; gap:1rem;
            border:1px solid #E7E5F4; border-radius:24px; padding:2.25rem 2.6rem; margin:.2rem 0 2.1rem;
            background:linear-gradient(112deg,#FFFFFF 0%,#FCFBFF 60%,#F0EEFF 100%); box-shadow:0 10px 30px rgba(39,44,92,.055); }
        .pp-hero h1 { margin:.1rem 0 .85rem; max-width:650px; }
        .pp-hero p { max-width:620px; margin:.15rem 0 .85rem; font-size:15px; }
        .pp-hero .pp-highlight { color:var(--pp-primary); }
        .pp-hero-art { position:relative; width:230px; height:190px; justify-self:center; }
        .pp-orbit { position:absolute; inset:14px 20px; border:1px solid #DCD8FC; border-radius:50%; transform:rotate(-23deg); }
        .pp-orbit:after { content:''; position:absolute; inset:19px 13px; border:1px dashed #D9D5F7; border-radius:50%; }
        .pp-node { position:absolute; width:43px; height:43px; display:grid; place-items:center; border:1px solid #E9E7F6; border-radius:14px; background:white; color:var(--pp-primary); box-shadow:0 7px 17px rgba(47,48,99,.09); }
        .pp-node svg { width:20px; height:20px; }
        .pp-node.center { width:58px; height:58px; left:86px; top:66px; color:white; border:0; background:var(--pp-primary); }
        .pp-node.one { left:20px; top:28px; }.pp-node.two { right:14px; top:34px; color:#20A8BC; }.pp-node.three { left:30px; bottom:13px; color:#20A8BC; }.pp-node.four { right:22px; bottom:17px; }
        .pp-pill { display:inline-flex; align-items:center; border-radius:999px; padding:.34rem .65rem; color:#6253C9; background:#F3F1FF; border:1px solid #E9E6FF; font-size:12px; font-weight:600; margin:0 .35rem .3rem 0; }
        .pp-workflow-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; margin:.9rem 0 1rem; }
        .pp-workflow-card { min-height:206px; display:flex; flex-direction:column; align-items:flex-start; padding:21px 22px 18px; background:white; border:1px solid var(--pp-border); border-radius:14px; box-shadow:0 4px 15px rgba(31,39,76,.04); transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease; }
        .pp-workflow-card:hover { transform:translateY(-4px); box-shadow:0 12px 24px rgba(44,43,94,.09); border-color:#D9D4FA; }
        .pp-card-icon { width:39px; height:39px; display:grid; place-items:center; border-radius:11px; background:#F1EFFF; color:var(--pp-primary); margin-bottom:16px; }
        .pp-card-icon svg { width:20px; height:20px; }
        .pp-step { color:var(--pp-primary); font:700 10px 'Inter',sans-serif; letter-spacing:.12em; text-transform:uppercase; }
        .pp-workflow-card h3 { margin:.55rem 0 .35rem; font-size:18px !important; }
        .pp-workflow-card p { margin:0; font-size:13px; line-height:1.55; }
        .pp-explore { margin-top:auto; padding-top:13px; color:var(--pp-primary); font-size:12px; font-weight:650; }
        @media (max-width:850px) { .pp-hero { grid-template-columns:1fr 180px; padding:1.8rem; } .pp-hero-art { transform:scale(.82); transform-origin:center; } }
        @media (max-width:700px) {
            .block-container { padding:1.2rem 1rem 3rem; }
            .pp-hero { display:block; min-height:0; padding:1.45rem; border-radius:18px; }
            .pp-hero-art { display:none; }
            .pp-workflow-grid { grid-template-columns:1fr; }
            .pp-workflow-card { min-height:0; }
            [data-testid="stHorizontalBlock"] { flex-direction:column !important; align-items:stretch !important; gap:.8rem !important; }
            [data-testid="stColumn"] { width:100% !important; flex:1 1 100% !important; min-width:100% !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(eyebrow: str, title: str, description: str) -> None:
    st.markdown(
        f'<div class="pp-eyebrow">{eyebrow}</div><h1>{title}</h1><p>{description}</p>',
        unsafe_allow_html=True,
    )
