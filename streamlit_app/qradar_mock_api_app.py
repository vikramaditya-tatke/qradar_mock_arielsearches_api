import streamlit as st
import requests
import polars as pl
from models import SearchRequest
from datetime import datetime

# --- Theme Configuration ---
st.set_page_config(
    layout="wide", page_title="QRadar Ariel Search", page_icon="🔍"  # Optional icon
)

st.markdown(
    """
    <style>
        /* Overall body style */
        body {
            background-color: #262730;
            color: white;
            font-family: 'Helvetica Neue', sans-serif;
        }
        /* Header and Title */
        .stApp > header {visibility: hidden;}
        .title {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            margin-top: 2em;
        }
        /* Search Form */
        .stTextArea textarea {background-color: #31333f; color: white; border: 1px solid #494c5c;}
        .stButton button {background-color: #007bff; color: white; border: none;}
        .stButton button:hover {background-color: #0056b3;}
        /* Results and History */
        .stDataFrame, .stTable {background-color: #31333f; color: white; border: 1px solid #494c5c;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Page Content ---

st.markdown('<div class="title">QRadar Ariel Search Mock</div>', unsafe_allow_html=True)


# --- Main Content ---

col1, col2 = st.columns([2, 1])  # Adjust as needed

# --- Search Area (Left Column) ---
with col1:
    with st.form("search_form"):
        query = st.text_area("Enter AQL Query:")
        submitted = st.form_submit_button("Search")

    if submitted:
        with st.spinner("Searching..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/searches",
                    json=SearchRequest(query_expression=query).dict(),
                    timeout=10  # Add timeout to handle long searches
                )
                response.raise_for_status()  # Raise exception for bad responses

                search_id = response.json()["search_id"]
                st.success(f"Search created with ID: {search_id}")

                result_response = requests.get(
                    f"http://127.0.0.1:8000/searches/{search_id}/results"
                )
                result_response.raise_for_status()

                results = result_response.json()
                df = pl.DataFrame(results["events"])
                st.subheader("Search Results:")
                st.dataframe(df)  # Display as interactive DataFrame

            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")

# --- Query History (Right Column) ---
with col2:
    st.subheader("Query History:")
    if "query_history" not in st.session_state:
        st.session_state.query_history = []  # Initialize with empty list

    for query, search_id, timestamp in st.session_state.query_history:
        st.markdown(
            f"_**{query}**_  &nbsp;&nbsp;&nbsp;&nbsp; _ID: {search_id}_  &nbsp;&nbsp;&nbsp;&nbsp; {timestamp}")  # Formatted display

    # Update history when a new search is submitted
    if submitted and response.status_code == 201:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # get current time
        st.session_state.query_history.append((query, search_id, timestamp))
