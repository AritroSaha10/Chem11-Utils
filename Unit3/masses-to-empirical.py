import json
from pprint import pprint
from math import gcd

def main():
    periodic_table = None
    with open('periodic_table.json', encoding="utf8") as f:
        periodic_table = json.load(f)

    # Make sure it's still not none
    assert periodic_table != None

    # Extract elements array
    periodic_table = periodic_table['elements']

    # Give user instructions
    print("Provide the masses of elements in this format:")
    print("C 20g")
    print("H 10g")
    print("O 70g")
    print("Enter 'stop' when you're done.")

    # Collect user input on elements & percentages
    element_info = {}
    mass_sum = 0

    collecting_input = True
    while collecting_input:
        user_input = input()
        if user_input == 'stop' or user_input == '':
            collecting_input = False
            break
        else:
            # Split the input into element and mass
            split_user_input = user_input.split(" ")

            element, mass_raw = split_user_input
            mass = float(mass_raw.replace("g", ""))

            # Get molar mass of element
            molar_mass = None
            for element_dict in periodic_table:
                if element_dict['symbol'] == element:
                    molar_mass = element_dict['atomic_mass']
                    break

            assert molar_mass != None, "Could not find molar mass for element"

            # Calculate moles
            moles = mass / molar_mass

            # Make sure it's not a duplicate
            assert element not in element_info, "Duplicate element"

            # Add info to dictionary
            element_info[element] = {
                'mass': mass,
                'molar_mass': molar_mass,
                'moles': moles
            }

            # Add to percentage sum
            mass_sum += mass
    
    assert len(element_info) > 0, "No elements provided"

    # Get smallest mole amount
    smallest_mole_amount = None
    for element, info in element_info.items():
        if smallest_mole_amount == None or info['moles'] < smallest_mole_amount:
            smallest_mole_amount = info['moles']
    
    assert smallest_mole_amount != None, "Could not find smallest mole amount"
    
    # Calculate subscripts for each element
    factors = []
    for element, info in element_info.items():
        subscript_raw = round(info['moles'] / smallest_mole_amount, 2)
        element_info[element]['subscript'] = subscript_raw

        if subscript_raw != int(subscript_raw):
            # Is a decimal, we need to make it a whole number
            # Add factor to the list
            decimal_as_ratio = float.as_integer_ratio(subscript_raw - int(subscript_raw))
            whole_factor = decimal_as_ratio[1] # denom can be mult to make decimal whole
            factors.append(whole_factor)
    
    # Get greatest common denominator of all factors
    subscript_factor_gcd = factors[0] if len(factors) > 0 else 1
    if len(factors) > 1:
        subscript_factor_gcd = gcd(*factors)

    # Multiply all of the subscripts by this number
    for element, info in element_info.items():
        old_subscript = element_info[element]['subscript']
        element_info[element]['subscript'] = old_subscript * subscript_factor_gcd

    pprint(element_info)

    # Create empirical formula
    empirical_formula = ""
    for element, info in element_info.items():
        # Convert subscript from float to whole number
        subscript_num = int(info['subscript'])

        # Don't write the subscript if it's 1
        subscript = str(subscript_num) if subscript_num != 1 else ""
        empirical_formula += f"{element}{subscript}"

    print(f"\nFinal empirical formula: {empirical_formula}")

if __name__ == '__main__':
    main()