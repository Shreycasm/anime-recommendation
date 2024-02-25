import streamlit as st
import pandas as pd
import pickle
import numpy as np
import ast
import re



def load_anime_data():
    
    with open('./artifacts/anime_df.pkl', 'rb') as f:
        return pickle.load(f)
  

def clean_df(df):
    df['synopsis'] = df['synopsis'].str.replace(r'\s*\[Written by MAL Rewrite\]$', '', regex=True)
    df['synopsis'] = df['synopsis'].apply(lambda x: re.sub(r'[\n\r]', ' ', x) if pd.notnull(x) else x)
    df['genre'] = df['genre_x'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

    return df

def display_top_animes(df, anime_type, top_type):
    anime_list = []

    st.subheader(f"TOP 25 {top_type} - {anime_type}")

    if anime_type == 'All Animes':
        top_25 = df.sort_values(by='weighted_rating', ascending=False).head(25) if top_type == 'Highest Rated' else df.sort_values(by='no_of_user_watched', ascending=False).head(25)
    else:
        top_25 = df[df["type"] == anime_type].sort_values(by='weighted_rating', ascending=False).head(25) if top_type == 'Highest Rated' else df[df["type"] == anime_type].sort_values(by='no_of_user_watched', ascending=False).head(25)

    for rank, (index, row) in enumerate(top_25.iterrows(), start=1):
        container = st.container(border=True, height  = 450)

        with container:
            poster_col, info_col = st.columns([0.2, 0.8], gap="small")
            poster_col.image(row['img_url'], use_column_width=True)

            with info_col:
                title , button = st.columns(2)
                st.subheader(f"{rank}. {row['title']}")
                st.write(f"**:red[Rating:]** :grey[{np.round(row['weighted_rating'], 2)}]")
                st.write(f"**:red[Views:]** :grey[{np.round(row['no_of_user_watched'], 0)}]")
                genres = ', '.join(row['genre'])
                st.write(f"**:red[Genre:]** :grey[{genres}]")
                st.write(f'**:red[Type:]** :grey[{row["type"]}]')

                st.write(f'**:red[Synopsis:]**')
                synopsis_container = st.container(border=False,height= 150)
                with synopsis_container:                
                    st.caption(f':grey[{row["synopsis"]}]')

