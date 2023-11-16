import pandas as pd

# Read excel file
df = pd.read_excel('pakistani_dataset_consolidated_augmented.xlsx')

# Display unique values in 'textual rating' column
print("Unique values:", df['Textual Rating'].unique())

# Replace misspellings or variations with the correct value
df['Textual Rating'] = df['Textual Rating'].replace(['FASLE', 'False.', 'FALSE', 'Fake'], 'False', regex=True)

# Save the modified DataFrame
df.to_excel('pakistani_dataset_consolidated_augmented.xlsx', index=False)

