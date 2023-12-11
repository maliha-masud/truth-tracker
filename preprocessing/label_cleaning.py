import pandas as pd

#load file to be cleaned, and store as dataframe
existing_file_path = "pakistani_dataset_consolidated_augmented.xlsx"
df = pd.read_excel(existing_file_path)

#specify the classes to keep
allowed_classes = ['True', 'Half True', 'Misleading', 'Satire', 'Mostly False', 'False']

#filter the DataFrame to keep rows with allowed classes
df_filtered = df[df['Textual Rating'].isin(allowed_classes)]

#save the filtered DataFrame back to the same file
df_filtered.to_excel(existing_file_path, index=False)

#print count of each class
class_counts = df['Textual Rating'].value_counts()
print("Class Counts:")
print(class_counts)
