# main.py

import streamlit as st
import pandas as pd
from process import take_inputs, create_plot, get_curr_marks_plot_and_stat


## Data Persistnace
if "query_col" not in st.session_state:
    st.session_state["query_col"] = None

if "df" not in st.session_state:
    st.session_state["df"] = None

if "general_plot" not in st.session_state:
    st.session_state["general_plot"] = None

if "general_stats_details" not in st.session_state:
    st.session_state["general_stats_details"] = None 

if "curr_mark_plot" not in st.session_state:
    st.session_state["curr_mark_plot"] = None

if "curr_mark_stat_details" not in st.session_state:
    st.session_state["curr_marks_stat_details"] = None

if "sample_mark" not in st.session_state:
    st.session_state["sample_mark"] = None



## View elements persistance
if "gen_plot_stat" not in st.session_state:
    st.session_state["gen_plot_stat"] = None

if "futher_analysis" not in st.session_state:
    st.session_state["further_analysis"] = None 

## Functionizing Graphs for persistance

def generate_plot_and_stats():
    """
    Processes the data, generates the plot, and displays the statistical details.
    Also, stores the plot and stats in session state for persistence.
    """
    try:
        # Display the graph generation details
        st.write("""
            **Graph Generation Details:**
            - The plot displays a histogram of the selected column along with a normal distribution curve fitted to the data.
            - **Mean** and **Standard Deviation** are marked on the plot as vertical lines.
            - If the column has more than one mode (i.e., **multimodal** distribution), only the **first mode** (most frequent value) is displayed.
            - The **normal distribution curve** is calculated using the **mean** and **standard deviation** of the data.
            - Any missing or non-numeric values are excluded from the analysis before generating the plot.
            """)

        query_col = st.session_state["query_col"]
        
        # Process the data and create the plot
        processed_df = take_inputs(st.session_state["df"], query_col)

        # Generate the plot and get stats
        general_graph_plot, general_stats_details = create_plot(processed_df[query_col])

        # Store the plot and stats in session state for persistence
        st.session_state["general_plot"] = general_graph_plot
        st.session_state["general_stats_details"] = general_stats_details

        # Show the plot
        st.pyplot(st.session_state["general_plot"])

        # Show the stats in a formatted manner
        st.write("""
            ### Statistical Details:
            - **Mean**: {:.2f}
            - **Median**: {:.2f}
            - **Minimum** {:.2f}
            - **Maximum** {:.2f}
            - **Mode**: {:.2f}
            - **Standard Deviation**: {:.2f}
            - **Skewness**: {:.2f}
            - **Kurtosis**: {:.2f}
            """.format(general_stats_details['mean'], general_stats_details['median'],general_stats_details["min"],general_stats_details["max"],general_stats_details['mode'], general_stats_details['std_dev'], general_stats_details['skewness'], general_stats_details['kurtosis']))
    

    except ValueError as e:
        st.error(f"Error: {e}")


def handle_mark_query_and_plot():
    """
    Function to handle user query input, generate the plot, and persist the results in session_state.
    """


    if sample_mark <= 0 and st.session_state["sample_mark"] is not None:
        st.error("Please enter a valid mark greater than 0.")
        return

    try:
        # Process the data and create the plot
        query_col= st.session_state["query_col"]
        processed_df = take_inputs(st.session_state["df"], query_col)
        # Call the function to generate plot and stats
        curr_mark_graph_plot, stats_details = get_curr_marks_plot_and_stat(processed_df[query_col], sample_mark)

        # Save the results in session_state for persistence
        st.session_state["curr_mark_plot"] = curr_mark_graph_plot
        st.session_state["curr_marks_stat_details"] = stats_details
        st.session_state["sample_mark"] = sample_mark

        # Display the plot and stats
        st.pyplot(st.session_state["curr_mark_plot"])
        st.write("### Statistical Details:")
        st.write(f"""
        - **Z-Score**: {stats_details['z_score']:.2f}
            - The Z-Score represents how many standard deviations the queried mark is from the mean.
        - **Percentile**: {stats_details['percentile']:.2f}%
            - The percentile indicates the percentage of values below the queried mark.
        - **Probability Density**: {stats_details['probability_density']:.4f}
            - The probability density is the likelihood of the queried mark occurring in the distribution.
        """)


    except ValueError as e:
        st.error(f"Error: {e}")









st.title("**Data Analysis and Visualization: Query Mark Analysis**")
st.write("This project provides statistical analysis and visualization for Numeric data queries, focusing on distributions, Z-Scores, Percentiles, and Probability Density functions.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV File", type=["csv", "xlsx", "xls"])
    
if uploaded_file is not None:
    try:
        # Determine file type based on extension and read accordingly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        
    st.session_state["df"]=df

    # Display the DataFrame in the app
    st.write("### Data Preview")
    col1,col2,col3=st.columns([1, 2, 1])  # 1fr, 3fr, 1fr
    with col2:
        st.dataframe(df)

    # Display explanation paragraph under Data Preview
    st.write("""
        **Handling of Data:**
        - Any missing values such as **NaN**, **Null**, **None**, **blank**, or **spaces** will be automatically avoided (filled with 0).
        - Any non-numeric strings (e.g., **Jacob**) will be converted to **0**.
        - Any numerical strings (e.g., **"36"**) will be converted into numerical values (integer or float).
        """)

    # User selects the query column from the DataFrame
        
    st.session_state["query_col"]= st.selectbox("Select a Column to Analyze", df.columns)

    if st.button("Generate Plot and Stats"):
        st.session_state["gen_plot_stat"] = True

    if (st.session_state["gen_plot_stat"]):
        generate_plot_and_stats()
        if st.button("Futher Analysis.."):
            st.session_state["sample_mark"] = True



    if(st.session_state["sample_mark"]):
        # Ask the user for the query mark input (ensure it's a float)
        sample_mark = st.number_input("Enter a Mark to Query Further")

        if sample_mark is not None:
            handle_mark_query_and_plot()

        



