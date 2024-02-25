import streamlit as st
import pandas as pd
import pickle
import numpy as np
from utils.common import load_anime_data, clean_df, similarity_matrix ,item_similarity



df = load_anime_data()
df = clean_df(df)
similarity_matrix_output = similarity_matrix()
item_similarity_output = item_similarity()

def search_titles_content_based(title):
    title_index = df[df["title"] == title].index[0]
    similarity_score = similarity_matrix_output[title_index]
    similar_title = sorted(list(enumerate(similarity_score)), key=lambda x: x[1], reverse=True)[1:11]

    df1 = pd.DataFrame(columns=df.columns)
    for i in similar_title:
        df1 = pd.concat([df1, df[df.index == i[0]]], axis=0)

    return df1

def search_titles_item_based(title):
    
    selected_anime_id = df[df["title"] == title]["anime_id"].values[0]   
    indexxx = item_similarity_output[selected_anime_id].sort_values(ascending=False).index[1:11]  
    recommended_anime_title =   df[df["anime_id"].isin(indexxx)]["title"]
    
    df2 = pd.DataFrame(columns=df.columns)
    for i in recommended_anime_title:
        df2 = pd.concat([df2, df[df.title == i]], axis=0)
    
    return df2
    

def content_based_recommendations(recommendations):
    for index, row in recommendations.iterrows():
        container = st.container(border=True, height=400)

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
                synopsis_container = st.container(border=False, height=80)
                with synopsis_container:
                    st.caption(f':grey[{row["synopsis"]}]')

            with button_col:
                button_identifier = f"{row['title']}_button1"
                if st.button(f"Recommend more like ***{row['title']}***", key=button_identifier):
                    st.session_state.selected_anime = row['title']
                    st.session_state.recommendations = search_titles_content_based(row['title'])
                    st.rerun()


def item_based_recommendations(recommendations):
    for index, row in recommendations.iterrows():
        container = st.container(border=True, height=400)

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
                synopsis_container = st.container(border=False, height=80)
                with synopsis_container:
                    st.caption(f':grey[{row["synopsis"]}]')

            with button_col:
                button_identifier = f"{row['title']}_button"
                if st.button(f"Recommend more like ***{row['title']}***.", key=button_identifier):
                    st.session_state.selected_anime = row['title']
                    st.session_state.recommendations = search_titles_item_based(row['title'])
                    st.rerun()