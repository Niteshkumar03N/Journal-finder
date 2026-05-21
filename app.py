import streamlit as st
import json

# =====================================
# IMPORT SCRAPERS
# =====================================

from search.springer_scraper import find_journals
from search.elsevier_scraper import search_elsevier
from search.taylor_scraper import search_taylor
from search.wiley_scraper import scrape_wiley_journals
from search.cwauthors_scraper import search_cwauthors

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Journal Finder",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* =====================================
   GLOBAL
===================================== */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background:
        linear-gradient(
            135deg,
            #f4f7ff 0%,
            #fdf4ff 50%,
            #f3fff7 100%
        ) !important;
    min-height: 100vh;
}

/* =====================================
   HIDE STREAMLIT DEFAULT
===================================== */

#MainMenu,
footer,
header {
    visibility: hidden;
}

/* =====================================
   MAIN CONTAINER
===================================== */

.block-container {
    padding-top: 2rem !important;
    padding-left: 4rem !important;
    padding-right: 4rem !important;
    max-width: 1400px !important;
}

/* =====================================
   TITLE
===================================== */

.main-title {

    font-family: 'DM Serif Display', serif !important;

    font-size: 5.5rem !important;

    font-weight: 400 !important;

    color: #1a1a2e !important;

    text-align: center !important;

    margin-bottom: 2rem !important;

    margin-top: .5rem !important;
}

/* =====================================
   SUBTITLE
===================================== */

.subtitle-tag {
    display: inline-block;
    font-size: 13px;
    letter-spacing: .15em;
    color: #7c6fb0;
    text-transform: uppercase;
    font-weight: 700;
    margin-left: 12px;
    vertical-align: middle;
}

/* =====================================
   SECTION LABEL
===================================== */

.section-label {

    font-size: 15px;

    letter-spacing: .14em;

    text-transform: uppercase;

    color: #2b2345;   /* darker color */

    font-weight: 800;

    margin-top: 22px;

    margin-bottom: 14px;
}

/* =====================================
   TEXTAREA
===================================== */
            
label[data-testid="stWidgetLabel"] p {

    font-size: 15px !important;

    font-weight: 800 !important;

    letter-spacing: .12em !important;

    color: #2b2345 !important;

    text-transform: uppercase !important;
}

.stTextArea textarea {

    background: #fff !important;

    border: 2px solid #d4c5f9 !important;

    border-radius: 18px !important;

    font-family: 'DM Sans', sans-serif !important;

    font-size: 16px !important;

    color: #1a1a2e !important;

    min-height: 260px !important;

    padding: 18px !important;

    box-shadow:
        0 4px 20px rgba(124,111,176,.10) !important;
}

.stTextArea textarea:focus {

    border-color: #8b5cf6 !important;

    box-shadow:
        0 0 0 4px rgba(139,92,246,.15) !important;
}

/* =====================================
   CHECKBOX CHIPS
===================================== */

div[data-testid="stCheckbox"] {

    padding: 10px 18px !important;

    border-radius: 999px !important;

    font-size: 14px !important;

    margin-bottom: 10px !important;
}

/* Springer */

div[data-testid="stCheckbox"]:nth-of-type(1) {

    background:
        linear-gradient(
            135deg,
            #e8f4fd,
            #c8e6ff
        );

    border: 1.5px solid #6db8f7;
}

/* Elsevier */

div[data-testid="stCheckbox"]:nth-of-type(2) {

    background:
        linear-gradient(
            135deg,
            #fde8f4,
            #ffc8e8
        );

    border: 1.5px solid #f76db8;
}

/* Taylor */

div[data-testid="stCheckbox"]:nth-of-type(3) {

    background:
        linear-gradient(
            135deg,
            #e8fdf0,
            #c8ffd8
        );

    border: 1.5px solid #6df7a0;
}

/* CW Authors */

div[data-testid="stCheckbox"]:nth-of-type(4) {

    background:
        linear-gradient(
            135deg,
            #fdf4e8,
            #ffe8c8
        );

    border: 1.5px solid #f7b46d;
}
            
/* Wiley */

div[data-testid="stCheckbox"]:nth-of-type(5) {

    background:
        linear-gradient(
            135deg,
            #eef2ff,
            #dbe4ff
        );

    border: 1.5px solid #7c8cff;
}

/* =====================================
   BUTTON
===================================== */

.stButton > button {

    width: 100%;

    height: 55px !important;

    background:
        linear-gradient(
            135deg,
            #6c63ff,
            #a855f7
        ) !important;

    color: white !important;

    border: none !important;

    border-radius: 14px !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    margin-top: 10px !important;

    box-shadow:
        0 6px 20px rgba(108,99,255,.25) !important;
}

.stButton > button:hover {

    opacity: .92 !important;
}

/* =====================================
   CODE BLOCK
===================================== */

.stCode,
pre {

    border-radius: 14px !important;

    border: 1px solid #ddd !important;
}

/* =====================================
   SUCCESS MESSAGE
===================================== */

.stSuccess {

    border-radius: 14px !important;
}

/* =====================================
   JOURNAL CARD
===================================== */

.journal-card {

    background: white;

    border-radius: 18px;

    padding: 22px;

    margin-bottom: 18px;

    border: 1px solid #ece7ff;

    box-shadow:
        0 4px 18px rgba(108,99,255,.06);
}

/* =====================================
   JOURNAL TITLE
===================================== */

.journal-title {

    font-family:
        'DM Serif Display',
        serif;

    font-size: 24px;

    color: #1a1a2e;

    margin-bottom: 14px;
}

/* =====================================
   META
===================================== */

.journal-meta {

    display: flex;

    flex-wrap: wrap;

    gap: 10px;

    margin-top: 10px;
}

/* =====================================
   BADGES
===================================== */

.badge {

    font-size: 13px;

    padding: 7px 14px;

    border-radius: 999px;

    font-weight: 600;
}

.badge-pub {

    background: #f0edff;

    color: #6c63ff;
}

.badge-if {

    background: #e8fff1;

    color: #0d6e34;
}

.badge-cs {

    background: #eef6ff;

    color: #1565c0;
}

.badge-oa {

    background: #fff4e8;

    color: #b85c00;
}

/* =====================================
   OPEN LINK
===================================== */

.open-link {

    display: inline-flex;

    align-items: center;

    gap: 5px;

    font-size: 14px;

    color: #6c63ff;

    font-weight: 700;

    text-decoration: none;

    padding: 8px 16px;

    border-radius: 10px;

    border: 1.5px solid #d4c5f9;

    background: #f7f5ff;

    float: right;
}

.open-link:hover {

    background: #ede8fb;
}

/* =====================================
   DIVIDER
===================================== */

.divider {

    height: 2px;

    background:
        linear-gradient(
            90deg,
            #d4c5f9,
            #c8f7d4,
            #c8e6ff
        );

    border-radius: 2px;

    margin: 1.5rem 0;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================

st.markdown("""
<h1 class="main-title">Journal Finder</h1>
""", unsafe_allow_html=True)

# =====================================
# ABSTRACT INPUT
# =====================================

abstract = st.text_area(
    "RESEARCH ABSTRACT",
    height=150,
    placeholder="Paste your abstract here...",
    label_visibility="visible"
)

# =====================================
# PUBLISHERS
# =====================================

st.markdown('<div class="section-label">Publishers</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    springer = st.checkbox("Springer", value=True)

with col2:
    elsevier = st.checkbox("Elsevier", value=True)

with col3:
    taylor = st.checkbox("Taylor & Francis", value=True)

with col4:
    cwauthors = st.checkbox("CW Authors", value=True)

with col5:
    wiley = st.checkbox("Wiley", value=True)

# =====================================
# SEARCH BUTTON
# =====================================

search = st.button("Find Journals ↗")

# =====================================
# SEARCH LOGIC
# =====================================

if search:

    if not abstract.strip():
        st.warning("Please enter an abstract.")

    else:
        all_results = []

        # =====================================
        # SPRINGER
        # =====================================

        if springer:

            with st.spinner("Searching..."):

                springer_results = find_journals(abstract)

                for item in springer_results:

                    formatted_result = {

                        "journal_name": item.get("title"),

                        "publisher": "Springer",

                        "impact_factor": item.get("impact_factor"),

                        "publishing_model": item.get("Publishing Model"),

                        "submission_to_first_decision":
                            item.get("submission_to_first_decision"),

                        "url": item.get("link"),

                        "downloads": item.get("Downloads")
                    }

                    all_results.append(formatted_result)

        # =====================================
        # Elsevier
        # =====================================

        if elsevier:

            with st.spinner("Searching..."):

                elsevier_results = search_elsevier(
                    abstract
                )

                for item in elsevier_results:

                    publishing_model = []

                    if item.get("Open access") == "Yes":

                        publishing_model.append(
                            "Open Access"
                        )

                    if item.get("subscription") == "Yes":

                        publishing_model.append(
                            "Subscription"
                        )

                    formatted_result = {

                        "journal_name":
                            item.get("title"),

                        "publisher":
                            "Elsevier",

                        "impact_factor":
                            item.get("impact_factor"),

                        "citescore":
                            item.get("CiteScore"),

                        "publishing_model":
                            ", ".join(
                                publishing_model
                            ),

                        "submission_to_first_decision":
                            item.get(
                                "submission_to_first_decision"
                            ),

                        "url":
                            item.get("link"),

                        "publication_charge":
                            item.get(
                                "publication_charge"
                            ),

                        "acceptance_to_publication":
                            item.get(
                                "Acceptance_to_publication"
                            )
                    }

                    all_results.append(
                        formatted_result
                    )

        # =====================================
        # Taylor & Francis
        # =====================================

        if taylor:
            with st.spinner("Searching..."):
                all_results.extend(search_taylor(abstract))


        # =====================================
        # CW Authors
        # =====================================

        if cwauthors:

            with st.spinner("Searching..."):

                cwauthors_results = search_cwauthors(abstract)

                for _, item in cwauthors_results.iterrows():

                    formatted_result = {

                        "journal_name": item.get("Title"),

                        "publisher": item.get("Publisher"),

                        "impact_factor": item.get("Impact Factor"),

                        "citescore": item.get("CiteScore"),

                        "url": item.get("Link")
                    }

                    all_results.append(formatted_result)


        # =====================================
        # Wiley
        # =====================================

        if wiley:
            with st.spinner("Searching..."):

                wiley_results = scrape_wiley_journals(abstract)

                for item in wiley_results:

                    formatted_result = {
                        "journal_name": item.get("Title"),
                        "publisher": "Wiley",
                        "impact_factor": item.get("Impact Factor"),
                        "publishing_model": item.get("Publication Charge"),
                        "submission_to_first_decision": item.get("Submission To First Decision"),
                        "url": item.get("Link"),
                        "citescore": item.get("Acceptance Rate")
                    }

                    all_results.append(formatted_result)



        # Download
        json_data = json.dumps(all_results, indent=2, ensure_ascii=False)
        st.download_button(
            label="⬇ Download Results JSON",
            data=json_data,
            file_name="journals.json",
            mime="application/json"
        )

        # Divider
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # =====================================
        # GROUP RESULTS BY PUBLISHER
        # =====================================

        publisher_groups = {}

        for result in all_results:

            publisher = result.get("publisher", "Other")

            if publisher not in publisher_groups:
                publisher_groups[publisher] = []

            publisher_groups[publisher].append(result)

        # =====================================
        # SHOW RESULTS
        # =====================================

        for publisher_name, publisher_results in publisher_groups.items():

            st.markdown(f"""
            <h2 style="
                margin-top:40px;
                margin-bottom:20px;
                color:#1a1a2e;
                font-size:32px;
                font-weight:700;
            ">
                {publisher_name}
            </h2>
            """, unsafe_allow_html=True)

            for result in publisher_results:

                # =====================================
                # BUILD BADGES
                # =====================================

                badges = ""

                if result.get("publisher"):

                    badges += (
                        f'<span class="badge badge-pub">'
                        f'{result["publisher"]}'
                        f'</span> '
                    )

                if result.get("impact_factor"):

                    badges += (
                        f'<span class="badge badge-if">'
                        f'Impact Factor {result["impact_factor"]}'
                        f'</span> '
                    )

                if result.get("citescore"):

                    badges += (
                        f'<span class="badge badge-cs">'
                        f'CiteScore {result["citescore"]}'
                        f'</span> '
                    )

                # =====================================
                # SPRINGER DOWNLOADS
                # =====================================

                if result.get("publisher") == "Springer":

                    if result.get("downloads"):

                        clean_downloads = str(
                            result["downloads"]
                        )

                        badges += (
                            f'<span class="badge badge-cs">'
                            f'Downloads {clean_downloads}'
                            f'</span> '
                        )

                # =====================================
                # PUBLISHING MODEL
                # =====================================

                if result.get("publishing_model"):

                    badges += (
                        f'<span class="badge badge-oa">'
                        f'{result["publishing_model"]}'
                        f'</span> '
                    )

                # =====================================
                # SUBMISSION TIME
                # =====================================

                if result.get("submission_to_first_decision"):

                    badges += (
                        f'<span class="badge badge-cs">'
                        f'Submission to First Decision: '
                        f'{result["submission_to_first_decision"]}'
                        f'</span> '
                    )

                # =====================================
                # APC
                # =====================================

                if result.get("publication_charge"):

                    badges += (
                        f'<span class="badge badge-oa">'
                        f'APC {result["publication_charge"]}'
                        f'</span> '
                    )

                # =====================================
                # ACCEPTANCE TO PUBLICATION
                # =====================================

                if result.get("acceptance_to_publication"):

                    badges += (
                        f'<span class="badge badge-cs">'
                        f'Acceptance to Publication '
                        f'{result["acceptance_to_publication"]}'
                        f'</span> '
                    )

                # =====================================
                # OPEN BUTTON
                # =====================================

                open_btn = (
                    f'<a class="open-link" '
                    f'href="{result["url"]}" '
                    f'target="_blank">'
                    f'↗ Open Journal'
                    f'</a>'
                )

                # =====================================
                # CARD UI
                # =====================================

                st.markdown(f"""
                <div class="journal-card">
                    {open_btn}
                    <div class="journal-title">
                        {result["journal_name"]}
                    </div>
                    <div class="journal-meta">
                        {badges}
                    </div>
                </div>
                """, unsafe_allow_html=True)