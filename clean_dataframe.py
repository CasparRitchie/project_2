import pandas as pd
import streamlit as st


@st.cache_data
def clean_dataframe():
    # Load the film dataset (df_full)
    df_full = pd.read_csv(
        "df_full_new.csv", na_values='\\N')
    df_full['release_date'] = pd.to_datetime(
        df_full['release_date'], errors='coerce')
    df_full['Nb_traduction'] = df_full['spoken_languages'].astype(str).apply(
        lambda x: len(x) - 1)
    # Add a column for decades
    df_full['year'] = df_full['release_date'].dt.year
    df_full['decade'] = (df_full['year'] // 10) * 10
    # Drop rows with non-finite values in the 'decade' column
    df_full = df_full.dropna(subset=['decade'])
    df_full['popularity'] = pd.to_numeric(
        df_full['popularity'], errors='coerce')
    # Convert the 'decade' column to integers
    df_full['decade'] = df_full['decade'].astype(int)

    # enleve ADULT
    df_full = df_full[df_full['adult'] != True]

    # Remove films released before 1950
    df_full = df_full[df_full['decade'] >= 1950]

    # Combine "runtimeMinutes" and "runtime" columns into a new column "total_runtime"
    df_full['total_runtime'] = df_full['runtimeMinutes'].combine_first(
        df_full['runtime'])

    # Drop the "runtimeMinutes" and "runtime" columns
    # df_full.drop(['runtimeMinutes', 'runtime'], axis=1, inplace=True)

    # Drop rows with missing values in "total_runtime"
    df_full.dropna(subset=['total_runtime'], inplace=True)

    # Extract the first genre entry from genres_x
    df_full['genres_x'] = df_full['genres_x'].str.strip(
        "[]").str.split(", ").str[0].str.strip("'")

    # Extract the first genre entry from genres_y
    df_full['genres_y'] = df_full['genres_y'].str.split(",").str[0].str.strip()

    # Combine genres_x and genres_y, taking the first non-empty entry
    df_full['genres_combined'] = df_full['genres_x'].fillna(
        df_full['genres_y'])

    # Replace remaining blank values in genres_combined with "None"
    # Convert the type to date, handling empty or invalid values
    df_full['genres_combined'] = df_full['genres_combined'].replace('', 'None')
    print('df full is being used and it looks like this')
    print(df_full.columns)

    return df_full
