
with open('input.txt') as f:
    lines = f.readlines()

ops = [ ]

# parse the operations and column widths 
for c in lines[-1]:
    if c == '*' or c == '+':
        ops.append([c, 0])
        continue 

    ops[-1][1] += 1

# correct for the last column 
ops[-1][1] += 1

all_values = [ ]

offset = 0
for x in range(len(ops)):
    col_values = [ ]

    for i in range(ops[x][1] - 1, -1, -1):
        digits = [ ]
        for y in range(len(lines) - 1):
            char = lines[y][offset + i]

            digits.append(char)

        col_values.append(digits)

    print(col_values)

    offset += ops[x][1] + 1

    all_values.append(col_values)

def coalesce_number(arr):
    number = 0

    for digit in arr:
        if digit == ' ':
            continue 

        number *= 10
        number += int(digit)

    return number 

def coalesce_array(arr):
    out = [ ] 
    for item in arr:
        out.append(coalesce_number(item))

    return out 

final_values = [coalesce_array(x) for x in all_values]

total = 0

for (i, op) in enumerate(ops):
    sum = 0

    if op[0] == '*':
        sum = 1
        for value in final_values[i]:
            sum *= value 

    elif op[0] == '+':
        for value in final_values[i]:
            sum += value 

    total += sum 

print(total)

# input2.txt = 3263827
# input.txt = 9029931401920
