import pandas as pd
import datetime as dt
import numpy as np

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

    for i in range(1, 13):
        # Filter the data to get only the January rows
        month_data = maricopa_df.loc[maricopa_df['Time Period'].dt.month == i]

        # Calculate the average precipitation for month
        month_average = month_data.loc[month_data['Precip'] != 'T', 'Precip'].astype(
            float).mean()

        # Impute the 'T' values with the average precipitation
        maricopa_df.loc[((maricopa_df['Precip']
                        == 'T') & (maricopa_df['Time Period'].dt.month == i)), 'Precip'] = month_average

    miami_df = pd.read_csv(dir + 'miami_dade_data.csv')
    miami_df['Time Period'] = pd.to_datetime(
        miami_df['Time Period'], errors='coerce')
    miami_df['Month'] = miami_df['Time Period'].dt.strftime('%B')

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

    df_dict = {'Maricopa_AZ': maricopa_df,
               'Miami_FL': shasta_df, 'Shasta_CA': shasta_df}

    # for key in df_dict.keys():
    #     df_dict.get(key).set_index['Month']

    return (df_dict)


def EDA(df):
    """
    perform basic EDA on the dataset
    """
    # read_dfs
    pass


def main():
    county_data = read_dfs_and_clean(directory_w_data)
    for county in county_data.keys():
        print(f'The {county} dataset is below \n {county_data.get(county)}')
        print(
            f'Info of {county} dataset is below \n {county_data.get(county).info()}')


main()
