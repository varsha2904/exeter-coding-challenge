import pandas as pd
import time
import os
import psutil
import re

start_time = time.time()

input_file_path = r'C:\Users\Varsha.Unnikrishnan\PycharmProjects\test_run\input_files\t8.shakespeare.txt'
words_file = r'C:\Users\Varsha.Unnikrishnan\PycharmProjects\test_run\input_files\find_words.txt'
dict_path = r'C:\Users\Varsha.Unnikrishnan\PycharmProjects\test_run\input_files\french_dictionary.csv'
output_file_path = r'C:\Users\Varsha.Unnikrishnan\PycharmProjects\test_run\output\t8.shakespeare.translated.txt'
frequency_path = r'C:\Users\Varsha.Unnikrishnan\PycharmProjects\test_run\output\frequency.csv'
performance_path = r'C:\Users\Varsha.Unnikrishnan\PycharmProjects\test_run\output\performance.txt'

# Read input file
with open(input_file_path, encoding='utf-8', mode='r') as file:
    lines = file.read()


# Read words to be translated
df_words = pd.read_csv(words_file, header=None)
words_list = df_words[0].to_list()


# Read dictionary
df = pd.read_csv(dict_path, header=None, names=['English word', 'French word'])
df_frequency = df.to_dict(orient='records')
french_dict = dict(zip(df['English word'], df['French word']))


# Translating given english words to french
result_list = []
for word in words_list:
    if word in lines:
        lines, count_lower = re.subn(r'\b{0}\b'.format(word), french_dict[word], lines)
        lines, count_upper = re.subn(r'\b{0}\b'.format(word.upper()), french_dict[word].upper(), lines)
        lines, count_capital = re.subn(r'\b{0}\b'.format(word.capitalize()), french_dict[word].capitalize(), lines)
        result_list.extend([dict(entry, Frequency=count_lower+count_upper+count_capital)
                           for entry in df_frequency if entry['English word'] == word])

# Writing the translated file
with open(output_file_path, encoding='utf-8', mode='w') as file:
    file.write(lines)


# Writing the file with frequency details
df_frequency = pd.DataFrame(result_list)
df_frequency.to_csv(frequency_path, index=False)


# Calculation for memory used
process = psutil.Process(os.getpid())
memory_used = process.memory_info().rss//1024 ** 2
process_memory = 'Memory used: {0} MB'.format(memory_used)


# Calculation for time taken
end_time = time.time()
time_taken = end_time - start_time
seconds = time_taken % (24 * 3600)
minutes = time_taken // 60
performance = "Time to process: {0} minutes {1} seconds".format(minutes, seconds) + '\n' + process_memory


# Writing the file with performance details
with open(performance_path, encoding='utf-8', mode='w') as file:
    file.write(performance)
