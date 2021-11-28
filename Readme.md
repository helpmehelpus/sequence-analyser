# Nucleobase analyser
This project contains scripts that create and analyse nucleobase sequences of adenine (A), cytosine (C),
guanine (G), and thymine (T), that make up portions of DNA strands in search for surprising sequences

Two scripts are present in this project:
* `generate_sequences.py`: Populates an `input` folder with `txt` files, each of which containing a 4096-char string
representing a segment of a DNA strand.
* `analyse_sequences.py`: Analyses the `input` folder, produces an `output/results.csv` file, and prints a brief
analysis to the console.

### Surprising Sequences
Our 4096-chars input segments of DNA are expected to contain roughly equal frequencies (25%) of the four nucleobases. 
In our context, an input string is considered surprising, and therefore a potential indicator of a sequence that can be
related to undesired gene expressions, if:
* The frequency of any specific nucleobase is equal to, or greater than 26,5%
* There exist sub-sequences with 32 or more consecutive occurrences of the same nucleobase
* The entire sequence is a palindrome, i.e., reading it from left to right yields the same string as reading it from right to
left.


We assume the input files have already been parsed and processed accordingly, so as to filter out malformed input data.
The output file is a `csv` sheet, whose columns are:
* `filename`: the name of the input file
* `freq_A`, `freq_B`, `freq_C`, `freq_D`, the frequencies of each nucleobase
* `is_surprising`, `is_imbalanced`, `has_consecutive`, `is_palindrome`: boolean values that indicate whether a given
string is surprising, and its respective surprising trait(s)

## Usage
The scripts require Python 3 to run. To generate data, run `python3 generate_sequences.py -N`, where `N` is the number 
of data points to be created. These points will rarely contain surprising sequences. To increase the odds of generating
surprising sequences, invoke the script with the optional argument -s:
* `python3 generate_sequences.py -50000 -s`

This will create an `input` folder, whose file names are the MD5 hashes of the respective 4096-char sequence. To analyse
the data, run `python3 analyse_sequences.py`. This will analyse the data and produce the file `/output/results.csv`, 
which contains data about each input string. The output of these scripts could be used downstream for visualization with
Pandas, Matplotlib, or for model training.