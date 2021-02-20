'''
# Name: flc_component.py
# Task: Defining the class where the FLC action takes place
# Date: (Revised) 20.Feb 2021
# Src:  https://pythonhosted.org/scikit-fuzzy/userguide/fuzzy_control_primer.html
'''
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

class FuzzyController():
    # inputs and output definition
    cam_dist = 0    # input 1/Antecedent
    beam_width = 0  # input 2/Antecedent
    out = 0         # output/Consequent

    # rule-set variables
    rule1 = 0
    rule2 = 0
    rule3 = 0
    rule4 = 0
    rule5 = 0
    rule6 = 0
    rule7 = 0
    rule8 = 0
    rule9 = 0

    # control system
    dyn_focus_ctrl = 0
    dyn_focus_ctrl_sim = 0

    def __init__(self):
        self.cam_dist = 0
        self.beam_width = 0
        self.out = 0
        self.rule1 = 0
        self.rule2 = 0
        self.rule3 = 0
        self.rule4 = 0
        self.rule5 = 0
        self.rule6 = 0
        self.rule7 = 0
        self.rule8 = 0
        self.rule9 = 0
        self.dyn_focus_ctrl = 0
        self.dyn_focus_ctrl_sim = 0
        print("INFO: FuzzyController() object created")

    def setup(self):    # setup the main FLC parameters
        self.cam_dist = ctrl.Antecedent(np.arange(0, 51, 1), "cam_dist")    # 0 cms to 50 cms with step-size 1
        self.beam_width = ctrl.Antecedent(np.array([79000, 73000, 58000, 50000, 43000, 34000, 25000]), "beam_width")
                                        # temporary beam width area values; 50k is the middle-point calculated on paper
        self.out = ctrl.Consequent(np.array([2, 4, 6]), "out")  # volt values 0-2V

        # create the membership functions
        self.cam_dist["Near"] = fuzz.trimf(self.cam_dist.universe, [0, 0, 25])
        self.cam_dist["Far"] = fuzz.trimf(self.cam_dist.universe, [0, 25, 50])
        self.cam_dist["Very Far"] = fuzz.trimf(self.cam_dist.universe, [25, 50, 50])

        self.beam_width["Large"] = fuzz.trimf(self.beam_width.universe, [25000, 25000, 50000])
        self.beam_width["X-Large"] = fuzz.trimf(self.beam_width.universe, [25000, 50000, 79000])
        self.beam_width["XX-Large"] = fuzz.trimf(self.beam_width.universe, [50000, 79000, 79000])

        self.out["Low"] = fuzz.trimf(self.out.universe, [2, 2, 4])
        self.out["Mid"] = fuzz.trimf(self.out.universe, [2, 4, 6])
        self.out["High"] = fuzz.trimf(self.out.universe, [4, 6, 6])

        # save the plots
        self.cam_dist.view()
        plt.savefig("cam_dist_mf.png")
        self.beam_width.view()
        plt.savefig("beam_width_mf.png")
        self.out.view()
        plt.savefig("out_mf.png")

        # define the rules
        self.rule1 = ctrl.Rule(self.cam_dist["Near"] | self.beam_width["Large"], self.out["Low"])
        self.rule2 = ctrl.Rule(self.cam_dist["Near"] | self.beam_width["X-Large"], self.out["Mid"])
        self.rule3 = ctrl.Rule(self.cam_dist["Near"] | self.beam_width["XX-Large"], self.out["Mid"])

        self.rule4 = ctrl.Rule(self.cam_dist["Far"] | self.beam_width["Large"], self.out["Low"])
        self.rule5 = ctrl.Rule(self.cam_dist["Far"] | self.beam_width["X-Large"], self.out["Mid"])
        self.rule6 = ctrl.Rule(self.cam_dist["Far"] | self.beam_width["XX-Large"], self.out["Mid"])

        self.rule7 = ctrl.Rule(self.cam_dist["Very Far"] | self.beam_width["Large"], self.out["Low"])
        self.rule8 = ctrl.Rule(self.cam_dist["Very Far"] | self.beam_width["X-Large"], self.out["Mid"])
        self.rule9 = ctrl.Rule(self.cam_dist["Very Far"] | self.beam_width["XX-Large"], self.out["High"])

        # TODO: Add rule-set view plots later and save them

        # define the control system with the defined rule-set
        self.dyn_focus_ctrl = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3, self.rule4])

        # simulate the control system so that we can apply inputs to the control system
        self.dyn_focus_ctrl_sim = ctrl.ControlSystemSimulation(self.dyn_focus_ctrl)

        print("INFO: FLC setup complete")

    def run_flc(self, input1_cd, input2_bw):
        print("INFO: FLC running now...")
        # feed the inputs to the control system simulation object
        self.dyn_focus_ctrl_sim.input["cam_dist"] = input1_cd
        self.dyn_focus_ctrl_sim.input["beam_width"] = input2_bw

        # run the flc control system simulation
        self.dyn_focus_ctrl_sim.compute()
        print("OUTPUT: FLC Output is: ", self.dyn_focus_ctrl_sim.output["out"])

        # view the simulation results on graph
        self.out.view(sim=self.dyn_focus_ctrl_sim)
        plt.savefig("flc_output.png")

    def stop_flc(self):
        print("ALERT: FLC stopped running...")


'''
f = FuzzyController()
f.setup()
f.run_flc(48, 36000)
f.stop_flc()
'''


