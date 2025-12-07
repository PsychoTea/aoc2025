
class Range():
    def __init__(self, start, end) -> None:
        self.start = start 
        self.end = end 
        self.ignore = False 

    def is_in_range(self, num) -> bool:
        return num >= self.start and num <= self.end 

    def count(self) -> int:
        return (self.end - self.start) + 1 

    def __str__(self) -> str:
        return f"range {self.start} -> {self.end}"

def coalesce_ranges(range1, range2):
    if range2.start >= range1.start and range2.end <= range1.end:
        # range2.ignore = True 
        return True 

    did = False 

    if range2.start >= range1.start and range2.start <= range1.end:
        range1.end = range2.end 
        did = True 
    
    if range2.end >= range1.start and range2.end <= range1.start:
        range1.start = range2.start 
        did = True 

    # if did:
    #     range2.ignore = True 

    return did 

def coalesce_ranges_old(ranges: list[Range]):
    # is r2 a subset of r1?
    for r1 in ranges:
        for r2 in ranges:
            if r1 == r2:
                continue 

            if r2.start >= r1.start and r2.end <= r1.end:
                r2.ignore = True 

    # does r2 positively extend r1?
    for r1 in ranges:
        if r1.ignore:
            continue 

        for r2 in ranges:
            if r2.ignore:
                continue 

            if r1 == r2:
                continue 

            print(f"comparing {r1} and {r2}")
            if r2.start >= r1.start and r2.start <= r1.end:
                r1.end = r2.end 
                r2.ignore = True 

    # # does r2 negatively extend r1?
    for r1 in ranges:
        if r1.ignore:
            continue 

        for r2 in ranges:
            if r2.ignore:
                continue 

            if r1 == r2: 
                continue 

            if r2.end >= r1.start and r2.end <= r2.start:
                r1.start = r2.start 
                r2.ignore = True 

    return [x for x in ranges if x.ignore == False] 

with open('input.txt', 'r') as f:
    lines = f.readlines()

fresh_ids = [ ]
available_ids = [ ]

for line in lines:
    if "-" in line:
        parts = line.split('-')

        part1 = int(parts[0], 10)
        part2 = int(parts[1], 10)

        if part2 < part1:
            print(f"parse failure: {part1=} {part2=}")
            assert part2 > part1 

        fresh_ids.append(Range(part1, part2))

        # for idx in range(part1, part2 + 1):
        #     fresh_ids.append(idx)

        continue 

    id = 0

    try:
        id = int(line, 10)
    except:
        print(f"failed to parse line: {line}")
        continue 

    available_ids.append(id)

print("done parsing")

cnt = 0

# for id in available_ids:
#     for rng in fresh_ids:
#         if rng.is_in_range(id):
#             cnt += 1
#             break 

# highest_id = 0
# for rng in fresh_ids:
#     if rng.end > highest_id:
#         highest_id = rng.end 
# highest_id += 1

# for i in range(0, highest_id):
#     for rng in fresh_ids:
#         if rng.is_in_range(i):
#             cnt += 1
#             break

# for rng in fresh_ids:
#     print(f"range {rng.start} -> {rng.end} = {rng.count()}")
#     cnt += rng.count()

coalesce = fresh_ids 

# prev_len = len(coalesce)

# while True:
#     coalesce = coalesce_ranges(fresh_ids)
#     prev_len = len(coalesce)

#     if prev_len == len(coalesce):
#         break

def do_coalesce(ranges):
    for r1 in ranges:
        for r2 in ranges:
            if r1 == r2:
                continue 

            did = coalesce_ranges(r1, r2)

            if did:
                ranges.remove(r2)
                return 1

    return 0 

# test_ranges = [
#     Range(3, 5),
#     Range(100, 100)
# ]

# do_coalesce(test_ranges)
# for r in test_ranges:
#     print(r)
# exit(0)

while True:
    rval = do_coalesce(coalesce)

    print("ranges after round:")
    for r in coalesce:
        print(f"\t{r}")

    if rval == 0:
        break


# coalesce = coalesce_ranges(fresh_ids)

# print(f"count = {len(coalesce)}")

# for r in coalesce:
#     print(r)

for rng in coalesce:
    print(f"range {rng.start} -> {rng.end} = {rng.count()}")
    cnt += rng.count()

print(f"answer: {cnt}")
    
