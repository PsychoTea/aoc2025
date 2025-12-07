import math 

with open('input.txt', 'r') as f:
    lines = f.readlines()

# parse the operations, recording how wide each column is 
ops = [ ]
col_widths = [ ]
curr_col = -1
for op in lines[-1]:
    if op != '*' and op != '+':
        col_widths[curr_col] += 1
        continue 

    ops.append(op)
    col_widths.append(0)
    curr_col += 1

col_widths[-1] += 1

orig_numbers = [ ]
col_idx = 0

# parse the actual data
for l in lines[:-1]:
    col_idx = 0
    l = l.strip('\n')

    arr = [ ]

    for col in col_widths:
        # grab c characters from the line 
        chars = l[col_idx:col_idx + col]

        chars = chars.replace(" ", "0")

        col_idx += col + 1

        arr.append(int(chars, 10))

    orig_numbers.append(arr)

# reverse matrix
numbers = [ ]

for i, op in enumerate(ops):
    nums = [ ]

    for j in range(len(orig_numbers)):
        nums.append(orig_numbers[j][i])

    numbers.append(nums)

print(f"{numbers=}")

new_numbers = [ ]

for col in numbers:
    width = len(str(col))

    new_digs = []

    for dig in range(width):
        num = 0

        for i, item in enumerate(col):
            # grab each digit
            if (item % 10) > 0:
                num *= 10
                num += item % 10
            col[i] = math.floor(item / 10)

        if num != 0:
            new_digs.append(num)

    new_numbers.append(new_digs)

print(f"{new_numbers=}")

sums = [ ]

# apply given operation to each column
for i, op in enumerate(ops):
    sumX = 0

    if op == '*':
        sumX = 1

        for value in new_numbers[i]:
            sumX *= value 

        sums.append(sumX)

    if op == '+':
        sumX = 0

        for value in new_numbers[i]:
            sumX += value 

        sums.append(sumX)

print(sum(sums))
