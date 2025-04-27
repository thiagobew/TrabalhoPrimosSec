"""
Pseudo-Random Number Generator (PRNG) module implementing Linear Congruential Generator (LCG) and Xorshift algorithms.

This module provides generators for creating pseudo-random number sequences with configurable bit sizes.
Supports generation, saving, and parallel processing of random number sequences.

Key functions:
- lcg_numpy: Linear Congruential Generator with configurable parameters
- xorshift_numpy: Xorshift random number generator with adaptive shift parameters
- generate_and_save: Generates and saves random numbers with performance tracking
- run_generate_and_save: Wrapper for parallel generation of random numbers across different bit sizes

References:
    Marsaglia, G. (2003). Xorshift RNGs. Journal of Statistical Software, 8(14), 1-6.
"""
from collections.abc import Generator
import time
import multiprocessing

def lcg_numpy(seed: int, bits: int = 4096, a: int = 1103515245, c: int = 12345) -> Generator[int, None, None]:
    # Modulus is 2^bits
    # a and c are constants for the LCG
    # a = 1103515245, c = 12345 are common values for LCG, used in glibc
    modulus = 1 << bits
    state = seed % modulus  # Ensure the seed is within the modulus
    
    while True:
        state = (a * state + c) % modulus
        yield state

def choose_xorshift_parameters(bits: int) -> tuple[int, int, int]:
    """
    Seleciona parâmetros de deslocamento (shifts) para geradores Xorshift baseados no tamanho em bits.
    
    Os parâmetros para 32, 64, 96 e 128 bits são derivados diretamente do trabalho original de Marsaglia :cite[3],
    enquanto valores para tamanhos maiores são extrapolações baseadas nos mesmos princípios.
    
    Args:
        bits: Tamanho do estado interno em bits (32, 64, 96, 128 ou maior)
        
    Returns:
        Tupla (shift1, shift2, shift3) contendo os parâmetros de deslocamento recomendados
    
    Reference:
        Marsaglia, G. (2003). Xorshift RNGs. Journal of Statistical Software, 8(14), 1-6.
        https://www.jstatsoft.org/article/view/v008i14 :cite[1]:cite[3]
    """
    # Canonical parameters from the original paper :cite[3]
    if bits <= 32:
        return 13, 17, 5  # 32-bit version (xor32) :cite[3]
    elif bits <= 64:
        return 13, 7, 17   # 64-bit version (xor64) :cite[3]
    elif bits <= 96:
        return 10, 5, 26   # Adapted for 96-bit based on observed patterns
    elif bits <= 128:
        return 5, 14, 1    # 128-bit version (xor128) :cite[3]
    else:
        # Heuristic for larger sizes (>128 bits):
        # Prime divisors proportional to the state size,
        # maintaining the proportion of the original parameters :cite[3]
        shift1 = bits // 3  # ~1/3 of the size (equivalent to 13/32 for 32-bit)
        shift2 = bits // 2  # ~1/2 of the size (equivalent to 17/32)
        shift3 = bits // 5  # ~1/5 of the size (equivalent to 5/32)
        return shift1, shift2, shift3

def xorshift_numpy(seed: int, bits: int = 4096) -> Generator[int, None, None]:
    state = seed & ((1 << bits) - 1)  # Ensure the seed fits within the specified bits
    
    shift1, shift2, shift3 = choose_xorshift_parameters(bits)

    while True:
        # Xorshift steps
        state ^= (state << shift1) & ((1 << bits) - 1)
        state ^= (state >> shift2) & ((1 << bits) - 1)
        state ^= (state << shift3) & ((1 << bits) - 1)
        yield state

def generate_and_save(algorithm, seed, bits, iterations, filename_prefix):
    # Initialize generator
    if algorithm == "lcg":
        gen = lcg_numpy(seed, bits)
    elif algorithm == "xorshift":
        gen = xorshift_numpy(seed, bits)
    else:
        raise ValueError("Algorithm must be 'lcg' or 'xorshift'")
    
    # Generate and save numbers in batches
    output_file = f"results/{filename_prefix}_{algorithm}_{bits}_bits.txt"
    time_file = f"results/time_{algorithm}_{bits}_bits.txt"
    
    batch_size = 1000
    num_batches = iterations // batch_size
    remaining = iterations % batch_size
    batch_times = []
    with open(output_file, "w") as f:
        for _ in range(num_batches):
            batch_start_time = time.time()
            batch = [next(gen) for _ in range(batch_size)]
            batch_elapsed = time.time() - batch_start_time
            batch_times.append(batch_elapsed)
            f.writelines(f"{num}\n" for num in batch)
        
        # Handle remaining iterations
        if remaining > 0:
            batch_start_time = time.time()
            batch = [next(gen) for _ in range(remaining)]
            batch_elapsed = time.time() - batch_start_time
            f.writelines(f"{num}\n" for num in batch)
            batch_times.append(batch_elapsed)
    
    total_time = sum(batch_times)
    avg_batch_time = total_time / len(batch_times) if batch_times else 0
    speed = iterations / total_time if total_time > 0 else 0
    with open(time_file, "w") as f:
        f.write(f"Algorithm: {algorithm}\n")
        f.write(f"Bits: {bits}\n")
        f.write(f"Total Time: {total_time:.15f} sec\n")
        f.write(f"Average Batch Time: {avg_batch_time:.15f} sec\n")
        f.write(f"Speed: {speed:.0f} numbers/sec\n")
    
    print(f"Data saved to {output_file}, time logged to {time_file}")

# Example usage with parallelization
def run_generate_and_save(bits):
    # Use a combination of current time and process ID for a more unique seed
    current_time_seed = int(time.time()) ^ (multiprocessing.current_process().pid)
    generate_and_save("lcg", seed=current_time_seed, bits=bits, iterations=500_000, filename_prefix="prng")
    generate_and_save("xorshift", seed=current_time_seed, bits=bits, iterations=500_000, filename_prefix="prng")

if __name__ == "__main__":
    bit_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    num_cores = multiprocessing.cpu_count()
    
    with multiprocessing.Pool(num_cores) as pool:
        pool.map(run_generate_and_save, bit_sizes)