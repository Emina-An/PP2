def solve(numheads, numlegs):
    for chickens in range(numheads + 1):
        rabbits = numheads - chickens
        if 2 * chickens + 4 * rabbits == numlegs:
            return chickens, rabbits
    return None

if __name__ == "__main__":
    heads = 35
    legs = 94
    result = solve(heads, legs)
    if result:
        chickens, rabbits = result
        print(f"Chickens: {chickens}, Rabbits: {rabbits}")
    else:
        print("No solution found.")
