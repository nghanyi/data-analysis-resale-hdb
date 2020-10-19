"""This is a module to show sort the data and show the Top 10 Cheapest Resale Flats
Function(top10()) :  allows the display of the top 10 cheapest resale flat with the
other details.
"""

from collections import Counter
import copy
import matplotlib.pyplot as plt
import pandas as pd
import data_helper
import search

""" To retrieve resale flat records with
    "region", "town", "street_name", "flat_type", "flat_model", "lease_commence_date", "remaining_lease", "resale_price" columns 
"""

# def get_filtered_data():
#     df = data_helper.get_dataframe()
#     top10_data = df[["region", "town", "street_name", "flat_type", "flat_model", "lease_commence_date", "remaining_lease",
#                      "resale_price"]]
#     # print(f"DataFrame:\n{top10_data}\n")
#     # print(f"column types:\n{top10_data.dtypes}")
#
#     # Convert the dataframe to list.
#     resaleflatList = top10_data.values.tolist()
#     return resaleflatList
#
# # Declare Lists to store the values
# rpRecord = []
# descRPAmt = []
# top10CheapestResaleFlat = []

#
# def retrieve_Top10():
#     resaleflatList = get_filtered_data()
#     print("Function : Tabulating Resale Flat Records..\n")
#     # Storing the region, town, flat ype and resale_price to another list
#     rpRecord = resaleflatList.copy()
#
#     # Sort resale flat record according to total resale price in ascending (Cheapest First)
#     descRPAmt = rpRecord.copy()
#     sorted_RPlist = sorted(descRPAmt, key=lambda x: x[7])  # x[7] : Index 7 is "resale_price" column
#
#     # Append top 10 Cheapest Resale Flats to list
#     for i in range(len(sorted_RPlist)):
#         if i < 10:
#             top10CheapestResaleFlat.append(sorted_RPlist[i])
#
#     # Returning values
#     print("Function : Showing Top 10 Completed..")
#     print("Top 10 Results:\n", top10CheapestResaleFlat)
#
#     return {"rpRecord": rpRecord,
#             "descRPAmt": descRPAmt,
#             "top10CheapestResaleFlat": top10CheapestResaleFlat}
#
# retrieve_Top10()


df = data_helper.get_dataframe()
print(df)
