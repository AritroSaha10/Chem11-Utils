from pyvalem.formula import Formula
from pyvalem.reaction import Reaction
import json
from pprint import pprint

def main():
    periodic_table = None
    with open('periodic_table.json', encoding="utf8") as f:
        periodic_table = json.load(f)

    # Make sure it's still not none
    assert periodic_table != None

    # Extract elements array
    periodic_table = periodic_table['elements']

    # Util func on periodic table data
    find_element_by_symbol = lambda symbol: filter(lambda element: element["symbol"] == symbol, periodic_table)

    # Get compound
    formula = Formula(input("Enter a formula for an compound: "))
    print(formula.atom_stoich)

    # Sum all atomic weights
    elements_data = {}
    mass_sum = 0
    for element, subscript in formula.atom_stoich.items():
        elem_data = next(iter(find_element_by_symbol(str(element))))
        molar_mass = elem_data["atomic_mass"]

        elements_data[str(element)] = {
            "molar_mass": molar_mass,
            "subscript": subscript,
        }

        mass_sum += molar_mass * subscript

    # Print element percentage compositions
    for elem, element_data in elements_data.items():
        print(f"{elem}:")
        print(f"  Molar mass: {element_data['molar_mass']} g/mol")
        print(f"  Subscript: {element_data['subscript']}")
        print(f"  Mass percentage: {round(element_data['molar_mass'] * element_data['subscript'] / mass_sum * 100, 2)}%")
    

if __name__ == "__main__":
    main()