import streamlit as st
import pandas as pd
from utils.common import load_anime_data, clean_df
from utils.recommendation import similarity_matrix, content_based_recommendations, search_titles_content_based, search_titles_item_based, item_based_recommendations
from utils.top import display_top_animes

st.set_page_config(layout="wide", page_title="Anime Recommendation System")

col1, col2, col3, col4, col5 = st.columns([0.15, 0.15, 0.22, 0.15, 0.15])
st.markdown("<h1 style='color: white; text-align: center;'>ANIME RECOMMENDATION SYSTEM</h1>", unsafe_allow_html=True)

df = load_anime_data()
df = clean_df(df)
similarity_matrix_output = similarity_matrix()

tab1, tab2 = st.tabs(["RECOMMENDATIONS","TOP ANIME"])

with tab1:
    col, _, _ = st.columns([0.5, 0.3, 0.2])

    if "selected_anime" not in st.session_state:
        st.session_state.selected_anime = df["title"].astype(str).iloc[0]

    selected_anime_index = df[df["title"] == st.session_state.selected_anime].index[0] if not df[df["title"] == st.session_state.selected_anime].empty else 0
    selected_anime = col.selectbox("Enter Anime Name", df["title"].astype(str).unique(), index=int(selected_anime_index))


    col1, col2 = st.columns(2)
    tab_selection  = st.radio(" ", ["Similar Content Anime", f"People who watched {selected_anime} also watched..."], horizontal = True)

    if tab_selection == "Similar Content Anime":
        # Display content-based recommendations
        st.session_state.selected_anime = selected_anime
        st.session_state.recommendations = search_titles_content_based(selected_anime)
        content_based_recommendations(st.session_state.recommendations)

    elif tab_selection == f"People who watched {selected_anime} also watched...":
        # Display item-based recommendations
        st.session_state.selected_anime = selected_anime
        st.session_state.recommendations_item = search_titles_item_based(selected_anime)
        item_based_recommendations(st.session_state.recommendations_item)


    with tab2:
        col1, col2, col3 = st.columns([0.3, 0.3, 0.6])

        anime_type = col2.selectbox("Select Anime type", ["All Animes", "TV", "OVA", "Movie", "Special"])
        top_type = col1.selectbox("Select top", ['Highest Rated', 'Most Watched'])
        st.divider()

        display_top_animes(df, anime_type, top_type)
