

# # =====================================
# # app.py
# # =====================================

# import streamlit as st

# from elsevier_scraper import (
#     search_elsevier
# )

# # =====================================
# # PAGE CONFIG
# # =====================================

# st.set_page_config(
#     page_title="Elsevier Journal Finder",
#     layout="wide"
# )

# # =====================================
# # TITLE
# # =====================================

# st.title(
#     "Elsevier Journal Finder"
# )

# st.write(
#     "Paste your abstract and find matching Elsevier journals"
# )

# # =====================================
# # INPUT
# # =====================================

# abstract = st.text_area(
#     "Enter Abstract",
#     height=250
# )

# # =====================================
# # OPEN ACCESS FILTER
# # =====================================

# open_access = st.checkbox(
#     "Open Access Only"
# )

# # =====================================
# # BUTTON
# # =====================================

# search = st.button(
#     "Find Journals"
# )

# # =====================================
# # SEARCH
# # =====================================

# if search:

#     if not abstract.strip():

#         st.warning(
#             "Please enter abstract"
#         )

#     else:

#         results_placeholder = (
#             st.empty()
#         )

#         all_results = []

#         # =====================================
#         # STREAM RESULTS
#         # =====================================

#         for item in search_elsevier(
#             abstract
#         ):

#             # OA FILTER

#             if open_access:

#                 if (
#                     item[
#                         "publishing_model"
#                     ]
#                     != "Open Access"
#                 ):

#                     continue

#             all_results.append(
#                 item
#             )

#             # =====================================
#             # LIVE RESULTS
#             # =====================================

#             with results_placeholder.container():

#                 st.success(
#                     f"{len(all_results)} journals found"
#                 )

#                 for result in all_results:

#                     with st.container(
#                         border=True
#                     ):

#                         st.subheader(
#                             result[
#                                 "journal_name"
#                             ]
#                         )

#                         col1, col2 = (
#                             st.columns(2)
#                         )

#                         # LEFT

#                         with col1:

#                             if result.get(
#                                 "impact_factor"
#                             ):

#                                 st.write(
#                                     f"Impact Factor: "
#                                     f"{result['impact_factor']}"
#                                 )

#                             if result.get(
#                                 "citescore"
#                             ):

#                                 st.write(
#                                     f"CiteScore: "
#                                     f"{result['citescore']}"
#                                 )

#                         # RIGHT

#                         with col2:

#                             if result.get(
#                                 "submission_to_first_decision"
#                             ):

#                                 st.write(
#                                     f"Submission to First Decision: "
#                                     f"{result['submission_to_first_decision']}"
#                                 )

#                             st.write(
#                                 f"Publishing Model: "
#                                 f"{result['publishing_model']}"
#                             )

#                             st.write(
#                                 f"Publisher: "
#                                 f"{result['publisher']}"
#                             )

#                         st.link_button(
#                             "Open Journal",
#                             result["url"]
#                         )






# # # =====================================
# # # main.py
# # # =====================================

# # import streamlit as st

# # # IMPORT SCRAPER FUNCTIONS

# # from springer_scraper import (
# #     extract_keywords,
# #     search_springer
# # )

# # # =====================================
# # # PAGE CONFIG
# # # =====================================

# # st.set_page_config(
# #     page_title="Unified Journal Finder",
# #     layout="wide"
# # )

# # # =====================================
# # # TITLE
# # # =====================================

# # st.title(
# #     "Unified Journal Finder"
# # )

# # st.write(
# #     "Paste your abstract and find matching journals"
# # )

# # # =====================================
# # # ABSTRACT INPUT
# # # =====================================

# # abstract = st.text_area(
# #     "Enter Research Abstract",
# #     height=250,
# #     placeholder="Paste your abstract here..."
# # )

# # # =====================================
# # # PUBLISHERS
# # # =====================================

# # st.subheader(
# #     "Select Publishers"
# # )

# # col1, col2, col3, col4, col5 = st.columns(5)

# # with col1:

# #     springer = st.checkbox(
# #         "Springer",
# #         value=True
# #     )

# # with col2:

# #     elsevier = st.checkbox(
# #         "Elsevier"
# #     )

# # with col3:

# #     wiley = st.checkbox(
# #         "Wiley"
# #     )

# # with col4:

# #     taylor = st.checkbox(
# #         "Taylor & Francis"
# #     )

# # with col5:

# #     mdpi = st.checkbox(
# #         "MDPI"
# #     )

# # # =====================================
# # # OPEN ACCESS
# # # =====================================

# # open_access = st.checkbox(
# #     "Open Access Only"
# # )

# # # =====================================
# # # SEARCH BUTTON
# # # =====================================

# # search = st.button(
# #     "Find Journals"
# # )

# # # =====================================
# # # SEARCH
# # # =====================================

# # if search:

# #     # =====================================
# #     # VALIDATION
# #     # =====================================

# #     if not abstract.strip():

# #         st.warning(
# #             "Please enter abstract"
# #         )

# #     else:

# #         # =====================================
# #         # KEYWORDS
# #         # =====================================

# #         keywords = extract_keywords(
# #             abstract
# #         )

# #         st.subheader(
# #             "Extracted Keywords"
# #         )

# #         st.code(keywords)

# #         # =====================================
# #         # SEARCHING
# #         # =====================================

# #         with st.spinner(
# #             "Searching journals..."
# #         ):

# #             results = []

# #             # CURRENTLY ONLY SPRINGER

# #             if springer:

# #                 springer_results = (
# #                     search_springer(
# #                         keywords
# #                     )
# #                 )

# #                 results.extend(
# #                     springer_results
# #                 )

# #         # =====================================
# #         # OPEN ACCESS FILTER
# #         # =====================================

# #         if open_access:

# #             filtered_results = []

# #             for item in results:

# #                 if (
# #                     item["publishing_model"]
# #                     == "Open Access"
# #                 ):

# #                     filtered_results.append(
# #                         item
# #                     )

# #             results = filtered_results

# #         # =====================================
# #         # RESULT COUNT
# #         # =====================================

# #         st.success(
# #             f"{len(results)} journals found"
# #         )

# #         # =====================================
# #         # NO RESULTS
# #         # =====================================

# #         if not results:

# #             st.error(
# #                 "No journals found"
# #             )

# #         else:

# #             # =====================================
# #             # SHOW RESULTS
# #             # =====================================

# #             for item in results:

# #                 with st.container(border=True):

# #                     st.subheader(
# #                         item["journal_name"]
# #                     )

# #                     col1, col2 = st.columns(2)

# #                     # LEFT COLUMN

# #                     with col1:

# #                         st.write(
# #                             f"Impact Factor: "
# #                             f"{item['impact_factor']}"
# #                         )

# #                         st.write(
# #                             f"Publishing Model: "
# #                             f"{item['publishing_model']}"
# #                         )

# #                     # RIGHT COLUMN

# #                     with col2:

# #                         st.write(
# #                             f"First Decision: "
# #                             f"{item['submission_to_first_decision']}"
# #                         )

# #                         st.write(
# #                             f"Publisher: "
# #                             f"{item['publisher']}"
# #                         )

# #                     # JOURNAL BUTTON

# #                     st.link_button(
# #                         "Open Journal",
# #                         item["url"]
# #                     )











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


# st.write(
#     "Paste your abstract and search journals from multiple publishers"
# )

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

with col2:

    elsevier = st.checkbox(
        "Elsevier",
        value=True
    )

# =====================================
# OPEN ACCESS
# =====================================

# open_access = st.checkbox(
#     "Open Access Only"
# )

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

        results_placeholder = st.empty()

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
        # OPEN ACCESS FILTER
        # =====================================

        # if open_access:

        #     filtered_results = []

        #     for item in all_results:

        #         if (
        #             item["publishing_model"]
        #             == "Open Access"
        #         ):

        #             filtered_results.append(
        #                 item
        #             )

        #     all_results = filtered_results

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