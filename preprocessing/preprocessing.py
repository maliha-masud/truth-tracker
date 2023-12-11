import pandas as pd

#load file to be cleaned, and store as dataframe
existing_file_path = "pakistani_dataset_consolidated_augmented.xlsx"
df = pd.read_excel(existing_file_path)

#define a dictionary for strict false replacements
#replace misspellings & variations with the correct value (False)
false_replacements = {
        'Fake': 'False', 'FALSE': 'False', 'FASLE': 'False', 'False.': 'False', 'false': 'False',
        'The claim is false. The video was actually a scene from a film called Load Wedding.': 'False',
        'False. The video used as evidence for this statement shows an attack on a church in Egypt in 2013.': 'False',
        'False: This is an Old Image of 2017': 'False', 'The picture in question is NOT from Kashmir.': 'False',
        'FAKE. It\'s morphed.': 'False', 'False: Famous Pak Chacha is alive.': 'False', 'False,': 'False',
        'Misleading and false.': 'False', 'FAKE': 'False', 'Altered Image': 'False', 'Incorrect': 'False',
        'The above is a FAKE vs REAL collage, it is clear that Mamata Banerjee and Imran Khan\'s faces were superimposed on the original picture using photo editing software.': 'False',
        'Pants on Fire': 'False', 'BJP MLAs in Punjab did not quit the party. The claim is false.': 'False',
        'Yanlış': 'False', 'Misleading and False': 'False', 'ALTERED IMAGE': 'False', 'Old Footage': 'False',
        'Picture is morphed.': 'False', 'False- The flag is of IUML Party': 'False', 'Baseless': 'False',
        'The video in question has been shared with the false claim.': 'False', 'Doctored image': 'False'
}
#apply strict replacements using the map method, leave rest of values as original
df['Textual Rating'] = df['Textual Rating'].map(false_replacements).fillna(df['Textual Rating'])

#Repeat for half-true
half_true_replacements = {'Half true': 'Half True', 'PARTLY TRUE': 'Half True', 'Partly True': 'Half True',
        'Partly': 'Half True', 'The horrific video in question is from Karachi, Pakistan and not from Hyderabad.': 'Half True'}
df['Textual Rating'] = df['Textual Rating'].map(half_true_replacements).fillna(df['Textual Rating'])

#Repeat for misleading
misleading_replacements = {'Misleading Claim': 'Misleading', 'Misleading,': 'Misleading',
        'Misleading: Google Translation from Urdu to English is incorrect.': 'Misleading',
        'The picture of the grave with flower bedding is not of Urdu poet Rahat Indori.': 'Misleading',
        'This is misleading.': 'Misleading', 'Milseading': 'Misleading',
        'The claim attached to the picture is true, but the picture is not recent as it was taken almost 17-years-ago. Hence, the post in question is misleading.': 'Misleading',
        'The man in the video is Russian.': 'Misleading',
        'Our investigation established that the video in question is five years old and it has no connection with the ongoing lockdown due to COVID-19.': 'Misleading',
        'Some studies have found that a disproportionate number of offenders and suspected offenders in child grooming gangs are categorised as being of Asian ethnicity and most don’t break this down any further so we can’t know if they are Pakistani. But all of the studies stress that the data isn’t good enough to know whether this is a true reflection of offenders in these cases.': 'Misleading'
        }
df['Textual Rating'] = df['Textual Rating'].map(misleading_replacements).fillna(df['Textual Rating'])

#Repeat for True
true_replacements = {'1': 'True', 'Mixture': 'True', 'In': 'True', 'Accurate': 'True', 'Not': 'True',
        'Since the WHO has advised people to wash hands frequently and use alcohol-based hand rubs and sanitizers as a preventive measure against the coronavirus, there is a shortage of hand sanitizers in many states in India. Some companies are trying to gain profits by fooling people.': 'True'}
df['Textual Rating'] = df['Textual Rating'].map(true_replacements).fillna(df['Textual Rating'])

#Repeat for Mostly False
mostly_false_replacements = {'Mostly false': 'Mostly False', 'Suspicious': 'Mostly False', 'Missing Context': 'Half True',
        'Mixed': 'Mostly False', 'Inaccurate': 'Mostly False', 'Partly false': 'Mostly False'}
df['Textual Rating'] = df['Textual Rating'].map(mostly_false_replacements).fillna(df['Textual Rating'])

#display unique values in 'textual rating' column
df['Textual Rating'] = df['Textual Rating'].str.title() #title: only first letter uppercase
print("Unique values:", df['Textual Rating'].unique())

#save the modified DataFrame
df.to_excel(existing_file_path, index=False)

