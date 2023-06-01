# import pandas as pd
# from fuzzywuzzy import process
# from fuzzywuzzy import fuzz
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer
# from sklearn.neighbors import NearestNeighbors
# from sklearn.preprocessing import StandardScaler
# import streamlit as st
# import requests

# from clean_dataframe import clean_dataframe


# def get_image_url(poster_path, size='w500'):
#     base_url = 'https://image.tmdb.org/t/p'
#     return f'{base_url}/{size}/{poster_path}'


# def display_image(image_url):
#     response = requests.get(image_url)
#     st.image(response.content, use_column_width=True)


# def page_2(df_full):
#     nltk.download('vader_lexicon')

#     # Get film name from user input
#     film_name = st.text_input("Enter a film name:")

#     # Look up attributes from df_full based on film name
#     matching_films = df_full[df_full['originalTitle'].apply(
#         lambda x: fuzz.partial_ratio(x.lower(), film_name.lower())) > 90]
#     if matching_films.empty:
#         st.write("No matching films found.")
#         return

#     input_film_attributes = matching_films.iloc[0]
#     input_film = {
#         'genres_combined': input_film_attributes['genres_combined'],
#         'popularity': input_film_attributes['popularity'],
#         'runtimeMinutes': input_film_attributes['runtimeMinutes'],
#         'decade': input_film_attributes['decade'],
#         'averageRating': input_film_attributes['averageRating'],
#         'numVotes': input_film_attributes['numVotes'],
#         'overview': input_film_attributes['overview'],
#         'original_language': input_film_attributes['original_language'],
#         'poster_path': input_film_attributes['poster_path']
#     }

#     # Convert categorical variables to numerical using one-hot encoding
#     df_encoded = pd.get_dummies(
#         df_full[['genres_combined', 'original_language']])

#     # Preprocess the input
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(df_encoded)

#     # Train the Nearest Neighbors model
#     model = NearestNeighbors(metric='cosine')
#     model.fit(X_scaled)

#     # Preprocess the input film
#     input_film_encoded = pd.get_dummies(pd.DataFrame(input_film, index=[0]))
#     input_film_encoded = input_film_encoded.reindex(
#         columns=df_encoded.columns, fill_value=0)
#     input_film_scaled = scaler.transform(input_film_encoded)

#     # Find similar films
#     # Increase n_neighbors to include more films
#     distances, indices = model.kneighbors(input_film_scaled, n_neighbors=3)

#     # Get the recommended films
#     recommended_films = df_full.iloc[indices[0]].copy()

#     # Perform sentiment analysis on the overview text
#     sid = SentimentIntensityAnalyzer()
#     recommended_films.loc[:,
#                           'overview'] = recommended_films['overview'].astype(str)
#     recommended_films.loc[:, 'overview_sentiment'] = recommended_films['overview'].apply(
#         lambda x: sid.polarity_scores(x)['compound'])

#     # Filter recommended films based on similarity thresholds and original language
#     rating_threshold = 200  # Adjust this threshold as desired
#     popularity_threshold = 200  # Adjust this threshold as desired

#     similar_films = recommended_films[
#         (abs(recommended_films['averageRating'] - input_film_attributes['averageRating']) <= rating_threshold) &
#         (abs(recommended_films['popularity'] - input_film_attributes['popularity']) <= popularity_threshold) &
#         (recommended_films['original_language'] ==
#          input_film_attributes['original_language'])
#     ]

#     # Remove the input film from the recommended films
#     similar_films = similar_films[similar_films['originalTitle'] != film_name]

#     # Sort by sentiment in descending order
#     similar_films = similar_films.sort_values(
#         by='overview_sentiment', ascending=False)

#     # Display recommended films with images
#     for index, row in similar_films.iterrows():
#         st.subheader(row['originalTitle'])
#         st.write("Number of Votes:", row['numVotes'])
#         st.write("Genres:", row['genres_combined'])
#         st.write("Popularity:", row['popularity'])
#         st.write("Overview Sentiment:", row['overview_sentiment'])
#         image_url = get_image_url(row['poster_path'])
#         display_image(image_url)
#         st.write("---")


# if __name__ == "__main__":
#     df_full = clean_dataframe()
#     page_2(df_full)


import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import streamlit as st
import requests
import seaborn as sns
from clean_dataframe import clean_dataframe
import matplotlib.pyplot as plt

# Define your color scheme
primaryColor = "#d90b1c"
backgroundColor = "#000000"
secondaryBackgroundColor = "#161616"
textColor = "#ffffff"
# Set the color palette
sns.set_palette([primaryColor])


def get_image_url(poster_path, size='w500'):
    base_url = 'https://image.tmdb.org/t/p'
    return f'{base_url}/{size}/{poster_path}'


def display_image(image_url):
    response = requests.get(image_url)
    st.image(response.content, use_column_width=True)


def page_2(df_full):
    # Get unique genre values
    genre_values = df_full['genres_combined'].unique()

    # Create a multiselect widget for genre filtering
    selected_genres = st.multiselect(
        'Select genres', genre_values, default=genre_values)

    # Filter the dataframe based on selected genres
    filtered_df = df_full[df_full['genres_combined'].isin(selected_genres)]

    st.title('Tendances')
    # Add a slider to select the start and end years
    start_year, end_year = st.slider('Select a range of years', min_value=int(
        df_full['year'].min()), max_value=int(df_full['year'].max()), value=(2010, 2022))

    # Filter the data for the selected range of years and selected genres
    filtered_data = df_full[df_full['year'].between(
        start_year, end_year) & df_full['genres_combined'].isin(selected_genres)]

    # Count the number of films by genre
    genre_counts = filtered_data['genres_combined'].value_counts().head(10)

    # Sort the genres in descending order
    genre_counts_sorted = genre_counts.sort_values(ascending=False)
    sns.set_palette([primaryColor])

    # Create a horizontal bar plot
    fig, ax = plt.subplots(facecolor=backgroundColor)
    ax.barh(genre_counts_sorted.index, genre_counts_sorted.values,
            color=primaryColor)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Films', color=textColor)
    ax.set_ylabel('Genre', color=textColor)
    ax.set_title('Number of Films by Genre from {} to {}'.format(
        start_year, end_year), color=textColor)
    ax.xaxis.label.set_color(textColor)
    ax.yaxis.label.set_color(textColor)
    ax.title.set_color(textColor)
    ax.spines['bottom'].set_color(textColor)
    ax.spines['left'].set_color(textColor)
    ax.tick_params(axis='x', colors=textColor)
    ax.tick_params(axis='y', colors=textColor)

    # Display the plot using st.pyplot()
    st.pyplot(fig)
    plt.show()

    # Filter the data for the selected range of years and selected genres for language analysis
    filtered_data_language = filtered_data[filtered_data['year'].between(
        start_year, end_year) & filtered_data['genres_combined'].isin(selected_genres)]

    # Filter films released in 2022
    films_2022 = filtered_data_language
    # [filtered_data_language['year'] == 2022]

    # Keep only the first language in 'spoken_languages' and exclude empty values ([])
    films_2022['spoken_one'] = films_2022['spoken_languages'].str.split(
        ',').str[0]
    films_2022['spoken_one'] = films_2022['spoken_one'].replace(
        "['en'", "['en']")
    films_2022 = films_2022[films_2022['spoken_one'] != '[]']

    # Count the number of films by spoken language
    language_counts = films_2022['spoken_one'].value_counts().head(10)

    # # Créer le graphique à barres
    # fig, ax = plt.subplots(figsize=(8, 4))
    # sns.barplot(x=language_counts.index, y=language_counts.values, ax=ax,
    #             color=primaryColor)
    # ax.set_xlabel("Langue")
    # ax.set_ylabel("Nombre de films")
    # ax.set_title('10 langues les plus parlées dans les films sortis de {} à {}'.format(
    #     start_year, end_year))
    # st.pyplot(fig)

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(8, 4), facecolor=backgroundColor)
    sns.barplot(x=language_counts.index, y=language_counts.values,
                ax=ax, color=primaryColor)

    # Set the color of the bars individually
    for bar in ax.patches:
        bar.set_color(primaryColor)

    # Set the labels and title of the chart
    ax.set_xlabel("Langue", color=textColor)
    ax.set_ylabel("Nombre de films", color=textColor)
    ax.set_title('10 langues les plus parlées dans les films sortis de {} à {}'.format(
        start_year, end_year), color=textColor)
    ax.xaxis.label.set_color(textColor)
    ax.yaxis.label.set_color(textColor)
    ax.title.set_color(textColor)
    ax.spines['bottom'].set_color(textColor)
    ax.spines['left'].set_color(textColor)
    ax.tick_params(axis='x', colors=textColor)
    ax.tick_params(axis='y', colors=textColor)

    # Display the plot using st.pyplot()
    st.pyplot(fig)


if __name__ == "__main__":
    df_full = clean_dataframe()
    page_2(df_full)
