import pandas as pd
from datetime import datetime

main_file = "main.xlsx"

def get_main_data():
    """read the main file"""
    #on default the first row is the header, the first column is the row id (that is important for the join action later on)
    df = pd.read_excel(main_file, sheet_name="MOCK_DATA")
    return df



def get_current_month_rate():
    """To read the rate file according to current month"""
    #get the month string
    #eg: April
    month = datetime.now().strftime("%B")

    #use the month name as file name
    file_path = "lookup/" + month + ".xlsx"

    #read the excel file
    df = pd.read_excel(file_path, sheet_name="data")
    return df



def calcuate_new_rate(main_file, rate_file):

    # join the two tables, just like VLOOKUP, the default "lookup value" is the key of the tables.
    # this create a new dataframe
    joined = main_file.join(rate_file, how="left", lsuffix="_main", rsuffix="_rate")

    # do calcuations:
    main_file["new_rate"] = joined["balance"] * joined["Rate"]

    return main_file


if __name__ == '__main__':
    # get the nessary datas
    main = get_main_data();
    month_rate = get_current_month_rate()

    # do the calcuation
    result = calcuate_new_rate(main, month_rate)

    print(result)
    # output to file
    result.to_excel("output.xlsx")