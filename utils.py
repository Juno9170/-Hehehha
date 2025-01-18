def levenshtein_distance(a, b):
    # if |b| == 0, |a|
    if a == "":
        return len(b)
    # if |a| == 0, |b|
    if b == "":
        return len(a)
    # if head(a) == head(b)
    if a[0] == b[0]:
        return levenshtein_distance(a[1:], b[1:])
    # otherwise
    res = min(
        levenshtein_distance(a[1:], b),
        levenshtein_distance(a, b[1:]),
        levenshtein_distance(a[1:], b[1:])
    )
    return 1 + res


print(levenshtein_distance("kitten", "sitting"))
