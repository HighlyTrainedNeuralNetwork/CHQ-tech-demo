import pandas as pd
from dateutil import parser

df = pd.read_csv("assets/Sample Call Data.csv")
disposition_reference_df = pd.read_excel("assets/Disposition Definitions.xlsx")
call_center_dispositions = disposition_reference_df["Call Center Disposition"].tolist()
CHQ_dispositions = disposition_reference_df["CHQ Disposition"].tolist()
disposition_dict = {}
for call_center_disposition, CHQ_disposition in zip(call_center_dispositions, CHQ_dispositions):
    disposition_dict[call_center_disposition] = CHQ_disposition
unique_ids = []
int_conversion_dict = {"1": "Yes", "2": "No", "3": "Undecided", "4": "Refused"}

# remove incomplete rows
df.dropna(inplace=True, subset=["ID", "Congressional District", "Call Date", "Disposition"])
# enforce integer type for ID and Congressional District columns
df["ID"] = df["ID"].astype(int)
df["Congressional District"] = df["Congressional District"].astype(int)

# iterate through each row
for index, row in df.iterrows():
    # enforce unique ID values for ID column
    if row["ID"] not in unique_ids:
        unique_ids.append(row["ID"])
    else:
        new_val = row["ID"].max() + 1
        df.at[index, "ID"] = new_val
        unique_ids.append(new_val)
    # enforce correct date format for Call Date column
    datetime_date = parser.parse(row["Call Date"]).strftime("%m/%d/%Y")
    df.at[index, "Call Date"] = datetime_date
    # enforce standard disposition for Disposition column
    if row["Disposition"] in disposition_dict.keys():
        df.at[index, "Disposition"] = disposition_dict[row["Disposition"]]
    # account for integers in response for Q1 column
    if not pd.isnull(row["Q1"]) and row["Q1"][0] in int_conversion_dict.keys():
        df.at[index, "Q1"] = int_conversion_dict[row["Q1"][0]]

df.to_csv("assets/Sample Call Data Clean.csv", index=False)