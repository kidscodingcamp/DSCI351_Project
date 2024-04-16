import streamlit as st
from neo4j import GraphDatabase

# Function to create a Neo4j session
def get_neo4j_session(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver.session()

# Define your connection parameters
uri = "bolt://localhost:7687"  # or "neo4j://localhost:7687" depending on your setup
user = "neo4j"  # default user, replace with your actual username
password = "password"  # replace with your actual password

# Start a Streamlit app
st.title('Neo4j Movie Database Viewer')

# Fetch data from Neo4j
def fetch_data(query):
    with get_neo4j_session(uri, user, password) as session:
        result = session.run(query)
        return [record for record in result]

# Define a Cypher query
query = "MATCH (m:Movie) RETURN m.title as title, m.release_year as year LIMIT 10"

# Display data in Streamlit
if st.button('Fetch Movies'):
    try:
        data = fetch_data(query)
        if data:
            for record in data:
                st.write(f"Title: {record['title']}, Year: {record['year']}")
        else:
            st.write("No data found.")
    except Exception as e:
        st.write("An error occurred:", e)

# Run the Streamlit app
if __name__ == "__main__":
    st.sidebar.success("Enter your Neo4j credentials and run the app!")

