def largest_k_joltage(line: str, k: int = 12) -> int:
    """
    Given a string of digits `line`, pick exactly k digits in order
    to form the largest possible number.
    """
    digits = [int(c) for c in line.strip()]
    n = len(digits)
    stack = []

    for i, d in enumerate(digits):
        # While the last chosen digit is smaller than current,
        # and we can still complete k digits if we pop it, pop.
        while stack and d > stack[-1] and (len(stack) - 1 + (n - i) >= k):
            stack.pop()

        # If we still need more digits, take this one
        if len(stack) < k:
            stack.append(d)

    # Convert chosen digits to an integer
    value = 0
    for d in stack:
        value = value * 10 + d

    return value


def main():
    total = 0
    with open("input.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            v = largest_k_joltage(line, 12)
            total += v

    print(total)


if __name__ == "__main__":
    main()