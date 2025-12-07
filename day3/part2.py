
with open('input.txt', 'r') as f:
    lines = f.readlines()

def find_largest(line, total, depth, start_idx, run_total):
    if depth == total:
        return run_total 

    cut = -total + depth + 1
    if cut == 0:
        line_s = line
    else:
        line_s = line[:cut]

    largest = 0
    idx = 0
    for i, c in enumerate(line_s):
        if i < start_idx:
            continue 

        val = int(c, 10)

        if val > largest:
            largest = val 
            idx = i 

    run_total *= 10
    run_total += largest 

    return find_largest(line, total, depth + 1, idx + 1, run_total)

total = 0

for line in lines:
    line = line.strip('\n')

    v = find_largest(line, 12, 0, 0, 0)

    print(f"{line} -> {v}")

    total += v

# answer = 172787336861064
print(f"{total} " + ("good" if total == 172787336861064 else "bad"))