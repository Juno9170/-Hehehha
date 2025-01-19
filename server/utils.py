class utils:

    @staticmethod
    def levenshtein_distance(a, b):
        # if |b| == 0, |a|
        if a == "":
            return len(b)
        # if |a| == 0, |b|
        if b == "":
            return len(a)
        # if head(a) == head(b)
        if a[0] == b[0]:
            return utils.levenshtein_distance(a[1:], b[1:])
        # otherwise
        res = min(
            utils.levenshtein_distance(a[1:], b),
            utils.levenshtein_distance(a, b[1:]),
            utils.levenshtein_distance(a[1:], b[1:])
        )
        return 1 + res

    @staticmethod
    def levenshtein_operations(s, target):
        m, n = len(s), len(target)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base cases
        for i in range(m + 1):
            dp[i][0] = i  # Deletion
        for j in range(n + 1):
            dp[0][j] = j  # Insertion

        # Fill the DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s[i - 1] == target[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j] + 1,     # Deletion
                                   dp[i][j - 1] + 1,     # Insertion
                                   dp[i - 1][j - 1] + 1)  # Substitution

        # Backtrack to find the sequence of operations
        i, j = m, n
        operations = []

        while i > 0 or j > 0:
            if i > 0 and j > 0 and s[i - 1] == target[j - 1]:
                i -= 1
                j -= 1
            elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
                operations.append({
                    "operation": "sub",
                    "from": s[i - 1],
                    "to": target[j - 1],
                    "position": i
                })
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
                operations.append(
                    {
                        "operation": "del",
                        "char": s[i - 1],
                        "position": i
                    })
                i -= 1
            elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
                operations.append({
                    "operation": "ins",
                    "char": target[j - 1],
                    "position": i + 1
                })
                j -= 1

        operations.reverse()
        return operations
