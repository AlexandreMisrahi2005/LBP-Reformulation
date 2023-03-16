import numpy as np
from amplpy import AMPL, Environment

class NoSolutionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print("There is no solution")

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

    x = np.array([ampl.get_variables()["x"][i].value() for i in range(1,int(ampl.get_parameter("Nmax").value())+1)])
    y = np.array([ampl.get_variables()["y"][i].value() for i in range(1,int(ampl.get_parameter("Qmax").value())+1)])
    z = np.array([ampl.get_variables()["z"][i].value() for i in range(1,int(ampl.get_parameter("Pmax").value())+1)])
    # fx = ampl.get_objective("obj").get().value()     # objective value

    return x,y,z