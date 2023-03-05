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


clean_data_dictionary = {}
listed_raw_data = raw_data.split('\n')[2:]
col_names = listed_raw_data[0].split(' ')
listed_raw_data = listed_raw_data[1:]

for col_name in col_names:
    clean_data_dictionary[col_name] = []

    for line in listed_raw_data:
        line_content = ''.join(line)
        line_content = line_content.replace(' ', '')
        if len(line_content) < 40:
            continue
        # print(line_content)
        if col_name == 'Year':
            clean_data_dictionary[col_name].append(line_content[:4])
        else:
            line_content_no_year = line_content[4:]
            # try:
            if line_content_no_year[col_names.index(col_name)-1: col_names.index(col_name)+3].find('M') == -1:

                clean_data_dictionary[col_name].append(
                    line_content_no_year[(col_names.index(col_name)-1) * 4: ((col_names.index(col_name)) * 4)])
            else:
                clean_data_dictionary[col_name].append('NA')

output_df = pd.DataFrame.from_dict(clean_data_dictionary)
print(output_df.to_string())

# build a separate function to work through the bottom part of the pdf file


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
        if len(line_content) < 40:
            continue
        # print(line_content)
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
