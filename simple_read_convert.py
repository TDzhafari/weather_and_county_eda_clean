###########################################################################
#   Author: Timur Dzhafari
#   Purpose: Climate dataset cleaning
#   Date: 3/9/2023
#
# todo: 1)transposing needs to be put into a callable function so that it can
#       be run by both run_temp_cleaning and run_perc_cleaning.
#
#       2)get the housing datasets and merge with this temp and perc data.
#
#       3)exploratory analysis is needed (simple describe, info, dtypes) mb
#       add visualizations and data dictionary if we want to be really fancy.
#
#       4)building time series models. (use OOP to do it once and replicate
#         3 times for all 3 of our models)
#
# data sources: zillow - (need link)
#               weather - (need link)
############################################################################

import pandas as pd
import numpy as np
import PyPDF2


def transpose():
    pass

###########################################################################
#           Temperature
###########################################################################


def run_temp_cleaning():
    """
    This function is designed to clean temperature .pdf file and convert it to usable
    dataframe for later merge with the housing prices dataframe.
    """
    file = 'D:/School/UNCC/projects/repos/Prototype/tests/temp.pdf'
    pdfdoc_remote = PyPDF2.PdfReader(file)
    page = pdfdoc_remote.pages[0]
    raw_data = page.extract_text(0)

    # generate a dictionary to add data to
    clean_data_dictionary = {}
    # separate the raw_data string into a list of lists, removing header
    listed_raw_data = raw_data.split('\n')[2:]
    # first row represents column names, assign it var name col_names
    col_names = listed_raw_data[0].split(' ')
    # create a subset of list of lists that only has the body of the dataset
    listed_raw_data = listed_raw_data[1:]

    # outer loop iterating over columns
    for col_name in col_names:

        # for each column name create a new key in the dictionary, value is an empty list
        clean_data_dictionary[col_name] = []

        # inner loop iterates through rows of body of the dataset
        for line in listed_raw_data:
            # initial cleaning. Join the items in the row into a single string.
            line_content = ''.join(line)
            # remove all spaces
            line_content = line_content.replace(' ', '')
            # replace Mean with Avg. to be able to handle missing values 'M' (unsure what M means)
            line_content = line_content.replace('Mean', 'Avg.')
            # remove all 'M' non numeric values with 0.00
            line_content = line_content.replace('M', '0.00')
            # omit all short rows
            if len(line_content) < 40:
                continue

            # if column name is year get first 4 charasters of the string - its a year
            if col_name == 'Year':
                clean_data_dictionary[col_name].append(line_content[:4])
            # if column isnt 'Year' proceed with parsing the data
            else:
                # first get the subset of the data in the row (remove year data)
                line_content_no_year = line_content[4:]
                # if there is no 'M' values in the substring
                if line_content_no_year[col_names.index(col_name)-1: col_names.index(col_name)+3].find('M') == -1:
                    # append the section using string slicing.
                    clean_data_dictionary[col_name].append(
                        line_content_no_year[(col_names.index(col_name)-1) * 4: ((col_names.index(col_name)) * 4)])
                # if 'M' is present append NONE string (not a none object)
                else:
                    clean_data_dictionary[col_name].append('NONE')

    # generate the dataframe out of the dictionary
    output_df = pd.DataFrame.from_dict(clean_data_dictionary)
    # print it the dictionary
    print(output_df.to_string())
    return output_df

###########################################################################
#           Percipitation
###########################################################################


def run_percip_cleaning():
    """
    This function is designed to clean percipitation .pdf file and convert it to usable
    dataframe for later merge with the housing prices dataframe.
    """

    file = 'D:/School/UNCC/projects/repos/Prototype/tests/percip.pdf'
    pdfdoc_remote = PyPDF2.PdfReader(file)
    page = pdfdoc_remote.pages[0]
    raw_data = page.extract_text(0)

    # print(raw_data.split('\n')[2:])

    clean_data_dictionary = {}
    listed_raw_data = raw_data.split('\n')[2:]
    col_names = listed_raw_data[0].split(' ')
    listed_raw_data = listed_raw_data[1:]
    for col_name in col_names:
        clean_data_dictionary[col_name] = []

        for line in listed_raw_data:
            line_content = ''.join(line)
            line_content = line_content.replace(' ', '')
            line_content = line_content.replace('Mean', 'Avg.')
            line_content = line_content.replace('M', '0.00')
            line_content = line_content.replace('T', '0.00')
            if len(line_content) < 40:
                continue
            if col_name == 'Year':
                clean_data_dictionary[col_name].append(line_content[:4])
            else:
                line_content_no_year = line_content[4:]
                # try:
                if line_content_no_year[col_names.index(col_name)-1: col_names.index(col_name)+3].find('M') == -1 and line_content_no_year[col_names.index(col_name)-1: col_names.index(col_name)+3].find('T') == -1:

                    clean_data_dictionary[col_name].append(
                        line_content_no_year[(col_names.index(col_name)-1) * 4: ((col_names.index(col_name)) * 4)])
                else:
                    clean_data_dictionary[col_name].append('NA')

    output_df = pd.DataFrame.from_dict(clean_data_dictionary)
    print('/n')
    print(output_df.to_string())
    return output_df


###########################################################################
#           Transposing
###########################################################################
def transpose_df(temp_df):

    # remove "Annual" columns as it is not needed
    temp_df.drop(columns=["Annual"], inplace=True)

    # transpose the dataframe
    df_trans = temp_df.set_index('Year').T

    # get rid of calculated "Avg." column
    df_trans.drop(columns=["Avg."], inplace=True)

    # check out transposed df
    print(df_trans)

    # create a date range with the start and end dates
    date_range = pd.date_range(start='2000-01-01', end='2022-12-01', freq='MS')

    # vectorizing dataframe
    arr = temp_df.to_numpy()

    dict = {}
    cnt1 = 0

    # a bit tired at this point. strftime should be moved to the dataframe. No need to call it on every iteration of the loop. Fix out of bounds error. No need for try-except block if the code is better.
    try:
        for year_data in arr:
            for cnt in range(1, 13):
                dict[date_range[cnt1].strftime('%m-%d-%Y')] = year_data[cnt]
                cnt1 += 1
    except IndexError as e:
        print(
            f" boooo! out of bounds error! :( check out the last successful datapoint added. Key: {str(date_range[cnt1-1].strftime('%m-%d-%Y'))}, Value: {year_data[cnt-1]}")
        print(f' oh and here is the stack too: {e}')

    # final_df is what we decided we wanted for the output to look like.
    final_df = pd.DataFrame.from_dict(
        dict, orient='index', columns=['temp_value'])
    print(final_df.to_string())


def main():
    temp_df = run_temp_cleaning()
    percip_df = run_percip_cleaning()
