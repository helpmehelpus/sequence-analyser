import argparse
import hashlib
import os
import random
import sys

from pathlib import Path

import string

INPUT_PATH = '../input/'
SEQUENCE_SIZE = 4096
POSSIBLE_NUCLEOBASES = ['A', 'C', 'G', 'T']
IMBALANCE = [[35, 25, 25, 15], [15, 35, 25, 25], [25, 15, 35, 25], [25, 25, 15, 35]]


def generate_sequence():
    sequence = ''.join(random.choices(POSSIBLE_NUCLEOBASES, k=SEQUENCE_SIZE))
    store_sequence(sequence)


def generate_imbalanced_sequence():
    sequence = ''.join(random.choices(POSSIBLE_NUCLEOBASES, weights=random.choice(IMBALANCE), k=SEQUENCE_SIZE))
    store_sequence(sequence)


def generate_consecutive_sequence():
    first_part_length = random.randint(1, 3850)
    first_part = ''.join(random.choices(POSSIBLE_NUCLEOBASES, k=first_part_length))

    consecutive_part_length = random.randint(32, 200)
    consecutive_nucleobase = random.randint(0, 3)
    consecutive_part = ''.join(POSSIBLE_NUCLEOBASES[consecutive_nucleobase] for x in range(consecutive_part_length))

    final_part_length = SEQUENCE_SIZE - first_part_length - consecutive_part_length
    final_part = ''.join(random.choices(POSSIBLE_NUCLEOBASES, k=final_part_length))

    sequence = first_part + consecutive_part + final_part
    store_sequence(sequence)


def generate_palindrome_sequence():
    first_part = ''.join(random.choices(POSSIBLE_NUCLEOBASES, k=(SEQUENCE_SIZE // 2)))
    second_part = first_part[::-1]
    sequence = first_part + second_part
    store_sequence(sequence)


def store_sequence(sequence):
    if not os.path.exists(INPUT_PATH):
        os.makedirs(INPUT_PATH)
    file_name = os.path.join(INPUT_PATH, hashlib.md5(sequence.encode('utf-8')).hexdigest() + '.txt')
    if os.path.isfile(file_name) is True:
        print("Sequence already exists, skipping creation")
        return
    else:
        file_name = os.path.join(Path.cwd(), file_name)
        fp = open(file_name, 'x')
        fp.write(sequence)
        fp.close()


def generate_batch(number_of_entries, surprisal=False):
    for x in range(number_of_entries):
        if surprisal:
            chance = random.uniform(0, 1)
            if 0 <= chance < 0.1:
                generate_imbalanced_sequence()
            elif 0.1 <= chance < 0.2:
                generate_consecutive_sequence()
            elif 0.2 <= chance < 0.3:
                generate_palindrome_sequence()
            else:
                generate_sequence()
        else:
            generate_sequence()
    print("Generated entries: ", number_of_entries)


parser = argparse.ArgumentParser(description='Generate input data for surprisal analysis')
parser.add_argument('BatchSize',
                    metavar='batch_size',
                    type=str,
                    help='the number of data to create')
parser.add_argument('-s',
                    '--surprisal',
                    action='store_true',
                    help='increase the chances of generating surprising sequences')

args = parser.parse_args()
batch_size = int(args.BatchSize)

if args.surprisal:
    generate_batch(batch_size, surprisal=True)
else:
    generate_batch(batch_size)
