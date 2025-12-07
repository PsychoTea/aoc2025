
with open('input.txt', 'r') as f:
    lines = f.readlines()

total = 0

for line in lines:
    line = line.strip('\n')

    largest1 = 0
    idx1 = 0
    for i, c in enumerate(line[:-1]):
        val = int(c, 10)

        if val > largest1:
            largest1 = val 
            idx1 = i 

    largest2 = 0
    idx2 = 0
    for i, c in enumerate(line):
        if i <= idx1:
            continue 

        val = int(c, 10)

        if val > largest2:
            largest2 = val 
            idx2 = i 

    v = (largest1 * 10) + largest2

    print(f"{line} -> {v}")

    total += v

# answer = 17359
print(total)