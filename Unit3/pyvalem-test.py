from pyvalem.formula import Formula
from pyvalem.reaction import Reaction

def main():
    formula = Formula("(C6)H12O6")
    reaction = Reaction("2Al + Fe2O3 -> Al2O3 + 2Fe")
    print(formula.atom_stoich)
    print(reaction.reactants)
    print(reaction.products)

if __name__ == "__main__":
    main()
