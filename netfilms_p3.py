import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
from clean_dataframe import clean_dataframe

# Define your color scheme
primaryColor = "#d90b1c"
backgroundColor = "#000000"
secondaryBackgroundColor = "#161616"
textColor = "#ffffff"


def page_3(df_full):
    st.title("Analyse des genres")

    # Get unique genre values
    genre_values = df_full['genres_combined'].unique()

    # Create a multiselect widget for genre filtering
    selected_genres = st.multiselect(
        'Select genres', genre_values, default=genre_values)

    # Filter the dataframe based on selected genres
    filtered_df = df_full[df_full['genres_combined'].isin(selected_genres)]

    # Regroup data by decade and calculate the average popularity, average rating, and sum of numVotes for each decade
    popularity_by_decade = filtered_df.groupby('decade')['popularity'].mean()
    rating_by_decade = filtered_df.groupby('decade')['averageRating'].mean()
    num_votes_by_decade = filtered_df.groupby('decade')['numVotes'].sum()

    # Configure Seaborn style
    sns.set(style="darkgrid")

    # # Create a figure with three subplots
    # fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))

    # # Plot the average popularity by decade
    # ax1.bar(popularity_by_decade.index.astype(str), popularity_by_decade)
    # ax1.set_xlabel('Decade')
    # ax1.set_ylabel('Average Popularity')
    # ax1.set_title('Average Popularity by Decade')
    # ax1.tick_params(axis='x', rotation=90)

    # # Plot the average rating by decade
    # ax2.bar(rating_by_decade.index.astype(str), rating_by_decade)
    # ax2.set_xlabel('Decade')
    # ax2.set_ylabel('Average Rating')
    # ax2.set_title('Average Rating by Decade')
    # ax2.tick_params(axis='x', rotation=90)

    # # Plot the sum of numVotes by decade
    # ax3.bar(num_votes_by_decade.index.astype(str), num_votes_by_decade)
    # ax3.set_xlabel('Decade')
    # ax3.set_ylabel('Number of Votes')
    # ax3.set_title('Number of Votes by Decade')
    # ax3.tick_params(axis='x', rotation=90)

    # # Calculate the average runtime of films per year for the filtered dataframe
    # average_runtime_year_filtered = filtered_df.groupby(
    #     'year')['runtimeMinutes'].mean()

    # # Create the line plot for the average runtime with filtered data
    # ax4.plot(average_runtime_year_filtered.index,
    #          average_runtime_year_filtered)
    # ax4.set_xlabel('Année de sortie du film')
    # ax4.set_ylabel('Durée moyenne des films (minutes)')
    # ax4.set_title('Évolution de la durée moyenne des films')

    # # Adjust the spacing between subplots
    # plt.tight_layout()

    # # Display the charts in Streamlit
    # st.pyplot(fig)
    # Create a figure with three subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
        2, 2, figsize=(18, 12), facecolor=backgroundColor)

    # Plot the average popularity by decade
    ax1.bar(popularity_by_decade.index.astype(str),
            popularity_by_decade, color=primaryColor)
    ax1.set_xlabel('Decade', color=textColor)
    ax1.set_ylabel('Average Popularity', color=textColor)
    ax1.set_title('Average Popularity by Decade', color=textColor)
    ax1.tick_params(axis='x', rotation=90, colors=textColor)
    ax1.tick_params(axis='y', colors=textColor)

    # Plot the average rating by decade
    ax2.bar(rating_by_decade.index.astype(str),
            rating_by_decade, color=primaryColor)
    ax2.set_xlabel('Decade', color=textColor)
    ax2.set_ylabel('Average Rating', color=textColor)
    ax2.set_title('Average Rating by Decade', color=textColor)
    ax2.tick_params(axis='x', rotation=90, colors=textColor)
    ax2.tick_params(axis='y', colors=textColor)

    # Plot the sum of numVotes by decade
    ax3.bar(num_votes_by_decade.index.astype(str),
            num_votes_by_decade, color=primaryColor)
    ax3.set_xlabel('Decade', color=textColor)
    ax3.set_ylabel('Number of Votes', color=textColor)
    ax3.set_title('Number of Votes by Decade', color=textColor)
    ax3.tick_params(axis='x', rotation=90, colors=textColor)
    ax3.tick_params(axis='y', colors=textColor)

    # Calculate the average runtime of films per year for the filtered dataframe
    average_runtime_year_filtered = filtered_df.groupby(
        'year')['runtimeMinutes'].mean()

    # Create the line plot for the average runtime with filtered data
    ax4.plot(average_runtime_year_filtered.index,
             average_runtime_year_filtered, color=primaryColor)
    ax4.set_xlabel('Année de sortie du film', color=textColor)
    ax4.set_ylabel('Durée moyenne des films (minutes)', color=textColor)
    ax4.set_title('Évolution de la durée moyenne des films', color=textColor)
    ax4.tick_params(axis='x', colors=textColor)
    ax4.tick_params(axis='y', colors=textColor)

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Display the charts in Streamlit
    st.pyplot(fig)


if __name__ == "__main__":
    df_full = clean_dataframe()
    page_3(df_full)
