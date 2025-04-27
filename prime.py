import random
import time
from pathlib import Path
from prng import lcg_numpy

# --- Primality Tests ---
# True if n is "probably prime", False if "composite"
def fermat_test(n: int, k: int = 5) -> bool:
    n = int(n)  # Ensure n is a Python integer
    if n <= 1:
        return False
    if n <= 3:
        return True
    for _ in range(k):
        a = random.randint(2, n - 1)  # Use Python's built-in random for large integers
        if pow(a, n - 1, n) != 1:  # Use modular exponentiation for efficiency
            return False
    return True

# True if n is "probably prime", False if "composite"
def miller_rabin_test(n: int, k: int = 5) -> bool:
    n = int(n)  # Ensure n is a Python integer
    
    # Base cases
    if n <= 1:
        return False
    if n <= 3:
        return True
    # Check if n is even
    if n % 2 == 0:
        return False
    
    # Factor n-1 as 2^s * d with d odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
        
    # Perform k iterations of the Miller-Rabin test
    for _ in range(k):
        # Choose a random base a in the range [1, n-1]
        a = random.randint(1, n - 1) 
        x = pow(a, d, n) # Modular exponentiation
        if x == 1:
            # Passed this iteration
            continue
        for i in range(s - 1):
            x = pow(x, pow(2, i)*d, n)
            if x == -1 % n:
                # Passed this iteration
                break
            else:
                # If we didn't break, n is composite
                return False
                
    # If we passed all iterations, n is probably prime
    return True

# --- Prime Search ---
def find_prime(algorithm: str, bits: int, output_dir: Path) -> None:
    seed = int(time.time())  # Unique seed per run
    gen = lcg_numpy(seed, bits)

    start_time = time.time()
    attempts = 0
    while True:
        num = int(next(gen)) | (1 << (bits - 1))  # Ensure the number has the correct bit length
        attempts += 1

        if algorithm == "fermat":
            # Benchmark Fermat test
            fermat_start = time.time()
            fermat_result = fermat_test(num, k= bits // 4)  # Use k = bits // 4, same as Miller-Rabin for fair comparison
            fermat_time = time.time() - fermat_start

            if fermat_result:
                elapsed = time.time() - start_time
                log_prime(num, algorithm, bits, attempts, elapsed, output_dir, fermat_time)
                break

        elif algorithm == "miller_rabin":
            # Benchmark Miller-Rabin test
            miller_rabin_start = time.time()
            miller_rabin_result = miller_rabin_test(num, k=bits // 4)  # Use k = bits // 4 for more accuracy
            miller_rabin_time = time.time() - miller_rabin_start

            if miller_rabin_result:
                elapsed = time.time() - start_time
                log_prime(num, algorithm, bits, attempts, elapsed, output_dir, miller_rabin_time)
                break

def log_prime(num: int, algorithm: str, bits: int, attempts: int, time_taken: float, output_dir: Path, time: float) -> None:
    output_file = output_dir / f"primes_{algorithm}_{bits}_bits.txt"
    with open(output_file, "a") as f:
        f.write(f"{num}\n")
    
    stats_file = output_dir / f"stats_{algorithm}_{bits}_bits.txt"
    with open(stats_file, "a") as f:
        f.write(
            f"Prime found: {num}\n"
            f"Algorithm: {algorithm}\n"
            f"Bits: {bits}\n"
            f"Attempts: {attempts}\n"
            f"Time: {time_taken:.15f} sec\n"
            f"Test Time: {time:.15f} sec\n"
            f"Speed: {attempts/time_taken:.0f} numbers/sec\n\n"
        )
    print(f"Prime found: {num} ({bits} bits, {algorithm}, {time_taken:.16f} sec)")

# --- Main ---
if __name__ == "__main__":
    output_dir = Path("prime_results")
    output_dir.mkdir(exist_ok=True)
    
    # Test configurations
    bit_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

    
    for bits in bit_sizes:
        find_prime("fermat", bits, output_dir)
        find_prime("miller_rabin", bits, output_dir)