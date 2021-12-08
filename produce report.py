import pandas as pd

df = pd.read_csv("assets/Sample Call Data Clean.csv")
disposition_reference_df = pd.read_excel("assets/Disposition Definitions.xlsx")

dates = sorted(set(df["Call Date"]))
dispositions = sorted(set(disposition_reference_df["CHQ Disposition"]))
disposition_count_dict = {}
for disposition in dispositions:
    for date in dates:
        if disposition in disposition_count_dict.keys():
            disposition_count_dict[disposition].append(df[(df["Call Date"] == date) &
                                                          (df["Disposition"] == disposition)].shape[0])
        else:
            disposition_count_dict[disposition] = [df[(df["Call Date"] == date) &
                                                      (df["Disposition"] == disposition)].shape[0]]
    disposition_count_dict[disposition].insert(0, sum(disposition_count_dict[disposition]))
Q1_answers = sorted(set(df[df["Q1"].notnull()]["Q1"]))
Q1_answers_count_dict = {}
for Q1_answer in Q1_answers:
    for date in dates:
        if Q1_answer in Q1_answers_count_dict.keys():
            Q1_answers_count_dict[Q1_answer].append(df[(df["Call Date"] == date) & (df["Q1"] == Q1_answer)].shape[0])
        else:
            Q1_answers_count_dict[Q1_answer] = [df[(df["Call Date"] == date) & (df["Q1"] == Q1_answer)].shape[0]]
    Q1_answers_count_dict[Q1_answer].insert(0, sum(Q1_answers_count_dict[Q1_answer]))
dates.insert(0, "Total")

dispositions_label = pd.DataFrame(index=["Dispositions"], columns=dates)
dispositions_df = pd.DataFrame(disposition_count_dict.values(), index=disposition_count_dict.keys(), columns=dates)
Q1_answers_label = pd.DataFrame(index=["Q1 Responses"], columns=dates)
Q1_answers_df = pd.DataFrame(Q1_answers_count_dict.values(), index=Q1_answers_count_dict.keys(), columns=dates)
insert_target = pd.Series(name='NameOfNewRow')
output = dispositions_label.append(dispositions_df).append(Q1_answers_label).append(Q1_answers_df)
output.to_excel("assets/Generated Report.xlsx")