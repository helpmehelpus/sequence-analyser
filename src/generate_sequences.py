import argparse
import hashlib
import os
import random

from pathlib import Path

INPUT_PATH = '../input/'
SEQUENCE_SIZE = 4096
POSSIBLE_NUCLEOBASES = ['A', 'C', 'G', 'T']


def generate_batch(number_of_entries, surprisal=False):
    for x in range(number_of_entries):
        if surprisal:
            chance = random.uniform(0, 1)
            if 0 <= chance < 0.125:
                generate_random_sequence()
            elif 0.125 <= chance < 0.25:
                generate_consecutive_sequence()
            else:
                generate_balanced_sequence()
        else:
            generate_balanced_sequence()
    print("Generated entries: ", number_of_entries)


def generate_balanced_sequence():
    sequence = ''.join(random.choices(POSSIBLE_NUCLEOBASES, k=SEQUENCE_SIZE))
    store_sequence(sequence)


def generate_random_sequence():
    sequence = ''.join(random.choices(POSSIBLE_NUCLEOBASES, weights=generate_random_weights(), k=SEQUENCE_SIZE))
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


def generate_random_weights():
    total = 100
    imbalanced_weights = []
    for i in range(3):
        upper_bound = total - (4 - i - 1)
        if upper_bound == 1:
            imbalanced_weights.append(upper_bound)
            total -= 1
            continue
        weight = random.randint(1, upper_bound)
        imbalanced_weights.append(weight)
        total -= weight

    imbalanced_weights.append(total)
    return imbalanced_weights


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


def check_positive(value):
    int_value = int(value)
    if int_value <= 0:
        raise argparse.ArgumentTypeError(f'{value} is a negative number. Please supply a positive integer.')
    return int_value


parser = argparse.ArgumentParser(description='Generate input data for surprisal analysis')
parser.add_argument('BatchSize',
                    metavar='batch_size',
                    type=check_positive,
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
