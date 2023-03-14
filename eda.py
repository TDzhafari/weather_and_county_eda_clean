import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

# simply replace the directory in the string with the directory wher you have your datasets and execute the script.

directory_w_data = 'D:/School/UNCC/projects/repos/simple_pdf_read/datasets/'


def read_dfs(dir):
    maricopa_df = pd.read_csv(dir + 'Maricopa_county_data.csv')
    miami_df = pd.read_csv(dir + 'miami_dade_data.csv')
    shasta_df = pd.read_csv(dir + 'Shasta County_Redding CA.csv')

    return ({'Maricopa_AZ': maricopa_df, 'Miami_FL': miami_df, 'Shasta_CA': shasta_df})


def read_dfs_and_clean(dir):
    maricopa_df = pd.read_csv(dir + 'Maricopa_county_data.csv')
    maricopa_df['Time Period'] = pd.to_datetime(
        maricopa_df['Time Period'], errors='coerce')
    maricopa_df['Month'] = maricopa_df['Time Period'].dt.strftime('%B')

    print(maricopa_df.columns)

    maricopa_df.loc[maricopa_df['Time Period'] == '7/31/2004',
                    'Housing Prices'] = maricopa_df.loc[maricopa_df['Time Period'] == '7/31/2004', 'Housing Prices'].fillna(183041.7888)

    for i in range(1, 13):
        # Filter the data to get only the January rows
        month_data = maricopa_df.loc[maricopa_df['Time Period'].dt.month == i]

        # Calculate the average precipitation for month
        month_average = month_data.loc[month_data['Precip'] != 'T', 'Precip'].astype(
            float).mean()

        # Impute the 'T' values with the average precipitation
        maricopa_df.loc[((maricopa_df['Precip']
                        == 'T') & (maricopa_df['Time Period'].dt.month == i)), 'Precip'] = month_average
    maricopa_df['Precip'] = pd.to_numeric(maricopa_df['Precip'])

    miami_df = pd.read_csv(dir + 'miami_dade_data.csv')
    miami_df['Time Period'] = pd.to_datetime(
        miami_df['Time Period'], errors='coerce')
    miami_df['Month'] = miami_df['Time Period'].dt.strftime('%B')

    miami_df['Housing Price'].fillna(276517.2682, inplace=True)
    miami_df.loc[miami_df['Time Period'] == '3/31/2018', 'Housing Price'] = miami_df.loc[miami_df['Time Period']
                                                                                         == '3/31/2018', 'Housing Price'].fillna(276517.2682)

    for i in range(1, 13):
        # Filter the data to get only the January rows
        month_data = miami_df.loc[miami_df['Time Period'].dt.month == i]

        # Calculate the average precipitation for month
        month_average = month_data.loc[month_data['Precip'] != 'T', 'Precip'].astype(
            float).mean()

        # Impute the 'T' values with the average precipitation
        miami_df.loc[((miami_df['Precip']
                       == 'T') & (miami_df['Time Period'].dt.month == i)), 'Precip'] = month_average

    shasta_df = pd.read_csv(dir + 'Shasta County_Redding CA.csv')
    shasta_df['Time Period'] = pd.to_datetime(
        shasta_df['Time Period'], errors='coerce')
    shasta_df['Month'] = shasta_df['Time Period'].dt.strftime('%B')

    for i in range(1, 13):
        # Filter the data to get only the January rows
        month_data = shasta_df.loc[shasta_df['Time Period'].dt.month == i]

        # Calculate the average precipitation for month
        month_average = month_data.loc[month_data['Precip'] != 'T', 'Precip'].astype(
            float).mean()

        # Impute the 'T' values with the average precipitation
        shasta_df.loc[((shasta_df['Precip']
                       == 'T') & (shasta_df['Time Period'].dt.month == i)), 'Precip'] = month_average

    shasta_df['Precip'] = pd.to_numeric(shasta_df['Precip'])
    df_dict = {'Maricopa_AZ': maricopa_df,
               'Miami_FL': miami_df, 'Shasta_CA': shasta_df}

    # for key in df_dict.keys():
    #     df_dict.get(key).set_index['Month']

    return (df_dict)


def EDA(county_name, df):
    """
    perform basic EDA on the dataset
    """
    # df['Percip'] = df['Percip'].astype(np.float32)

    # Print the shape of the DataFrame
    print(f'Shape of the {county_name} dataset: \n {df.shape}')

    # Print the data types of the columns
    print(f'Data types of the {county_name} dataset: \n {df.dtypes}')

    # Print the summary statistics of the numerical columns
    print(
        f'Summary statistics of the {county_name} dataset: \n {round(df.describe(),2)}')

    # Check for missing values
    print(
        f'Missing values of the {county_name} dataset: \n {df.isnull().sum()}')

    print(f'Columns of {county_name} are {df.columns}')

    # BELOW NEEDS FIXING

    # Create a figure with two subplots, sharing the y-axis
    fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(10, 5), sharey=True)

    # Plot the first numerical column on the first subplot
    axs[0].hist(df['Avg_Temp'])
    axs[0].set_xlabel(f'Avg_Temp {county_name}')
    axs[0].set_ylabel('Frequency')

    # Plot the second numerical column on the second subplot
    axs[1].hist(df['Precip'])
    axs[1].set_xlabel(f'Precip {county_name}')
    axs[1].set_ylabel('Frequency')

    # Plot the third numerical column on the second subplot
    axs[2].hist(df['Max_Temp'])
    axs[2].set_xlabel(f'Max_Temp {county_name}')
    axs[2].set_ylabel('Frequency')

    # Plot the third numerical column on the second subplot
    if county_name == 'Miami_FL':
        axs[3].hist(df['Housing Price'])
        axs[3].set_xlabel(f'Housing Price {county_name}')
        axs[3].set_ylabel('Frequency')
    else:
        axs[3].hist(df['Housing Prices'])
        axs[3].set_xlabel(f'Housing Prices {county_name}')
        axs[3].set_ylabel('Frequency')

    # Show the plot
    plt.show()

    plt.plot(df['Time Period'], df['Avg_Temp'])

    # Add labels and title
    plt.xlabel("Time Period")
    plt.ylabel(f"Average Temperature {county_name}")
    plt.title("Average Temperature by Time Period")

    # Show plot
    plt.show()

    plt.plot(df['Time Period'], df['Precip'])

    # Add labels and title
    plt.xlabel("Time Period")
    plt.ylabel(f"Precipitation {county_name}")
    plt.title("Precipitation by Time Period")

    # Show plot
    plt.show()

    plt.plot(df['Time Period'], df['Max_Temp'])

    # Add labels and title
    plt.xlabel("Time Period")
    plt.ylabel(f"Max Temperature {county_name}")
    plt.title("Max Temperature by Time Period")

    # Show plot
    plt.show()


def main():
    county_data = read_dfs_and_clean(directory_w_data)
    for county in county_data.keys():
        EDA(county, county_data.get(county))
        # print(f'The {county} dataset is below \n {county_data.get(county)}')
        # print(
        #     f'Info of {county} dataset is below \n {county_data.get(county).info()}')


main()
