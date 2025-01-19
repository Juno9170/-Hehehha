# from stt import Lango
# import eng_to_ipa as ipa

# text = "the quick brown fox jumped over the lazy dog"
# target = ipa.convert(text).replace('\'', '').replace('ˈ', '')
# s = "ək wɪk bɹawn fɑks d͡ʒʌmpt owvɹ̩ð ə lejzi dɔɡ"

# res = Lango.compare(s, target)

# for r in res:
#     print(r)

def levenshtein_operations_with_alignment(str1, str2):
    m, n = len(str1), len(str2)

    # Initialize the DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Deletion
    for j in range(n + 1):
        dp[0][j] = j  # Insertion

    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,     # Deletion
                               dp[i][j - 1] + 1,     # Insertion
                               dp[i - 1][j - 1] + 1) # Substitution

    # Backtrack to find the sequence of operations and alignments
    i, j = m, n
    operations = []
    aligned_str1 = []
    aligned_str2 = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and str1[i - 1] == str2[j - 1]:
            aligned_str1.append(str1[i - 1])
            aligned_str2.append(str2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append(f"Substitute {str1[i - 1]} with {str2[j - 1]} at position {i}")
            aligned_str1.append(str1[i - 1])
            aligned_str2.append(str2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            operations.append(f"Delete {str1[i - 1]} from position {i}")
            aligned_str1.append(str1[i - 1])
            aligned_str2.append(" ")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            operations.append(f"Insert {str2[j - 1]} at position {i + 1}")
            aligned_str1.append(" ")
            aligned_str2.append(str2[j - 1])
            j -= 1

    operations.reverse()
    aligned_str1.reverse()
    aligned_str2.reverse()

    return operations, ''.join(aligned_str1), ''.join(aligned_str2)

# Example usage
str1 = "w c"
str2 = "swick"
operations, aligned_str1, aligned_str2 = levenshtein_operations_with_alignment(str1, str2)
for op in operations:
    print(op)
print("Aligned str1:", aligned_str1)
print("Aligned str2:", aligned_str2)