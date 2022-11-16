from compound_to_percentage import main as compound_to_percentage
from find_limiting_reagent import main as find_limiting_reagent
from masses_to_empirical import main as masses_to_empirical
from percentage_comp_to_empirical import main as percentage_comp_to_empirical

num_mapping = {
    1: {
        "function": compound_to_percentage,
        "name": "Convert Compound to Percentage Composition"
    },
    2: {
        "function": find_limiting_reagent,
        "name": "Find Limiting Reagent in Reaction"
    },
    3: {
        "function": masses_to_empirical,
        "name": "Masses to Empirical Formula"
    },
    4: {
        "function": percentage_comp_to_empirical,
        "name": "Percentage Composition to Empirical Formula"
    }
}

while True:
    inp = int(
        input("""Options
  1. Compound to Percentage Composition
  2. Find Limiting Reagent in Reaction
  3. Masses to Empirical Formula
  4. Percentage Composition to Empirical 
Choice (1, 2, 3, 4): """)
    )

    if inp in [1, 2, 3, 4]:
        print("Running")
        num_mapping[inp]()
    else:
        print("Invalid input.")

    print()
    print()
    print("----------------------")
    print()
    print()
