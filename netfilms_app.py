import streamlit as st
from clean_dataframe import clean_dataframe
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import fuzz
from nltk.sentiment import SentimentIntensityAnalyzer
from PIL import Image, UnidentifiedImageError
import requests
import pandas as pd
import base64
import io

# Set the default layout to wide mode
st.set_page_config(layout="wide")

# Load the cleaned dataframe
df_full = clean_dataframe()

@st.cache_data
def get_image_url(poster_path, size='w500'):
    base_url = 'https://image.tmdb.org/t/p'
    return f'{base_url}/{size}/{poster_path}'

@st.cache_data
def display_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            st.image(image, use_column_width=True)
        else:
            st.write("Image not available")
    except (UnidentifiedImageError, requests.exceptions.RequestException):
        st.write("Image not available")

def page_2(df_full):
    st.title("Recommandations de films")

    # Get film name from user input
    film_name = st.text_input("Entrez le nom d'un film:", key="film_input")

    if not film_name:
        # Film name not entered, return without displaying recommendations
        return

    if st.session_state.film_input:
        # Look up attributes from df_full based on film name
        matching_films = df_full[df_full['originalTitle'].apply(
            lambda x: fuzz.partial_ratio(x.lower(), film_name.lower())) > 90]

        if matching_films.empty:
            st.write(
                "Oups, nous n'avons pas pu trouver ce film dans notre base. Veuillez essayer un autre.")
            return

        input_film_attributes = matching_films.iloc[0]

        # Calculate sentiment score for the input film overview
        sid = SentimentIntensityAnalyzer()
        input_film_sentiment = sid.polarity_scores(
            input_film_attributes['overview'])['compound']

        input_film = {
            'poster_path': input_film_attributes['poster_path'],
            'genres_combined': input_film_attributes['genres_combined'],
            'popularity': input_film_attributes['popularity'],
            'runtimeMinutes': input_film_attributes['runtimeMinutes'],
            'decade': input_film_attributes['decade'],
            'averageRating': input_film_attributes['averageRating'],
            'numVotes': input_film_attributes['numVotes'],
            'overview': input_film_attributes['overview'],
            'original_language': input_film_attributes['original_language']
        }

        # Convert categorical variables to numerical using one-hot encoding
        df_encoded = pd.get_dummies(
            df_full[['genres_combined', 'original_language']])

        # Preprocess the input
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_encoded)

        # Train the Nearest Neighbors model
        model = NearestNeighbors(metric='cosine')
        model.fit(X_scaled)

        # Preprocess the input film
        input_film_encoded = pd.get_dummies(
            pd.DataFrame(input_film, index=[0]))
        input_film_encoded = input_film_encoded.reindex(
            columns=df_encoded.columns, fill_value=0)
        input_film_scaled = scaler.transform(input_film_encoded)

        # Find similar films
        # Increase n_neighbors to include more films
        distances, indices = model.kneighbors(
            input_film_scaled, n_neighbors=7)  # Update n_neighbors to 4

        # Get the recommended films
        recommended_films = df_full.iloc[indices[0]].copy()

        # Perform sentiment analysis on the overview text
        recommended_films.loc[:, 'overview'] = recommended_films['overview'].astype(
            str)
        recommended_films.loc[:, 'overview_sentiment'] = recommended_films['overview'].apply(
            lambda x: sid.polarity_scores(x)['compound'])

        # Filter recommended films based on similarity thresholds and original language

        # Adjust these thresholds as desired
        rating_threshold = 0.2  # Increase or decrease based on desired similarity
        popularity_threshold = 0.2  # Increase or decrease based on desired similarity
        sentiment_threshold = -1  # Adjust based on desired sentiment similarity

        similar_films = recommended_films[
            (abs(recommended_films['averageRating'] - input_film_attributes['averageRating']) <= rating_threshold) &
            (abs(recommended_films['popularity'] - input_film_attributes['popularity']) <= popularity_threshold) &
            (abs(recommended_films['overview_sentiment'] - input_film_sentiment) <= sentiment_threshold) &
            (recommended_films['original_language'] ==
             input_film_attributes['original_language'])
        ]

        # Remove the input film from the recommended films
        similar_films = similar_films[similar_films['originalTitle'] != film_name]

        # Select additional films if fewer than three recommendations
        if len(similar_films) < 3:
            additional_films = recommended_films.head(3 - len(similar_films))
            similar_films = pd.concat([similar_films, additional_films])

        # Sort by sentiment in descending order
        similar_films = similar_films.sort_values(
            by='overview_sentiment', ascending=False)

        # Display recommended films with images in side-by-side columns
        col1, col2, col3 = st.columns(3)

        num_films = len(similar_films)
        films_per_column = (num_films + 2) // 3  # Distribute films evenly across the columns

        for i in range(num_films):
            with col1, col2, col3:
                # Calculate the current column index
                col_index = i // films_per_column

                # Only display the film if it belongs to the current column
                if col_index == 0:
                    current_col = col1
                elif col_index == 1:
                    current_col = col2
                else:
                    current_col = col3

                # Display the film's details
                row = similar_films.iloc[i]
                current_col.subheader(row['originalTitle'])
                image_url = get_image_url(row['poster_path'])
                display_image(image_url)
                current_col.write("Nombre de votes: " + str(row['numVotes']))
                current_col.write("Genres: " + row['genres_combined'])
                current_col.write("Popularité: " + str(row['popularity']))
                current_col.write("Resumé score: " + str(row['overview_sentiment']))
                current_col.write("Résumé: " + row['overview'])
                current_col.write("Année de sortie: " + str(row['startYear']))


            st.write("—")

if __name__ == "__main__":
    page_2(df_full)
