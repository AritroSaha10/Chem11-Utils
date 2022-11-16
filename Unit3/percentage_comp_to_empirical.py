import json
from pprint import pprint
from math import gcd
from functools import reduce

def lcm(a, b):
    return abs(a*b) // gcd(a, b) if a and b else 0

def multiple_lcm(numbers):
    return reduce(lcm, numbers)

def main():
    periodic_table = None
    with open('periodic_table.json', encoding="utf8") as f:
        periodic_table = json.load(f)

    # Make sure it's still not none
    assert periodic_table != None

    # Extract elements array
    periodic_table = periodic_table['elements']

    # Give user instructions
    print("Provide the percentage compositions of elements in this format:")
    print("C 20%")
    print("H 10%")
    print("O 70%")
    print("Enter 'stop' when you're done.")

    # Collect user input on elements & percentages
    element_info = {}
    percentage_sum = 0

    collecting_input = True
    while collecting_input:
        user_input = input()
        if user_input == 'stop' or user_input == '':
            collecting_input = False
            break
        else:
            # Split the input into element and percentage
            split_user_input = user_input.split(" ")
            
            if len(split_user_input) == 1:
                # Assume remaining amount belongs to element, but make sure with user in case of typo
                confirmation = input("Looks like you didn't input a percentage value. Assume that remaining mass belongs to this element? (Y/n) ").lower()
                if confirmation != "n":
                    # Change percentage value to remaining percentage
                    split_user_input += [str((1 - percentage_sum) * 100)]
                    # Don't collect any other percentages after this
                    collecting_input = False
                else:
                    print("Skipping entry. Enter another entry below.")
                    continue

            element, percentage_raw = split_user_input
            percentage = float(percentage_raw.replace("%", ""))

            # Get molar mass of element
            molar_mass = None
            for element_dict in periodic_table:
                if element_dict['symbol'] == element:
                    molar_mass = element_dict['atomic_mass']
                    break

            assert molar_mass != None, "Could not find molar mass for element"

            # Calculate moles
            moles = percentage / molar_mass

            # Make sure it's not a duplicate
            assert element not in element_info, "Duplicate element"

            # Add info to dictionary
            element_info[element] = {
                'percentage': percentage / 100,
                'molar_mass': molar_mass,
                'moles': moles
            }

            # Add to percentage sum
            percentage_sum += percentage / 100
    
    assert len(element_info) > 0, "No elements provided"
    assert percentage_sum == 1, "Sum of all percentages != 0"

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
    
    # Get LCM of all factors
    subscript_factor = multiple_lcm(factors + [1, 1])

    # Multiply all of the subscripts by this number
    for element, info in element_info.items():
        old_subscript = element_info[element]['subscript']
        element_info[element]['subscript'] = old_subscript * subscript_factor

    for element, info in element_info.items():
        print(f"{element}:")
        print(f"  Percentage: {info['percentage']}%")
        print(f"  Molar mass: {info['molar_mass']} g/mol")
        print(f"  Moles: {info['moles']} mol")
        print(f"  Subscript: {info['subscript']}")
        print()

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