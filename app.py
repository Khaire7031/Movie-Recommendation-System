import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=6ffd2830d8c66af4df5a16e7f8414541&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


moviesData = pickle.load(open('movies.pkl','rb'))
movies_list = moviesData['title'].values
st.title('Movie Recommender System')
selected_movie_name = st.selectbox('How',movies_list)

similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movie_index = moviesData[moviesData['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = moviesData.iloc[i[0]]['movie_id']
        recommended_movies.append(moviesData.iloc[i[0]]['title'])
        # Fetch Poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    return recommended_movies,recommended_movies_poster

if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        cols[i].text(recommended_movie_names[i])
        cols[i].image(recommended_movie_posters[i])

print("End")
