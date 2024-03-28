import pandas as pd
from myapp.management.commands.preload import dataset
# pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
###

def cols_dataset():
    #data['Publisher Name'].value_counts() or data['Publisher Name'].unique() - ANIMATION
    return (dataset['Publisher Name'].describe(), dataset['Publisher Name'].value_counts(), dataset.Text.describe(), dataset['Textual Rating'].describe())
    # return data.describe()

def visualize_dataset():
    # Set the width and height of the figure
    plt.figure(figsize=(16,6))

    # Line chart showing how FIFA rankings evolved over time 
    sns.lineplot(data=dataset)

    # # sns.barplot(data=data)
    # # sns.heatmap(data=data)

    plt.savefig('static/lineplot.png')  # Save the plot as an image file

    # # # Save the plot as a temporary image file
    # # temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    # # plt.savefig(temp_file.name)
    # # plt.close()
    
    # # # Return the path to the temporary image file
    # # image_path = temp_file.name
    
    # # # Don't forget to delete the temporary file after serving it
    # # # temp_file.close()
    # # os.unlink(temp_file.name)
    
    # # return image_path