import sys
import argparse
import os
from contextlib import redirect_stdout
import numpy as np
import amplpy
from amplpy import AMPL, Environment

### ADD PATH TO FOLDER CONTAINING AMPL EXECUTABLE ###
ampl_path = "???"
#####################################################

model_path = "blevp2nlp.mod"

class ALGERROR(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def reformulate_LBP(solver='baron',
                    data_path='',
                    model_path='',
                    testing=False) -> None:
    '''
    Solver has to handle NLPs
    data_path: Path to the LBP data (AMPL-formatted .dat file). Mandatory argument if not testing.
    model_path: path to AMPL model (.mod file)
    '''

    ampl = AMPL(Environment(ampl_path))
    ampl.option["solver"] = solver

    output_handler = amplpy.OutputHandler()
    ampl.set_output_handler(output_handler)

    ampl.read(model_path)
    ampl.read_data(data_path)

    # check if bilevel
    if ampl.get_parameters()["lambda"].value() != 2:
        raise ALGERROR("Cannot reformulate: problem instance does not have 2 levels")

    # check UL constraints have no LL var (i.e. constraint parameters are 0)
    UL_cstr_LL_var_coeff = np.array([[ampl.get_parameter("A")[1,2,i,j] for j in range(1,int(ampl.get_parameter("n")[2])+1)] for i in range(1,int(ampl.get_parameter("m")[1])+1)])
    if UL_cstr_LL_var_coeff.any():
        raise ALGERROR("Cannot reformulate: problem instance is not a LBP")

    ampl.solve()
    status = ampl.get_value("solve_result")
    print("SOLVER STATUS:",status)
    if status == "solved":
        if testing:
            out_file = os.path.join("output",os.path.splitext(os.path.basename(data_path))[0]+".sol")
        else:
            out_file = "output/blevp2nlp.sol"
        with open(out_file, 'w') as f:
            with redirect_stdout(f):
                ampl.display("x")

        # get objective value
        fx = ampl.get_objective("obj").get().value()
        return fx
    else:
        return None



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_path", help="Path to the LBP data (AMPL-formatted .dat file). Mandatory argument if not testing.")
    parser.add_argument("-t", "--test", action="store_true", help="Run sample tests (may be used to check if AMPL executable works).")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    if args.test:
        print("#####\n# Running sample tests...\n")

        for path in os.listdir('tests'):
            data_path = os.path.join('tests', path)
            if os.path.isfile(data_path) and data_path.endswith(".dat"):
                print("Solving problem",os.path.splitext(os.path.basename(data_path))[0])
                fx = reformulate_LBP(
                    data_path=data_path,
                    model_path=model_path,
                    testing=True
                )
                print("##\n")
        print("# End sample tests\n#####")

    else:
        # check if is a .dat file
        if not os.path.isfile(args.data_path) or os.path.splitext(os.path.basename(args.data_path))[1] != ".dat":
            raise FileNotFoundError("Wrong file directory or type.")
        else:
            fx = reformulate_LBP(
                data_path=args.data_path,
                model_path=model_path
            )