
def part1(input):
    ranges = input.split(',')

    all_ids = [ ] 

    for id_range in ranges:
        parts = id_range.split('-')

        lower = int(parts[0], 10)
        upper = int(parts[1], 10)

        for id in range(lower, upper + 1):
            all_ids.append(id)

    dupes = [ ] 

    for id in all_ids:
        s = str(id)

        part1, part2 = s[:len(s)//2], s[len(s)//2:]

        if part1 == part2:
            dupes.append(id)

    answer = sum(dupes)

    print(f"answer: {answer}")

def part2(input):
    ranges = input.split(',')

    all_ids = [ ] 

    for id_range in ranges:
        parts = id_range.split('-')

        lower = int(parts[0], 10)
        upper = int(parts[1], 10)

        for id in range(lower, upper + 1):
            all_ids.append(id)

    dupes = [ ] 

    for id in all_ids:
        s = str(id)

        # index up to the halfway point 
        for i in range(1, (len(s) // 2) + 1):
            substr = s[0:i]

            # is it repeated in s?
            if (len(s) % len(substr)) != 0:
                continue 

            new_s = substr * (len(s) // len(substr))

            if new_s != s:
                continue 

            dupes.append(id)
            break

    answer = sum(dupes)

    print(f"answer = {answer}")
    # answer = 45283684555

with open('input.txt', 'r') as f:
    data = f.read()

part2(data)
