import streamlit as st
import pickle
import pandas as pd

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies['movie_id'] = movies['movie_id'].astype(int)
similarity = pickle.load(open('similarity.pkl', 'rb'))
poster_map = pickle.load(open('poster_map.pkl', 'rb'))  # ✅ Pre-saved posters

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster = poster_map.get(movie_id, "https://placehold.co/500x750?text=No+Poster")
        recommended_movies_posters.append(poster)

    return recommended_movies, recommended_movies_posters

# UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster, use_container_width=True)