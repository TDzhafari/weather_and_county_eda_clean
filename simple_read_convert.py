###########################################################################
#   Author: Timur Dzhafari
#   Purpose: Climeate Data mining
#   Date: 3/5/2023
############################################################################

import pandas as pd
import PyPDF2

###########################################################################
#           Temperature
###########################################################################

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

###########################################################################
#           Percipitation
###########################################################################

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
