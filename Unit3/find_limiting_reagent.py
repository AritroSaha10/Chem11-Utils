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

    reactants_data = {}
    reaction = Reaction(input("Enter a balanced chemical reaction: "))
    assert reaction.stoichiometry_conserved(), "Reaction not balanced"

    for amount, reactant in reaction.reactants:
        # Get molar mass
        molar_mass = 0
        formula = Formula(str(reactant))
        
        for element, subscript in formula.atom_stoich.items():
            element_data = next(find_element_by_symbol(element))
            
            assert element_data != None, f"Element '{element}' not found"
            element_molar_mass = element_data["atomic_mass"]
            molar_mass += element_molar_mass * subscript

        # Get mass from user
        mass = float(input(f"Mass of {reactant} (in g): "))
            
        reactants_data[reactant] = {
            'amount': amount,
            'formula': formula,
            'molar_mass': molar_mass,
            'mass': mass,
            'moles': mass / molar_mass
        }
    
    # Choose the first product and get data
    # TODO: Let user choose this
    prod_amount, _ = reaction.products[0]

    # Calculate amount of moles produced by each reactant, get lowest one
    limiting_reactant = reactants_data[next(iter(reactants_data))]
    for reactant, reactant_data in reactants_data.items():
        product_produced_mol = prod_amount / reactant_data["amount"] * reactant_data["moles"]
        if product_produced_mol < limiting_reactant["moles"]:
            limiting_reactant = reactant_data
    
    # Print limiting reactant info
    print("Limiting reactant info:")
    print(f"  Reactant: {limiting_reactant['formula']}")
    print(f"  Amount: {limiting_reactant['amount']}")
    print(f"  Molar mass: {limiting_reactant['molar_mass']}")
    print(f"  Mass: {limiting_reactant['mass']}")
    print(f"  Moles: {limiting_reactant['moles']}")
    print()

    # Calculate amount of product produced if desired
    if input("Calculate amount of product produced? (y/N): ").lower() == "y":
        for product in reaction.products:
            # Get molar mass of product
            prod_amount, prod_formula = product
            prod_formula = Formula(str(prod_formula))
            prod_molar_mass = 0

            for element, subscript in prod_formula.atom_stoich.items():
                element_data = next(find_element_by_symbol(element))
                assert element_data != None, f"Element '{element}' does not exist"
                element_molar_mass = element_data["atomic_mass"]
                prod_molar_mass += element_molar_mass * subscript
                
            # Get mass of product produced
            prod_mass = prod_molar_mass * prod_amount * limiting_reactant["moles"]
            print(f"Produced mass of {product}: {prod_mass}g")


    

if __name__ == "__main__":
    main()
