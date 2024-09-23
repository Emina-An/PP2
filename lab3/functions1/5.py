import itertools

def print_permutations():
    user_input = input("Enter a string: ")
    permutations = itertools.permutations(user_input)
    for perm in permutations:
        print(''.join(perm))

if __name__ == "__main__":
    print_permutations()
