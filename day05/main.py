from dataclasses import dataclass
from functools import cmp_to_key


def main():
    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")

    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    rules, index = extract_rules(lines)

    total = 0
    index += 1
    for line in lines[index:]:
        updates = list(map(lambda x: int(x), line.split(",")))
        if not is_valid(rules, updates):
            continue

        middle = len(updates) // 2
        total += updates[middle]

    return total


def second(lines: list[str]):
    rules, index = extract_rules(lines)

    total = 0
    index += 1
    for line in lines[index:]:
        updates = list(map(lambda x: int(x), line.split(",")))
        if is_valid(rules, updates):
            continue

        updates = sorted(updates, key=cmp_to_key(lambda x, y: comparator(x, y, rules)))
        middle = len(updates) // 2
        total += updates[middle]

    return total


@dataclass
class Rule:
    before: int
    after: int


def is_valid(rules: list[Rule], updates: list[int]):
    for rule in rules:
        if rule.before not in updates or rule.after not in updates:
            continue

        before_index = updates.index(rule.before)
        after_index = updates.index(rule.after)
        if before_index > after_index:
            return False

    return True


def extract_rules(lines: list[str]):
    index = 0
    rules = []
    while lines[index].strip() != "":
        rule = lines[index]
        rule = rule.split("|")
        rules.append(Rule(int(rule[0]), int(rule[1])))
        index += 1

    return rules, index


def comparator(x, y, rules: list[Rule]):
    try:
        next(rule for rule in rules if rule.before == x and rule.after == y)
    except StopIteration:
        return 0

    return -1


if __name__ == '__main__':
    main()
