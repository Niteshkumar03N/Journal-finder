import streamlit as st
import json

# =====================================
# IMPORT SCRAPERS
# =====================================

from search.springer_scraper import (
    extract_keywords,
    search_springer
)

from search.elsevier_scraper import (
    search_elsevier
)

from search.taylor_scraper import (
    search_taylor
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Journal Finder",
    layout="wide"
)

# =====================================
# TITLE
# =====================================

st.title(
    "Journal Finder"
)

# =====================================
# ABSTRACT INPUT
# =====================================

abstract = st.text_area(
    "Enter Research Abstract",
    height=250,
    placeholder="Paste your abstract here..."
)

# =====================================
# PUBLISHERS
# =====================================

st.subheader(
    "Select Publishers"
)

col1, col2 = st.columns(2)

with col1:

    springer = st.checkbox(
        "Springer",
        value=True
    )

    taylor = st.checkbox(
        "Taylor & Francis",
        value=True
    )

with col2:

    elsevier = st.checkbox(
        "Elsevier",
        value=True
    )

# =====================================
# SEARCH BUTTON
# =====================================

search = st.button(
    "Find Journals"
)

# =====================================
# SEARCH
# =====================================

if search:

    if not abstract.strip():

        st.warning(
            "Please enter abstract"
        )

    else:

        all_results = []

        # =====================================
        # KEYWORDS
        # =====================================

        keywords = extract_keywords(
            abstract
        )

        st.subheader(
            "Extracted Keywords"
        )

        st.code(keywords)

        # =====================================
        # SPRINGER RESULTS
        # =====================================

        if springer:

            with st.spinner(
                "Searching Springer..."
            ):

                springer_results = (
                    search_springer(
                        keywords
                    )
                )

                all_results.extend(
                    springer_results
                )

        # =====================================
        # ELSEVIER RESULTS
        # =====================================

        if elsevier:

            with st.spinner(
                "Searching Elsevier..."
            ):

                for item in search_elsevier(
                    abstract
                ):

                    all_results.append(
                        item
                    )

        # =====================================
        # TAYLOR RESULTS
        # =====================================

        if taylor:

            with st.spinner(
                "Searching Taylor & Francis..."
            ):

                taylor_results = (
                    search_taylor(
                        abstract
                    )
                )

                all_results.extend(
                    taylor_results
                )

        # =====================================
        # SHOW COUNT
        # =====================================

        st.success(
            f"{len(all_results)} journals found"
        )

        # =====================================
        # DOWNLOAD JSON BUTTON
        # =====================================

        json_data = json.dumps(
            all_results,
            indent=2,
            ensure_ascii=False
        )

        st.download_button(
            label="Download Results JSON",
            data=json_data,
            file_name="journals.json",
            mime="application/json"
        )

        # =====================================
        # SHOW RESULTS
        # =====================================

        for result in all_results:

            with st.container(
                border=True
            ):

                st.subheader(
                    result["journal_name"]
                )

                col1, col2 = st.columns(2)

                # LEFT

                with col1:

                    if result.get(
                        "impact_factor"
                    ):

                        st.write(
                            f"Impact Factor: "
                            f"{result['impact_factor']}"
                        )

                    if result.get(
                        "citescore"
                    ):

                        st.write(
                            f"CiteScore: "
                            f"{result['citescore']}"
                        )

                    st.write(
                        f"Publishing Model: "
                        f"{result['publishing_model']}"
                    )

                # RIGHT

                with col2:

                    if result.get(
                        "submission_to_first_decision"
                    ):

                        st.write(
                            f"Submission to First Decision: "
                            f"{result['submission_to_first_decision']}"
                        )

                    st.write(
                        f"Publisher: "
                        f"{result['publisher']}"
                    )

                st.link_button(
                    "Open Journal",
                    result["url"]
                )