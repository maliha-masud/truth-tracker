import pandas as pd

#original dataset file
existing_file_path = "pakistani_dataset_consolidated_augmented.xlsx"
df_existing = pd.read_excel(existing_file_path)

#dataset file to add to original
new_dataset_file_path = "Detection_Fake_1120.xlsx"
df_new = pd.read_excel(new_dataset_file_path)

#filter dates after a specified cutoff: July 2021
df_new['Published_ Date'] = pd.to_datetime(df_new['Published_ Date'], format='%d-%m-%Y')
cutoff_date = pd.to_datetime('2021-07-01')
df_new = df_new[df_new['Published_ Date'] > cutoff_date]

#map columns
column_mapping = {
    'News_Title': 'Title',
    'News_Text': 'Text',
    'Published_ Date': 'Review Date',
    'Source': 'Publisher Name',
    'Source_URL': 'URL',
    'Author': 'Author',
    'Label': 'Textual Rating'
}

#assign columns new names according to mapping
df_new = df_new.rename(columns=column_mapping)

#reorder columns
desired_column_order = [
    "Title", "Text", "Review Date", "Publisher Name", "URL", "Author", "Textual Rating"
]

df_new = df_new[desired_column_order]

#append existing file with new data
result_df = pd.concat([df_existing, df_new], ignore_index=True)

#replace original file with appended one
result_df.to_excel(existing_file_path, index=False)
