
'''
Given n candidate passwords, classify each as STRONG, WEAK_LENGTH, WEAK_PATTERN or
COMPROMISED. A strong password must contain at least one lowercase letter, uppercase letter, digit and one special symbol from
$#@. Its length must be between 6 and 12. It must not contain any dictionary word from a banned list as a contiguous substring,
ignoring case. It must also not contain the same character more than 3 times consecutively.
'''

b = int(input())

banned = []

for i in range(b):
    banned.append(input().lower())

n = int(input())

passwords = []

for i in range(n):
    passwords.append(input())

for i in range(n):

    password = passwords[i]

    # Check length
    isWeakLength = len(password) < 6 or len(password) > 12

    # Check banned words
    passwordLower = password.lower()
    isBanned = any(word in passwordLower for word in banned)

    # Check repeating characters
    repeat = 1
    isWeakPattern = False

    for j in range(1, len(password)):
        if password[j] == password[j - 1]:
            repeat += 1
            if repeat > 3:
                isWeakPattern = True
                break
        else:
            repeat = 1

    # Check password strength
    lower = False
    upper = False
    digit = False
    special = False

    for ch in password:
        if ch.islower():
            lower = True
        elif ch.isupper():
            upper = True
        elif ch.isdigit():
            digit = True
        elif ch in "$#@":
            special = True

    isStrong = lower and upper and digit and special

    # Print result
    if isBanned:
        print(f"{i+1}: COMPROMISED")
    elif isWeakLength:
        print(f"{i+1}: WEAK_LENGTH")
    elif isWeakPattern:
        print(f"{i+1}: WEAK_PATTERN")
    elif isStrong:
        print(f"{i+1}: STRONG")
    else:
        print(f"{i+1}: WEAK_PATTERN")