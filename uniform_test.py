import numpy as np
import os
from scipy.stats import chisquare

algorithms = ["lcg", "xorshift"]
bits = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

# Base directory for the files
base_dir = '/home/thiago-bewiahn/Desktop/sec_ufsc/primos/results'

# Log results
results = []

# Iterate over algorithms and bit sizes
for algorithm in algorithms:
    for bit_size in bits:
        file_path = os.path.join(base_dir, f'prng_{algorithm}_{bit_size}_bits.txt')
        
        if not os.path.exists(file_path):
            results.append(f"File not found: {file_path}")
            continue

        # Read numbers from the file
        with open(file_path, 'r') as file:
            numbers = [int(line.strip()) for line in file]

        # Perform Chi-Square Goodness-of-Fit test
        min_val, max_val = min(numbers), max(numbers)
        num_bins = int(np.ceil(1 + 3.322 * np.log10(len(numbers))))  # Sturges' formula
        bin_width = (max_val - min_val) // num_bins
        observed_counts = [0] * num_bins

        for number in numbers:
            bin_index = min(int((number - min_val) / bin_width), num_bins - 1)
            observed_counts[bin_index] += 1

        expected_count = len(numbers) / num_bins
        expected_counts = [expected_count] * num_bins

        chi2_stat = sum(
            (obs - exp) ** 2 / exp for obs, exp in zip(observed_counts, expected_counts)
        )
        p_value = chisquare(f_obs=observed_counts, f_exp=expected_counts).pvalue

        # Log the results
        result = (
            f"Algorithm: {algorithm}, Bits: {bit_size}\n"
            f"Chi-Square Statistic: {chi2_stat}, P-Value: {p_value}\n"
            f"{'Fail to reject the null hypothesis: The distribution is uniform.' if p_value > 0.05 else 'Reject the null hypothesis: The distribution is not uniform.'}\n"
        )
        results.append(result)

# Print all results
for result in results:
    print(result)