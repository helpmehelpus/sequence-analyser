import hashlib
import csv
import os
import shutil
import random
import sys

from pathlib import Path

INPUT_PATH = '../input/'
OUTPUT_PATH = '../output/'
SEQUENCE_SIZE = 4096
FREQUENCY_BALANCE_THRESHOLD = 0.265


def analyse_input():
    if not os.path.exists(INPUT_PATH):
        print("No input data present. Please generate data first")
        return
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(os.path.join(Path.cwd(), OUTPUT_PATH))
    os.makedirs(OUTPUT_PATH)
    output_file_name = os.path.join(OUTPUT_PATH, 'results.csv')

    with open(output_file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'freq_A', 'freq_B', 'freq_C', 'fred_D', 'is_surprising', 'is_imbalanced',
                         'has_consecutive', 'is_palindrome'])

        for dir_name, subdir_list, file_list in os.walk(INPUT_PATH):
            if len(file_list) == 0:
                print("Input folder is empty. Please generate data first")
                return
            for file_name in file_list:
                file_path = os.path.join(INPUT_PATH, file_name)
                with open(file_path, 'r') as file:
                    sequence = file.read()
                    sequence_data = analyse_sequence(sequence)
                    sequence_data.insert(0, file_name)
                    writer.writerow(sequence_data)
                    file.close()


def analyse_sequence(sequence):
    frequencies = calculate_frequencies(sequence)
    is_imbalanced = has_imbalanced_frequencies(frequencies)
    has_consecutive_subsequence = has_consecutive_nucleobases(sequence)
    is_a_palindrome = is_palindrome(sequence)
    is_surprising = is_imbalanced or has_consecutive_subsequence or is_a_palindrome
    return [frequencies['A'], frequencies['C'], frequencies['G'], frequencies['T'], is_surprising, is_imbalanced,
            has_consecutive_subsequence, is_a_palindrome]


def analyse_results():
    output_file_name = os.path.join(OUTPUT_PATH, 'results.csv')
    with open(output_file_name, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        line_count = -1
        surprising_count = imbalanced_count = has_consecutive_count = palindrome_count = 0
        for row in reader:
            if line_count == -1:
                print("File header is: ", row)
                line_count += 1
            else:
                line_count += 1
                if row[5] == 'True':
                    surprising_count += 1
                if row[6] == 'True':
                    imbalanced_count += 1
                if row[7] == 'True':
                    has_consecutive_count += 1
                if row[8] == 'True':
                    palindrome_count += 1

        print("Finished analysing input data. Number of entries: ", line_count)
        print(f'Surprising entries: {surprising_count}. Surprising data frequency: {surprising_count / line_count}')
        print(f'Imbalanced entries: {imbalanced_count}. Imbalanced data frequency: {imbalanced_count / line_count}')
        print(f'Entries with long single-base sequences: {has_consecutive_count}. Long single-base data frequency:'
              f' {has_consecutive_count / line_count}')
        print(f'Palindrome entries: {palindrome_count}. Palindrome data frequency: {palindrome_count / line_count}')


def calculate_frequencies(sequence):
    frequencies = {
        'A': 0,
        'C': 0,
        'G': 0,
        'T': 0
    }
    for i, v in enumerate(sequence):
        frequencies[v] += 1

    for k, v in frequencies.items():
        frequencies[k] = frequencies[k] / SEQUENCE_SIZE

    return frequencies


def has_imbalanced_frequencies(frequencies):
    for k, v in frequencies.items():
        if frequencies[k] >= FREQUENCY_BALANCE_THRESHOLD:
            return True
    return False


def has_consecutive_nucleobases(sequence):
    return 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' in sequence or 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC' in sequence or \
           'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG' in sequence or 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT' in sequence


def is_palindrome(sequence):
    for element in range(0, len(sequence) // 2):
        if sequence[element] != sequence[SEQUENCE_SIZE - element - 1]:
            return False
    return True


analyse_input()
analyse_results()
