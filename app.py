import streamlit as st
import pickle
import pandas as pd
import requests


# try:
#     response = requests.get("https://api.themoviedb.org/3/movie/10764?api_key=1df1226cb641a0772921bc2a41d7c2c2&language=en-US", timeout=50)
#     print(response.status_code)
#     print(response.json())
# except Exception as e:
#     print(f"Error: {e}")


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=1df1226cb641a0772921bc2a41d7c2c2&language=en-US"
    try:
        response = requests.get(url, timeout=10)  # 5 seconds timeout
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return None
    except requests.exceptions.Timeout:
        print(f"Timeout error for movie ID {movie_id}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        recommended_movies_poster.append(poster_url)
    return recommended_movies, recommended_movies_poster

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

st.title("🎬 Movie Recommender system")

selected_movie_name = st.selectbox("Select movie to get recommendations", movies_list)

if st.button("Show Recommendation"):
    recommended_movies, recommended_movies_poster = recommend(selected_movie_name)
    # col1, col2, col3, col4, col5 = st.columns(5)
    # print("Posters URLs:", recommended_movies_poster)

    cols = st.columns(5)
    # Fallback image url (you can replace with your own or a local file)
    fallback_image_url = "https://via.placeholder.com/300x450?text=No+Image"

    for i in range(5):
        with cols[i]:
            st.image(recommended_movies_poster[i]
                     if recommended_movies_poster[i] else fallback_image_url, use_container_width=True)

            # Show the title in a fixed height box to keep alignment
            st.markdown(
                f"""
                            <div style='text-align: center; height: 3em; overflow: hidden; font-weight: bold;'>
                                {recommended_movies[i]}
                            </div>
                            """,
                unsafe_allow_html=True
            )
else:
    st.write("No image to display")



#     with col1:
#         st.text(recommended_movies[0])
#         if recommended_movies_poster[0]:
#             st.image(recommended_movies_poster[0], use_container_width=True)
#         else:
#             st.image(fallback_image_url)
#     with col2:
#         st.text(recommended_movies[1])
#         if recommended_movies_poster[1]:
#             st.image(recommended_movies_poster[1], use_container_width=True)
#         else:
#             st.image(fallback_image_url)
#     with col3:
#         st.text(recommended_movies[2])
#         if recommended_movies_poster[2]:
#             st.image(recommended_movies_poster[2], use_container_width=True)
#         else:
#             st.image(fallback_image_url)
#     with col4:
#         st.text(recommended_movies[3])
#         if recommended_movies_poster[3]:
#             st.image(recommended_movies_poster[3], use_container_width=True)
#         else:
#             st.image(fallback_image_url)
#     with col5:
#         st.text(recommended_movies[4])
#         if recommended_movies_poster[4]:
#             st.image(recommended_movies_poster[4], use_container_width=True)
#         else:
#             st.image(fallback_image_url)
# else:
#     st.write("No image to display")
