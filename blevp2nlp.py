import sys
import argparse
import os
import numpy as np
from amplpy import AMPL, Environment

model_path = "blevp2nlp.mod"

def reformulate_LBP(solver='baron',ampl_path='',model_path='',data_path='') -> None:

    '''
    Solver has to handle NLPs
    ampl_path: path to folder containing ampl executable
    model_path: path to AMPL model
    data_path: path to AMPL-formatted .dat file
    '''
    ampl = AMPL(Environment(ampl_path))
    ampl.option["solver"] = solver

    ampl.read(model_path)
    ampl.read_data(data_path)

    ampl.solve()
    assert ampl.get_value("solve_result") == "solved"

    x = [round(ampl.get_variables()["x"][i].value(),8) for i in range(1,int(ampl.get_parameter("n").value())+1)]
    y = [round(ampl.get_variables()["y"][i].value(),8) for i in range(1,int(ampl.get_parameter("q").value())+1)]
    z = [round(ampl.get_variables()["z"][i].value(),8) for i in range(1,int(ampl.get_parameter("p").value())+1)]
    fx = round(ampl.get_objective("obj").get().value(),8)     # objective value

    return (x,y,z),fx


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
        print("Running sample tests...")

        for path in os.listdir('tests'):
            data_path = os.path.join('tests', path)
            if os.path.isfile(data_path) and data_path[-4:] == ".dat":
                print("Solving problem",data_path[6:-4])
                (x,y,z),fx = reformulate_LBP(
                    ampl_path=args.ampl_path,
                    model_path=model_path,
                    data_path=data_path
                )
                print("\tFound solution:",x,y,z,"with value:",fx,"\n")