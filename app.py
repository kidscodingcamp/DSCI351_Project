import streamlit as st\
from pymongo import MongoClient\
from neo4j import GraphDatabase\
\
# Initialize MongoDB connection\
client = MongoClient("mongodb_connection_string")\
db = client.movieDB\
movies_collection = db.movies\
\
# Initialize Neo4j connection\
neo4j_driver = GraphDatabase.driver("neo4j_connection_string")\
\
# Streamlit UI\
st.title("Movie Watchlist App")\
\
username = st.text_input("Enter your username")\
movie_title = st.text_input("Search for a movie to add to your watchlist")\
\
if st.button("Add Movie"):\
    # Search in MongoDB\
    movie = movies_collection.find_one(\{"title": movie_title\})\
    \
    # Neo4j session\
    with neo4j_driver.session() as session:\
        # Ensure the User node exists\
        session.run("MERGE (u:User \{name: $username\})", username=username)\
        \
        if movie:\
            # Movie exists in MongoDB, so add it with its ID\
            session.run("""\
                MATCH (u:User \{name: $username\})\
                MERGE (m:Movie \{id: $movie_id, title: $movie_title\})\
                MERGE (u)-[:ADDED_TO_WATCHLIST]->(m)\
                """, username=username, movie_id=str(movie['_id']), movie_title=movie_title)\
        else:\
            # Movie not found, add it without an ID\
            session.run("""\
                MATCH (u:User \{name: $username\})\
                MERGE (m:Movie \{title: $movie_title\})\
                MERGE (u)-[:ADDED_TO_WATCHLIST]->(m)\
                """, username=username, movie_title=movie_title)\
        \
        st.success(f"Added '\{movie_title\}' to \{username\}'s watchlist")\
}
