import pyomo.environ as pe
import numpy as np
from LBP_reformulation import *

ampl_path = "../ampl_macos64"
model_path = "LBP_reformulation.mod"

def pb_4():
    data_path = "LBP_reformulation_pb_4.dat"
    x,y,z = reformulate_LBP(
        ampl_path=ampl_path,
        model_path=model_path,
        data_path=data_path
    )
    print(x,y,z)

def pb_7():
    data_path = "LBP_reformulation_pb_7.dat"
    x,y,z = reformulate_LBP(
        ampl_path=ampl_path,
        model_path=model_path,
        data_path=data_path
    )
    print(x,y,z)

def pb_7_1():
    data_path = "LBP_reformulation_pb_7_1.dat"
    x,y,z = reformulate_LBP(
        ampl_path=ampl_path,
        model_path=model_path,
        data_path=data_path
    )
    print(x,y,z)

def pb_7_2():
    data_path = "LBP_reformulation_pb_7_2.dat"
    x,y,z = reformulate_LBP(
        ampl_path=ampl_path,
        model_path=model_path,
        data_path=data_path
    )
    print(x,y,z)

def pb_8():
    data_path = "LBP_reformulation_pb_8.dat"
    x,y,z = reformulate_LBP(
        ampl_path=ampl_path,
        model_path=model_path,
        data_path=data_path
    )
    print(x,y,z)

pb_4()
pb_7()
pb_7_1()
pb_7_2()
pb_8()
