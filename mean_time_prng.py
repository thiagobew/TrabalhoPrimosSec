def parse_mean_time(algorithm, bits):
    filename = f"results/time_{algorithm}_{bits}_bits.txt"
    try:
        with open(filename, "r") as file:
            data = file.readlines()
            parsed_data = {}
            for line in data:
                if line.startswith("Algorithm:"):
                    parsed_data["Algorithm"] = line.split(":")[1].strip()
                elif line.startswith("Bits:"):
                    parsed_data["Bits"] = int(line.split(":")[1].strip())
                elif line.startswith("Total Time:"):
                    parsed_data["Time"] = float(line.split(":")[1].strip().split()[0])
                elif line.startswith("Speed:"):
                    parsed_data["Speed"] = int(line.split(":")[1].strip().split()[0].replace(",", ""))
            return parsed_data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None

# Example usage
algorithms = ["lcg", "xorshift"]
bits = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

for algorithm in algorithms:
    for bit in bits:
        result = parse_mean_time(algorithm, bit)
        if result:
            mean_time_us = (result["Time"] / result["Speed"] * 1_000_000) if result["Speed"] > 0 else 0
            print(f"Algorithm: {result['Algorithm']}, Bits: {result['Bits']}, Mean Time: {mean_time_us:.6f} microseconds")