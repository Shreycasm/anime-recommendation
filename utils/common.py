import streamlit as st
import pandas as pd
import pickle
import numpy as np
import ast
import re
import gzip




def load_anime_data():
    
    with open('./artifacts/anime_df.pkl', 'rb') as f:
        return pickle.load(f)

    

    

def clean_df(df):
    df['synopsis'] = df['synopsis'].str.replace(r'\s*\[Written by MAL Rewrite\]$', '', regex=True)
    df['synopsis'] = df['synopsis'].apply(lambda x: re.sub(r'[\n\r]', ' ', x) if pd.notnull(x) else x)
    df['genre'] = df['genre_x'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

    return df
