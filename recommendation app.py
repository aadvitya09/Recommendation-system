#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd

import pickle
import requests

def fetch_poster(movies_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=16c7d45cec535f026e7d9e94778bb583'.format(movies_id))
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data and data['poster_path'] is not None:
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    return None



def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies =[]
    recommended_movies_poster =[]
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster



# Load data using Pandas
movies_df = pd.read_pickle('movies.pkl')

# Extract titles from the DataFrame
movies  = movies_df['title'].values


similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movies Recommendation system")

selected_movie_name= st.selectbox(
    'which movie would you like to watch ?',
    movies
)



if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    for name, poster in zip(names, posters):
        if poster is not None:
            col1, col2, col3 , col4 ,col5 = st.columns(5)
            with col1:
                st.header(name)
                st.image(poster)






