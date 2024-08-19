import pandas as pd
import re

def process_bcr_data(data):
    """
    Process data for bar chart race visualization.

    :param data: DataFrame containing the processed data
    :return: Processed data suitable for bar chart race or error message
    """

    # RULES

    # 1. Check if the number of columns is between 3 and 6
    if not (3 <= data.shape[1] <= 6):
        return {"failed": "data failed bar chart race rule - number of columns must be between 3 and 6"}

    # 2. Check if the last column is a date column
    if not data.iloc[:, -1].apply(is_datetime_string).any():
        return {"failed": "data failed bar chart race rule - last column must be a date column"}

    # 3. Check if the second to last column is a number-string column
    if not data.iloc[:, -2].apply(lambda x: isinstance(x, str) and x.replace('.', '', 1).isdigit()).any():
        return {"failed": "data failed bar chart race rule - second to last column must be a quantity column"}

    # 4. Identify columns with word identifiers
    identifier_columns = identify_word_identifier_columns(data.iloc[:, :-2])


    # Rename the relevant columns based on the conditions
    new_columns = rename_columns(data.columns, identifier_columns)

    # Create a new DataFrame with the renamed columns
    new_data = data.copy()
    new_data.columns = new_columns

    # Select the relevant columns to form the new DataFrame
    selected_columns = [col for col in new_columns if col in ["category", "name", "value", "date"]]
    processed_data = new_data[selected_columns]

    print(processed_data)
    return processed_data.to_dict(orient='records')



def identify_word_identifier_columns(data):
    """
    Identify columns with word identifiers.

    :param data: DataFrame excluding the last two columns
    :return: List of column indices that match the word identifier rule
    """
    def is_non_link_word(x):
        if isinstance(x, str):
            if re.match(r'https?://|http://', x):  # Exclude URLs
                return False
            if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', x):  # Exclude date strings
                return False
            if x.replace('.', '', 1).isdigit():  # Exclude purely numeric strings
                return False
            if re.search(r'[A-Za-z]', x):  # Check if it contains any alphabetic character
                return True
        return False

    # Identify columns with word identifiers
    identifier_columns = [i for i in range(data.shape[1]) if data.iloc[:, i].apply(is_non_link_word).any()]
    return identifier_columns

def rename_columns(columns, identifier_columns):
    """
    Rename columns based on identified word identifiers and the last two columns.

    :param columns: List of original column names
    :param identifier_columns: List of column indices with word identifiers
    :return: List of new column names
    """
    new_columns = columns.tolist()

    # Rename the last two columns to "value" and "date"
    new_columns[-2] = "value"
    new_columns[-1] = "date"

    # Rename based on the number of word identifier columns found
    if len(identifier_columns) >= 2:
        new_columns[identifier_columns[0]] = "category"
        new_columns[identifier_columns[1]] = "name"
    elif len(identifier_columns) == 1:
        new_columns[identifier_columns[0]] = "name"

    return new_columns

def is_datetime_string(s):
    # Check if a string follows a common datetime format using regex
    datetime_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    return bool(re.match(datetime_pattern, str(s)))