import streamlit as st
import pandas as pd
import pickle
import numpy as np
import gzip
from utils.top import load_anime_data, clean_df

def similarity_matrix():
    #with open('./artifacts/similarity.pkl', 'rb') as f:
       # return pickle.load(f)
    filename = 'artifacts\similarity_.pkl'   
    with open(filename, 'rb') as gzipped_file:
        return pickle.load(gzipped_file)

df = load_anime_data()
df = clean_df(df)
similarity_matrix_output = similarity_matrix()

def search_titles(title):
    title_index = df[df["title"] == title].index[0]
    similarity_score = similarity_matrix_output[title_index]
    similar_title = sorted(list(enumerate(similarity_score)), key=lambda x: x[1], reverse=True)[1:10]

    df1 = pd.DataFrame(columns=df.columns)
    for i in similar_title:
        df1 = pd.concat([df1, df[df.index == i[0]]], axis=0)

    return df1

def display_anime_recommendations(recommendations):
    for index, row in recommendations.iterrows():
        container = st.container(border=True, height=450)

        with container:
            poster_col, info_col, button_col = st.columns([0.2, 0.6, 0.2], gap="small")
            poster_col.image(row['img_url'], use_column_width=True)

            with info_col:
                st.subheader(f"{row['title']}")
                st.write(f"**:red[Rating:]** :grey[{np.round(row['weighted_rating'], 2)}]")
                st.write(f"**:red[Views:]** :grey[{np.round(row['no_of_user_watched'], 0)}]")
                genres = ', '.join(row['genre'])
                st.write(f"**:red[Genre:]** :grey[{genres}]")
                st.write(f'**:red[Type:]** :grey[{row["type"]}]')

                st.write(f'**:red[Synopsis:]**')
                synopsis_container = st.container(border=False, height=150)
                with synopsis_container:
                    st.caption(f':grey[{row["synopsis"]}]')

            with button_col:
                button_identifier = f"{row['title']}_button"
                if st.button(f"Recommend more like ***{row['title']}***", key=button_identifier):
                    st.session_state.selected_anime = row['title']
                    st.session_state.recommendations = search_titles(row['title'])
                    st.rerun()

def main():
    st.header("Anime Recommendation System")

    tab1, tab2 = st.tabs(["RECOMMENDATIONS", "TOP ANIME"])

    with tab1:
        st.subheader("Anime Recommendations")
        selected_anime = st.selectbox("Select Anime Name", df["title"].astype(str).unique())
        if st.button("Recommend Similar Anime", key="general_recommend_button"):
            recommendations = search_titles(selected_anime)
            display_anime_recommendations(recommendations)

    with tab2:
        st.write("You can add any content for TOP ANIME tab here.")

if __name__ == "__main__":
    main()
