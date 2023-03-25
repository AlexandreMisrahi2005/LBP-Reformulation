import sys
import argparse
import os
from contextlib import redirect_stdout
import numpy as np
from amplpy import AMPL, Environment

model_path = "blevp2nlp.mod"

class ALGERROR(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def reformulate_LBP(solver='baron',
                    ampl_path='', 
                    data_path='',
                    model_path='') -> None:
    '''
    Solver has to handle NLPs
    ampl_path: Path to folder containing AMPL executable.
    data_path: Path to the LBP data (AMPL-formatted .dat file). Mandatory argument if not testing.
    model_path: path to AMPL model (.mod file)
    '''

    ampl = AMPL(Environment(ampl_path))
    ampl.option["solver"] = solver

    ampl.read(model_path)
    ampl.read_data(data_path)

    # !!! verify UL constraints have no LL var (assert the problem is an LBP)

    if ampl.get_parameters()["lambda"].value() != 2:
        raise ALGERROR("Cannot reformulate: problem instance does not have 2 levels")

    ampl.solve()
    status = ampl.get_value("solve_result")
    print("SOLVER STATUS:",status)
    if status == "solved":
        # !!! better handle directories
        with open(os.path.join("output",data_path[6:-4]+".sol"), 'w') as f:
            with redirect_stdout(f):
                ampl.display("x")

        fx = ampl.get_objective("obj").get().value()     # objective value

        return fx
    else:
        return None



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("ampl_path", help="Path to folder containing AMPL executable.")
    parser.add_argument("--data_path", help="Path to the LBP data (AMPL-formatted .dat file). Mandatory argument if not testing.")
    parser.add_argument("-t", "--test", action="store_true", help="Run sample tests (may be used to check if AMPL executable works).")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    if args.test:
        print("#####\n# Running sample tests...\n")

        for path in os.listdir('tests'):
            data_path = os.path.join('tests', path)
            # if os.path.isfile(data_path) and data_path[-4:] == ".dat":
            if os.path.isfile(data_path) and data_path.endswith(".dat"):
                print("Solving problem",data_path[6:-4])
                fx = reformulate_LBP(
                    ampl_path=args.ampl_path,
                    model_path=model_path,
                    data_path=data_path
                )
                print("##\n")
        print("# End sample tests\n#####")

    else:
        if not os.path.isfile(data_path) or data_path[-4:] != ".dat":
            raise("Wrong file directory or type.")
        else:
            fx = reformulate_LBP(
                ampl_path=args.ampl_path,
                model_path=model_path,
                data_path=args.data_path
            )