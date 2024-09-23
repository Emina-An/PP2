def grams_to_ounces(g):
    v = 28.349523125
    ounces = g / v
    return ounces

grams = float(input("Enter the amount in grams: "))
print(f"{grams} grams is equal to {grams_to_ounces(grams):.2f} ounces.")
