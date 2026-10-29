import sys
from pathlib import Path

import streamlit as st

# Connect to the existing LangGraph workflow
SRC_DIR = Path(__file__).parent / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from langgraph_fact_checker import run_traced_fact_check


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Fact Checker",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Claim input label */
[data-testid="stWidgetLabel"] p {
    color: #EAF2FF !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* Text typed by the user */
.stTextArea textarea {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Placeholder text */
.stTextArea textarea::placeholder {
    color: #AFC4E5 !important;
    -webkit-text-fill-color: #AFC4E5 !important;
    opacity: 1 !important;
}

/* Text area background */
.stTextArea textarea {
    background-color: #0C1D32 !important;
    border: 1px solid #294568 !important;
}


/* ----------------------------------------
   FIX 1: Judge Confidence Text
---------------------------------------- */

/* Confidence label */
[data-testid="stMetricLabel"] p {
    color: #AFC4E5 !important;
    -webkit-text-fill-color: #AFC4E5 !important;
}

/* Confidence value (100%, etc.) */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] > div {
    color: #AFC4E5 !important;
    -webkit-text-fill-color: #AFC4E5 !important;
}


/* ----------------------------------------
   FIX 2: Agent Investigation Dropdowns
---------------------------------------- */

/* Default dropdown appearance */
[data-testid="stExpander"] details summary {
    background-color: #10233C !important;
    color: #AFC4E5 !important;
    border-radius: 8px;
}

/* Dropdown label text */
[data-testid="stExpander"] details summary p {
    color: #AFC4E5 !important;
    -webkit-text-fill-color: #AFC4E5 !important;
}

/* Hover effect */
[data-testid="stExpander"] details summary:hover {
    background-color: #172E4D !important;
    color: #AFC4E5 !important;
}

/* Keep text colour unchanged on hover */
[data-testid="stExpander"] details summary:hover p {
    color: #AFC4E5 !important;
    -webkit-text-fill-color: #AFC4E5 !important;
}

/* Keep text colour unchanged when expanded */
[data-testid="stExpander"] details[open] summary,
[data-testid="stExpander"] details[open] summary p {
    color: #AFC4E5 !important;
    -webkit-text-fill-color: #AFC4E5 !important;
}

/* Dropdown arrow */
[data-testid="stExpander"] details summary svg {
    fill: #AFC4E5 !important;
    color: #AFC4E5 !important;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 75% 0%,
            #172447 0%,
            transparent 42%
        ),
        linear-gradient(
            135deg,
            #07111f,
            #09182b 60%,
            #07111f
        );

    color: #edf4ff;
}

[data-testid="stHeader"] {
    background: rgba(7, 17, 31, 0.7);
}

/* Remove sidebar completely */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none;
}

.block-container {
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Main heading */
.hero {
    font-size: clamp(2.4rem, 5vw, 3.7rem);
    font-weight: 850;
    letter-spacing: -0.055em;
    line-height: 1.1;
    color: #f3f7ff;
    margin-bottom: 0.5rem;
}

.grad {
    background: linear-gradient(
        90deg,
        #4da2ff,
        #8c59ff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.muted {
    color: #a8bddb;
    line-height: 1.65;
}

/* Cards */
.panel {
    background: linear-gradient(
        145deg,
        rgba(15, 34, 58, 0.95),
        rgba(9, 24, 42, 0.97)
    );

    border: 1px solid #1d3658;
    border-radius: 15px;
    padding: 1.2rem 1.3rem;
    margin: 0.65rem 0 1.1rem;
}

.step {
    background: linear-gradient(
        145deg,
        rgba(15, 34, 58, 0.95),
        rgba(9, 24, 42, 0.97)
    );

    border: 1px solid #1d3658;
    border-radius: 14px;
    padding: 1.15rem;
    min-height: 190px;
    height: 100%;
}

.step-icon {
    font-size: 2rem;
    line-height: 1.3;
    margin-bottom: 0.75rem;
}

.step-title {
    font-weight: 750;
    color: #f1f6ff;
    font-size: 1.03rem;
}

.step-copy {
    color: #a8bddb;
    font-size: 0.91rem;
    line-height: 1.6;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #f1f6ff;
    margin-bottom: 0.4rem;
}

/* Verdict colours */
.verdict {
    display: inline-block;
    padding: 0.55rem 1rem;
    border-radius: 999px;
    font-size: 1.1rem;
    font-weight: 850;
    letter-spacing: 0.04em;
}

.vtrue {
    color: #36e2b4;
    background: #10382f;
    border: 1px solid #176e5c;
}

.vfalse {
    color: #ff557a;
    background: #391729;
    border: 1px solid #79243d;
}

.vuncertain {
    color: #ffc96a;
    background: #342a18;
    border: 1px solid #74521d;
}

/* Verify button */
div.stButton > button[kind="primary"] {
    background: linear-gradient(
        110deg,
        #4385ff,
        #633cff
    );

    color: white;
    border: 0;
    border-radius: 10px;
    min-height: 3.1rem;
    font-weight: 750;
}

div.stButton > button[kind="primary"]:hover {
    border: 1px solid #9cbbff;
    color: white;
}

/* Input */
.stTextArea textarea {
    background: #0c1d32 !important;
    color: #edf4ff !important;
    border: 1px solid #294568 !important;
    border-radius: 10px !important;
}

/* Confidence */
[data-testid="stMetric"] {
    background: #0d1f34;
    border: 1px solid #1d3658;
    padding: 0.8rem 1rem;
    border-radius: 12px;
}

a {
    color: #83aaff !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    """
    <div style="
        font-size:1.1rem;
        font-weight:800;
        color:#eaf2ff;
        margin-bottom:1.5rem;
    ">
        🔷 AI Fact Checker
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        Verify <span class="grad">Any Claim</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="muted" style="font-size:1.08rem">
        This multi-agent AI system researches, debates,
        and provides evidence-based fact-checks.
    </p>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

claim = st.text_area(
    "Enter a claim to fact-check",
    placeholder=(
        "Example: The Great Wall of China "
        "is visible from the Moon."
    ),
    height=110
)

run_clicked = st.button(
    "🔍 Verify Claim",
    type="primary",
    use_container_width=True
)


# ---------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------

st.write("")

st.markdown(
    '<div class="section-title">How It Works</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="muted">
        Your claim passes through three stages of investigation.
    </p>
    """,
    unsafe_allow_html=True
)

cols = st.columns(3, gap="medium")

steps = [
    (
        "⌕",
        "1. Claim Parser",
        "Extracts the main claim and creates search queries."
    ),
    (
        "⚒",
        "2. Defense & Prosecutor",
        "Searches for supporting and contradicting "
        "evidence in parallel."
    ),
    (
        "⚖",
        "3. Judge Agent",
        "Reviews the evidence and returns "
        "True, False, or Uncertain."
    )
]

for col, (icon, title, description) in zip(cols, steps):

    with col:
        st.markdown(
            f"""
            <div class="step">
                <div class="step-icon">{icon}</div>
                <div class="step-title">{title}</div>
                <p class="step-copy">{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------------------------
# RUN FACT-CHECKING WORKFLOW
# ---------------------------------------------------

if run_clicked:

    if not claim.strip():

        st.warning("Please enter a claim first.")

    else:

        try:

            with st.spinner(
                "The agents are investigating your claim. "
                "This may take a little while..."
            ):

                result = run_traced_fact_check(
                    claim.strip()
                )

            verdict_data = result.get(
                "final_verdict",
                {}
            )

            verdict = verdict_data.get(
                "verdict",
                "Uncertain"
            )

            confidence = float(
                verdict_data.get("confidence", 0.0)
            )

            confidence = max(
                0.0,
                min(1.0, confidence)
            )

            verdict_class = {
                "True": "vtrue",
                "False": "vfalse",
                "Uncertain": "vuncertain"
            }.get(verdict, "vuncertain")

            verdict_icon = {
                "True": "✓",
                "False": "×",
                "Uncertain": "?"
            }.get(verdict, "?")


            # ---------------------------------------
            # FINAL VERDICT
            # ---------------------------------------

            st.divider()

            st.markdown(
                '<div class="section-title">Investigation Results</div>',
                unsafe_allow_html=True
            )

            left, right = st.columns(2)

            with left:

                st.markdown(
                    f"""
                    <div class="verdict {verdict_class}">
                        {verdict_icon} &nbsp; {verdict.upper()}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with right:

                st.metric(
                    "Judge confidence (model estimate)",
                    f"{confidence:.0%}"
                )

                st.progress(confidence)


            # ---------------------------------------
            # CLAIM AND EXPLANATION
            # ---------------------------------------

            st.markdown("#### Claim")

            st.write(
                result.get(
                    "main_claim",
                    claim.strip()
                )
            )

            st.markdown("#### Explanation")

            st.write(
                verdict_data.get(
                    "explanation",
                    "No explanation was returned."
                )
            )


            # ---------------------------------------
            # SOURCES AND AGENT RESULTS
            # ---------------------------------------

            left_col, right_col = st.columns(
                [1.05, 0.95],
                gap="large"
            )

            with left_col:

                st.markdown("#### ↗ Key Sources")

                sources = verdict_data.get(
                    "key_sources",
                    []
                )

                if sources:

                    for i, source in enumerate(sources):

                        if (
                            isinstance(source, str)
                            and source.startswith(
                                ("https://", "http://")
                            )
                        ):

                            st.link_button(
                                f"Open source {i + 1}",
                                source
                            )

                        else:

                            st.write(source)

                else:

                    st.info(
                        "The Judge did not return any source links."
                    )


            with right_col:

                st.markdown(
                    "#### Agent Investigation Details"
                )

                with st.expander(
                    "🛡 Defense Agent",
                    expanded=True
                ):

                    st.json(
                        result.get(
                            "defense_result",
                            {}
                        )
                    )

                with st.expander(
                    "⚔ Prosecutor Agent",
                    expanded=True
                ):

                    st.json(
                        result.get(
                            "prosecutor_result",
                            {}
                        )
                    )


            # ---------------------------------------
            # FULL INVESTIGATION
            # ---------------------------------------

            with st.expander(
                "View full investigation result"
            ):

                st.json(result)

            st.caption(
                "AI-generated verdicts can be wrong. "
                "Review the evidence and original sources "
                "before relying on a result."
            )


        except Exception as exc:

            st.error(
                "The investigation failed. "
                "Check the terminal for details."
            )

            st.exception(exc)


# ---------------------------------------------------
# ABOUT THIS PROJECT
# ---------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-title">About This Project</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="panel">'
    '<p class="muted">'
    'Multi-Agent AI Fact Checker is a project forexploring agentic AI workflows, '
    'web search, structured outputs, parallel execution, '
    'and LLM observability.'
    '</p>'
    '<p class="muted">'
    '<b>Tech stack:</b> '
    'Python · Google Gemini API · LangGraph · '
    'LangSmith · Pydantic · Streamlit · '
    'DuckDuckGo Search'
    '</p>'
    '<p class="muted">'
    'This is an experimental tool. '
    'AI-generated verdicts may be incorrect. '
    '</p>'
    '</div>',
    unsafe_allow_html=True
)
