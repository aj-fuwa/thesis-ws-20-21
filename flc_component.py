'''
# Name: flc_component.py
# Task: Defining the class where the FLC action takes place
# Date: (Revised) 29.Mar 2021
# Src:  https://pythonhosted.org/scikit-fuzzy/userguide/fuzzy_control_primer.html
#       https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem.html
#       https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_control_system_advanced.html
#       https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html
#       https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_defuzzify.html#example-plot-defuzzify-py
'''
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

class FuzzyController():

    def __init__(self):
        self.crisp_output = 0
        print("INFO: FuzzyController() object created")

    def setup(self):    # setup the main FLC parameters
        # get the data ranges for all parameters
        self.v_bw = np.array([79000, 73000, 58000, 50000, 43000, 34000, 25000])
        self.v_cd = np.arange(0, 51, 1)
        self.v_out = np.array([0, 1, 2])

        # create the membership functions
        self.bw_l = fuzz.trimf(self.v_bw, [25000, 25000, 50000])
        self.bw_xl = fuzz.trimf(self.v_bw, [25000, 50000, 79000])
        self.bw_xxl = fuzz.trimf(self.v_bw, [50000, 79000, 79000])

        self.cd_n = fuzz.trimf(self.v_cd, [0, 0, 25])
        self.cd_f = fuzz.trimf(self.v_cd, [0, 25, 50])
        self.cd_vf = fuzz.trimf(self.v_cd, [25, 50, 50])

        self.out_low = fuzz.trimf(self.v_out, [0, 0, 1])
        self.out_med = fuzz.trimf(self.v_out, [0, 1, 2])
        self.out_high = fuzz.trimf(self.v_out, [1, 2, 2])

        # plot the membership functions and save the plots
        self.fig, (self.p0, self.p1, self.p2) = plt.subplots(nrows=3, figsize=(10, 10))
        self.p0.set_title("Beam Width")
        self.p0.plot(self.v_bw, self.bw_l, 'r', label="Large")
        self.p0.plot(self.v_bw, self.bw_xl, 'g', label="Extra Large")
        self.p0.plot(self.v_bw, self.bw_xxl, 'b', label="Extra Extra Large")
        self.p0.legend()
        plt.savefig("beam_width_mf.png")

        self.p1.set_title("Cam Dist")
        self.p1.plot(self.v_cd, self.cd_n, 'r', label="Near")
        self.p1.plot(self.v_cd, self.cd_f, 'g', label="Far")
        self.p1.plot(self.v_cd, self.cd_vf, 'b', label="Very Far")
        self.p1.legend()
        plt.savefig("cam_dist_mf.png")

        self.p2.set_title("Out Voltage")
        self.p2.plot(self.v_out, self.out_low, 'r', label="Low")
        self.p2.plot(self.v_out, self.out_med, 'g', label="Medium")
        self.p2.plot(self.v_out, self.out_high, 'b', label="High")
        self.p2.legend()
        plt.savefig("out_mf.png")

        print("INFO: FLC setup complete")

    def run_flc(self, input1_cd, input2_bw):
        # find the degree of membership for the given input values for both the input params
        self.bw_l_act = fuzz.interp_membership(self.v_bw, self.bw_l, input2_bw)
        self.bw_xl_act = fuzz.interp_membership(self.v_bw, self.bw_xl, input2_bw)
        self.bw_xxl_act = fuzz.interp_membership(self.v_bw, self.bw_xxl, input2_bw)

        self.cd_n_act = fuzz.interp_membership(self.v_cd, self.cd_n, input1_cd)
        self.cd_f_act = fuzz.interp_membership(self.v_cd, self.cd_f, input1_cd)
        self.cd_vf_act = fuzz.interp_membership(self.v_cd, self.cd_vf, input1_cd)

        # get the rule activation for each rule
        self.rule1_activation = np.fmin(self.bw_l_act, self.out_low)

        self.rule2_activation = np.fmin(self.bw_xl_act, self.out_med)

        self.rule3_activation = np.fmin(np.fmin(self.bw_xxl_act, self.cd_n_act), self.out_high)

        self.rule4_activation = np.fmin(np.fmin(self.bw_xxl_act, self.cd_f_act), self.out_med)

        self.rule5_activation = np.fmin(np.fmin(self.bw_xxl_act, self.cd_vf_act), self.out_med)

        # get the aggregrate. This is where all the output membership functions must be combined
        self.agg_out_mf = np.fmax(self.rule1_activation,
           np.fmax(self.rule2_activation,
           np.fmax(self.rule3_activation,
           np.fmax(self.rule4_activation, 
			self.rule5_activation))))

        print("INFO: FLC running now...")
        
        # use "Centroid" defuzzifcation and get the crisp/defuzzified output
        self.crisp_output = fuzz.defuzz(self.v_out, self.agg_out_mf, 
					"centroid")


    def stop_flc(self):
        print("ALERT: FLC stopped running...")
