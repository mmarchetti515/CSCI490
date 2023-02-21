"""" #! /usr/bin/python3 """
import collections as collections
import os
import re
import sys

import nltk as nltk
import numpy as np
import pandas as pd

# 'global' variables
records = 0    # needs to be defined as global later on because it will be modified
invalid_chars = ['\n', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', '[', ']', '_', '—', '‘', '’', '“', '”', '\ufeff']
file_name = "74-2021-0329.txt"

def clean_file():
    # global vars aren't necessarily great, but it works in this specific use case
    global records
    open_in_read = open(file_name, 'r', encoding='utf-8')

    replacements = open_in_read.read()     
    for characters in replacements:
        # replace all invalid chars with space
        if characters in invalid_chars:
            replacements = replacements.replace(characters, ' ')
            # while we're cleaning the file, we need to keep track of our record count
            # this is done under this loop to reduce the amount of times we check for endlines, since
            # we only have endlines in invalid chars
            if characters == invalid_chars[0]:
                records += 1
        # clean upper case letters into lower case        
        elif characters.isupper():
            replacements = replacements.replace(characters, characters.lower())
    # close file to allow for access in write mode
    open_in_read.close()
    # this segment rewrites the cleaned file
    open_in_write = open(file_name, 'w', encoding='utf-8')
    open_in_write.write(replacements)
    open_in_write.close()

# total num chars counting spaces
def chars_read():
    read_cleaned_data = open("74-2021-0329.txt", "r")
    char_read_prep = read_cleaned_data.read()
    char_read = len(char_read_prep)
    return char_read

# total num chars without counting spaces
def chars_counted():
    read_cleaned_data = open("74-2021-0329.txt", "r")
    char_counted_prep = read_cleaned_data.read().replace(" ","")
    char_counted = len(char_counted_prep)
    return char_counted

#
def word_frequencies():
    read_unique_words = open("74-2021-0329.txt", "r")
    cleaned_unique_words = read_unique_words.read().split(None) # just changed from ' '
    df = pd.value_counts(np.array(cleaned_unique_words))
    read_unique_words.close()
    return df

# used to help determine frequency infomation in printing to stdout function
def length_information():
    len_longest_word = len(max(word_frequencies().index, key = len))
    word_len = {}
    for i in range(len_longest_word + 1):
        word_len[i] = 0
    # read all words again
    read_all_words = open("74-2021-0329.txt", "r")
    arr_words = read_all_words.read().split(None)
    read_all_words.close()
    for word in arr_words:
        temp = len(word)
        word_len[temp] += 1
    
    # sorting algoritm that sorts the values in reversed order
    word_len = {length: freq for length, freq in sorted(word_len.items(), key=lambda item: item[1], reverse=True)}
    # remove the (0:0) item from the end of the dict
    word_len.popitem()
    return word_len

# print to stdout, includes some calculations
def output():
    # defining this early on since it will be used multiple times in the function
    # this sorts our dictionary first by freq desc, then word asc
    rev_sorted_word_frequencies = {length: freq for length, freq in sorted(word_frequencies().items(), key=lambda item: (-item[1], item[0]))}
    # print arguments information
    print(f"no. of arguments =  {len(sys.argv)}")
    print(f"arguments are:  {sys.argv}")

    # print 16+ length words 
    print("\nwords of length 16 or more:")
    for word in sorted(word_frequencies().index):
        if len(word) >= 16:
            print("*** ", word)

    # print rank - length - freq - rank*freq information
    rank = 1
    freq_total = 0
    key_list = list(length_information().keys())
    print("\n\nrank  length     freq   rank*freq")
    for freq in length_information().values():
        print('{:4}'.format(rank), '{:7}'.format(key_list[rank-1]), '{:9}'.format(freq), '{:8}'.format(freq*rank))
        rank += 1
        freq_total += freq
    print("\nTotal", '{:12}'.format(freq_total))

    # next sub-section
    print("\n\nInvalid chars:      ", invalid_chars)
    print("\nRecords read:", '{:16}'.format(records))
    print("Characters read:", '{:13}'.format(chars_read()))
    print("Characters counted:", '{:10}'.format(chars_counted()))
    print("Words counted:", '{:15}'.format(freq_total))
    print("Distinct words:", '{:15}'.format(len(word_frequencies().index)))
    dist_word_freq = collections.Counter(rev_sorted_word_frequencies.values())
    print("Distinct word freqs:" '{:10}'.format(len(dist_word_freq)))

    # Frequency of frequencies preprocessing
    freq_table = {}
    for val in rev_sorted_word_frequencies.values():
        if val in freq_table:
            freq_table[val] += 1
        else:
            freq_table[val] = 1
    
    # Frequency of frequencies information
    print("\n\nFREQUENCY OF FREQUENCIES (DESCENDING)")
    print("Shows that 50% of all words only occur once")
    print("But those words only cover 5% of the corpus")
    print('"Most words are rare"\n')
    print("  #    freq   count  cum distinct words cum distinct %  cum words  cum word %")
    rank_freq = 1
    sorted_freq_table = {length: freq for length, freq in sorted(freq_table.items(), key=lambda item: (-item[1], item[0]))}
    sum_distinct_word = sum(sorted_freq_table.values())
    for freq,count in sorted_freq_table.items():
        if rank_freq == 1:
            print('{:3}'.format(rank_freq), '{:7}'.format(freq), '{:7}'.format(count), '{:10}'.format(count), '{:17.2f}'.format((count)/sum_distinct_word), '{:15}'.format(count), '{:15.2f}'.format(count/freq_total))
            temp = count
            temp_cum = count
            rank_freq += 1
        else:
            temp_cum = temp_cum + (count * freq)
            print('{:3}'.format(rank_freq), '{:7}'.format(freq), '{:7}'.format(count), '{:10}'.format(count+temp), '{:17.2f}'.format((count+temp)/sum_distinct_word), '{:15}'.format(temp_cum), '{:15.2f}'.format((temp_cum)/freq_total))
            temp += count
            rank_freq += 1
    print("\n\nWORD FREQUENCIES AND ZIPF'S LAW")
    print("Note that you can read 2/3 of the words in the book with only 200 words of English.")
    print("Can you understand a book if you only know 200 words of English?\n")
    print("rank   word               freq    rank*freq   cum words  cum word %")
    rank_zipf = 1
  
    sum_word = sum(rev_sorted_word_frequencies.values())
    for word,occurs in rev_sorted_word_frequencies.items():
        if rank_zipf == 1:
            print('{:4}'.format(rank_zipf), ' ', '{:<18}'.format(word), '{:4}'.format(occurs), '{:10}'.format(occurs*rank_zipf), '{:10}'.format(occurs), '{:10.2f}'.format((occurs)/sum_word))
            temp = occurs
            rank_zipf += 1
        else:
            print('{:4}'.format(rank_zipf), ' ', '{:<18}'.format(word), '{:4}'.format(occurs), '{:10}'.format(occurs*rank_zipf), '{:10}'.format(occurs+temp), '{:10.2f}'.format((occurs+temp)/sum_word))
            temp += occurs
            rank_zipf += 1

clean_file()
output()