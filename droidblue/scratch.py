import random

def roll_atk(n, has_focus):
    blanks, eyeballs, hits = 0, 0, 0

    for _ in range(n):
        d = random.randint(1, 8)

        if d <= 2:
            blanks += 1
        elif d <= 4:
            eyeballs += 1
        else:
            hits += 1

    if has_focus and eyeballs and hits + eyeballs >= 3:
        hits += eyeballs
        has_focus = False

    return has_focus, hits

def roll_def(n, has_focus, hits, has_heroic):
    blanks, eyeballs, evades = 0, 0, 0

    for _ in range(n):
        d = random.randint(1, 8)

        if d <= 3:
            blanks += 1
        elif d <= 5:
            eyeballs += 1
        else:
            evades += 1

    if has_heroic and n == blanks:
        return roll_def(n, has_focus, hits, has_heroic)

    if has_focus and evades < hits:
        evades += eyeballs
        has_focus = False

    return has_focus, evades

def round(has_heroic):
    has_focus = True
    has_focus, _ = roll_atk(4, has_focus)

    # spent_on_attack = not has_focus
    damage = 0

    for _ in range(2):
        _, hits = roll_atk(3, True)

        has_focus, evades = roll_def(2, has_focus, hits, has_heroic)

        if hits > evades:
            damage += hits - evades

    return damage

def game(has_heroic):
    damage = 0
    rounds = 0
    shots = 0

    while damage < 7:
        rounds += 1

        damage += round(has_heroic)

    return rounds

def stats():
    normal_counts = [0 for i in range(11)]
    heroic_counts = [0 for i in range(11)]
    n = 1000

    for _ in range(n * 100):
        rounds = game(False)
        rounds = min(rounds, 10)
        normal_counts[rounds] += 1

        rounds = game(True)
        rounds = min(rounds, 10)
        heroic_counts[rounds] += 1

    print("round  normal   heroic")
    print("#      deaths   deaths")
    for i in range(1, 11):
        print("{:2}: {:6.1f}%   {:6.1f}%".format(i, normal_counts[i] / n, heroic_counts[i] / n ))


stats()
