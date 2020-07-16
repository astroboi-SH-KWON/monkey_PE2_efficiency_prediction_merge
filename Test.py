import time
import os


import Util
import LogicPrep
############### start to set env ###############
WORK_DIR = os.getcwd() + "/"
INPUT_DIR = "input/crab_eating_deep_pe_input/"
# INPUT_DIR = "input/marmoset_deep_pe_input/"
OUTPUT = "output/"
############### end setting env ################

def test():
    util = Util.Utils()
    logic_preps = LogicPrep.LogicPreps()
    obj = util.read_file_wo_header_by_delimiter(WORK_DIR + INPUT_DIR + "deep_pe_input_chr_NTIC01005446.1.csv")
    new_obj = logic_preps.del_ele_in_list(obj, [''])
    util.make_1_obtainTm_MFE_input(new_obj)





if __name__ == '__main__':
    start_time = time.time()
    print("start >>>>>>>>>>>>>>>>>>")
    test()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.time() - start_time))