import streamlit as st
import pickle
import pandas as pd
import requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d763953d01d28d196eaaadbec2ae9c9c'

    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    headers = {
        "User-Agent": "MovieRecommender/1.0"
    }

    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Raises an HTTPError if the response was an error

    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


similarity = pickle.load(open("similarity.pkl",'rb'))
def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

movies_list = pickle.load(open('movie_dict.pkl','rb'))
movies= pd.DataFrame(movies_list)
st.title("Movie Recommender System")
option = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)
if st.button("Recommend"):
    names,poster=recommend(option)
    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
