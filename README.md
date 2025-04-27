# PRNG and Prime Number Project

## Overview
This project consists of Python scripts for generating prime numbers and pseudo-random numbers (PRNG), as well as analyzing the PRNG results. The project is organized into the following components:

1. **`prime.py`**: Generates prime numbers and stores the results in the `prime_results` folder.
2. **`prng.py`**: Generates pseudo-random numbers and stores the results in the `results` folder.
3. **`uniform_test.py`**: Analyzes the uniformity of the PRNG results.
4. **`mean_time_prng.py`**: Analyzes the mean time performance of the PRNG.

## How to Run

### Generating Pseudo-Random Numbers
To generate pseudo-random numbers, run the `prng.py` script:
```bash
python3 prng.py
```

### Generating Prime Numbers
To generate prime numbers, run the `prime.py` script:
```bash
python3 prime.py
```
It also prints the generated numbers to the console with the time taken to generate them and the number of bits used. These results are stored in the `prime_results` folder.

### Analyzing PRNG Uniformity
To analyze the uniformity of the pseudo-random number generator, use the `uniform_test.py` script:
```bash
python3 uniform_test.py
```

### Analyzing PRNG Mean Time Performance
To evaluate the mean time performance of the pseudo-random number generator, execute the `mean_time_prng.py` script:
```bash
python3 mean_time_prng.py
```

## Folder Structure
The project directory is organized as follows:
```
/prime_results/    # Stores the generated prime numbers
/results/          # Stores the pseudo-random number outputs
```

## Requirements
Ensure you have Python 3 installed. Although the project is written in Python 3.12, it should work with earlier versions of Python 3 as well. Install the required packages by running:
```bash
pip install -r requirements.txt
```


