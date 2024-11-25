import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def take_inputs(df,query_col):

    """
    Takes in a DataFrame and a query column name.
    - Converts the query column to numeric, setting invalid entries to 0.
    
    Parameters:
    - csv_file: str or file-like object, the path to the CSV file.
    - query_col: str, the name of the column to process in the DataFrame.
    
    Returns:
    - DataFrame with the processed query column.
    """


    ## Missing vals like NaN or null or no val or even None are avoided

    ## But in case of string vals, we will enforce it to turn 0.

    try:
        # Check if the column is of object type (string or mixed)
        if df[query_col].dtype == "object":
            # Convert the column to numeric, replacing non-numeric with NaN and filling with 0
            df[query_col] = pd.to_numeric(df[query_col], errors="coerce").fillna(0)
        return df
    except Exception as e:
        raise ValueError(f"Error processing column '{query_col}': {e}")
    

def create_plot(tot_marks_series):
    """
    Takes a Pandas Series (tot_marks_series), creates a histogram of the values,
    overlays a normal distribution curve, and returns the plot with a JSON of statistics.
    
    Parameters:
    - tot_marks_series: pandas.Series, the series of marks or data points to plot.
    
    Returns:
    - plt object: the plot with histogram and normal distribution curve.
    - dict: JSON-like dictionary containing statistical details.
    """

    try:
        # Validate if the series is empty
        if tot_marks_series.empty:
            raise ValueError("The data series is empty, cannot create plot.")

        # Calculate basic statistics
        minimum = tot_marks_series.min()
        maximum = tot_marks_series.max() 
        mean = tot_marks_series.mean()
        median = tot_marks_series.median()
        mode = tot_marks_series.mode().iloc[0]  # Get the first mode
        std = tot_marks_series.std()
        skewness = tot_marks_series.skew()
        kurtosis = tot_marks_series.kurtosis()

        # Create histogram plot
        tot_marks_series.plot(kind="hist", bins=30, density=True, alpha=0.6, color='blue', edgecolor='black', label="Histogram")

        # Gen x-vals for the normal distribution curve
        x = np.linspace(tot_marks_series.min(), tot_marks_series.max(), 1000)

        # Calculate the Probability Density Function (PDF) for the normal distribution
        pdf = (1 / (np.sqrt(2 * np.pi) * std)) * np.exp(-0.5 * ((x - mean) / std) ** 2)

        # Plot the normal distribution curve
        plt.plot(x, pdf, 'r', linewidth=2, label="Normal PDF")

        # Add mean and standard deviation lines
        plt.axvline(mean, color='green', linestyle='--', label=f'Mean: {mean:.2f}')
        plt.axvline(mean + std, color='orange', linestyle='--', label=f'Mean + 1 StdDev: {mean + std:.2f}')
        plt.axvline(mean - std, color='orange', linestyle='--', label=f'Mean - 1 StdDev: {mean - std:.2f}')
        
        # Customize the plot
        plt.title("Histogram and Normal Distribution")
        plt.xlabel("Marks")
        plt.ylabel("Density")
        plt.legend(loc='best')

        # Create the statistical details dictionary
        stats_details = {
            "min": minimum,
            "max": maximum,
            "mean": mean,
            "median": median,
            "mode": mode,
            "std_dev": std,
            "skewness": skewness,
            "kurtosis": kurtosis
        }

        # Return the plot and the statistical details
        return plt, stats_details
    except Exception as e:
        raise ValueError(f"Error creating plot: {e}")


def get_curr_marks_plot_and_stat(tot_marks_series,sample_mark=None):

    """
    This function generates a plot for the distribution of the total marks and calculates various statistics 
    for a given sample mark. It returns both the plot and a dictionary containing the calculated statistical details.

    Parameters:
    - tot_marks_series (pd.Series): A Pandas Series containing the total marks data.
    - sample_mark (float, optional): A specific mark to analyze, used to calculate the z-score, percentile, 
                                      and probability density. If not provided, a ValueError will be raised.

    Returns:
    - matplotlib.pyplot: A plot showing the histogram of total marks, the normal distribution curve, 
                          and a marker for the given sample mark.
    - dict: A dictionary containing the calculated statistical details:
        - "z_score" (float): The z-score of the provided sample mark.
        - "percentile" (float): The percentile of the provided sample mark.
        - "probability_density" (float): The probability density at the provided sample mark.

    Raises:
    - ValueError: If the data series is empty or if no sample mark is provided.
    """

    try:
        # Validate if the series and mark
        if tot_marks_series.empty:
            raise ValueError("The data series is empty, please ensure proper column name is given.")
        if sample_mark==None:
            raise ValueError("No mark was given for query.")

        mean = tot_marks_series.mean()
        std = tot_marks_series.std()
        z_score = (sample_mark - mean) / std
        percentile = (tot_marks_series < sample_mark).mean() * 100
        probability_density = (1 / (np.sqrt(2 * np.pi) * std)) * np.exp(-0.5 * ((sample_mark - mean) / std) ** 2)

        # Clear any previous plot to ensure fresh plot
        plt.clf()

        # Histogram
        tot_marks_series.plot(kind='hist', bins=30, density=True, alpha=0.6, color='blue', edgecolor='black', label="Histogram")

        # Normal Distribution Curve
        x = np.linspace(tot_marks_series.min(), tot_marks_series.max(), 1000)
        pdf = (1 / (np.sqrt(2 * np.pi) * std)) * np.exp(-0.5 * ((x - mean) / std) ** 2)


        plt.plot(x, pdf, 'r', linewidth=2, label="Normal PDF")

        # Highlight the sample mark
        plt.scatter(sample_mark, probability_density, color='orange', s=50, label=f"{sample_mark} Mark (Input Mark)", zorder=5)

        # Customize the plot
        plt.title("Normal Distribution of Total Marks with Query Mark")
        plt.xlabel("Marks")
        plt.ylabel("Density")
        plt.axvline(x=sample_mark, color='orange', linestyle='--', linewidth=1)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)

        # Create the statistical details dictionary
        stats_details = {
            "z_score": z_score,
            "percentile": percentile,
            "probability_density": probability_density
        }

        # Return the plot and the statistical details
        return plt, stats_details
    except Exception as e:
        raise ValueError(f"Error creating plot: {e}")