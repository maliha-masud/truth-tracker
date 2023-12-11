import pandas as pd

#load file to be cleaned, and store as dataframe
existing_file_path = "pakistani_dataset_consolidated_augmented.xlsx"
df = pd.read_excel(existing_file_path)

#remove rows with duplicate URL rows
df = df.drop_duplicates(subset=['URL'])

#remove rows with no 'Text'
df = df.dropna(subset=['Text', 'Textual Rating'])

#append back into excel file
df.to_excel(existing_file_path, index=False)

#for cleaning after a specific index - split data based on index
# before_index = 12000
# df_before = df.iloc[:before_index]
# df_after = df.iloc[before_index:]
# df_after = df_after.drop_duplicates(subset=['URL'])
# df = pd.concat([df_before, df_after])