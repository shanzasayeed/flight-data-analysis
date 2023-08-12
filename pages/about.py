import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
flights_data = pd.read_csv('flight_data.csv')

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

def main():
    st.title("About Flight Data")
    
    st.write(
        "Welcome to the 'About Flight Data' page! Here, you can explore insights and statistics"
        " from the provided flight dataset. This dataset contains information about flights, including"
        " departure and arrival times, delays, carriers, and more."
    )
    
    st.header("Dataset Overview")
    st.write("Let's start by taking a look at the first few rows of the dataset:")
    st.dataframe(flights_data.head())
    
    st.header("Number of Flights")
    num_flights = len(flights_data)
    st.write(f"Number of flights in the dataset: {num_flights}")
    
    st.header("Average Departure Delay")
    avg_dep_delay = flights_data['dep_delay'].mean()
    st.write(f"Average departure delay: {avg_dep_delay:.2f} minutes")
    
    st.header("Departure Delay Distribution")
    st.write("Let's visualize the distribution of departure delays:")
    plt.figure(figsize=(10, 6))
    sns.histplot(data=flights_data, x='dep_delay', bins=50, kde=True)
    plt.xlabel("Departure Delay (minutes)")
    plt.ylabel("Frequency")
    st.pyplot(plt)
    
    st.header("Airlines with Most Flights")
    airline_counts = flights_data['carrier'].value_counts()
    st.write("The top airlines with the most flights:")
    st.bar_chart(airline_counts)
    
    st.header("Top 10 Busiest Routes")
    top_routes = flights_data.groupby(['origin', 'dest']).size().reset_index(name='num_flights')
    top_routes = top_routes.sort_values('num_flights', ascending=False).head(10)
    st.write("The top 10 busiest flight routes:")
    st.dataframe(top_routes)
    
    st.header("Data Types of Numeric Columns")
    numeric_columns = ['dep_time', 'dep_delay', 'arr_time', 'arr_delay', 'air_time', 'distance', 'hour', 'minute']
    numeric_data = flights_data[numeric_columns]
    data_types = numeric_data.dtypes
    st.write(data_types)
    
    st.header("Concluding Remarks")
    st.write(
        "Exploring this flight dataset provides valuable insights into flight delays, airlines, and popular routes."
        " Analyzing the data can lead to better strategies for minimizing delays, optimizing routes, and improving"
        " overall flight operations. This 'About' page serves as a starting point for discovering patterns in the data"
        " and making informed decisions."
    )
    
if __name__ == "__main__":
    main()
