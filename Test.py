import time
import os


import Util
import LogicPrep
############### start to set env ###############
start_time = time.perf_counter()
WORK_DIR = os.getcwd() + "/"
INPUT_DIR = "input/crab_eating_deep_pe_input/"
# INPUT_DIR = "input/marmoset_deep_pe_input/"
OUTPUT = "output/"
TOP_N = 1000
############### end setting env ################

def test():
    util = Util.Utils()
    logic_preps = LogicPrep.LogicPreps()
    Tm_MFE_input_list = util.read_file_wo_header_by_delimiter(WORK_DIR + INPUT_DIR + "deep_pe_input_chr_NTIC01005446.1.csv")
    filtered_Tm_MFE_input_list = logic_preps.del_ele_in_list(Tm_MFE_input_list, [''])

    # os.remove('Tm_MFE_example.txt')
    # util.make_1_obtainTm_MFE_input(filtered_Tm_MFE_input_list)

    for tmp_arr in filtered_Tm_MFE_input_list:
        # # Tm_MFE_seq_input = tmp_arr[3]
        # try:
        #     os.remove('Tm_MFE_example.txt')
        # except Exception as err:
        #     print("os.remove('Tm_MFE_example.txt') : ", err)
        #
        # util.make_1_obtainTm_MFE_input([tmp_arr])
        # trgt_seq_47 = util.read_file_first_line('Tm_MFE_example.txt')
        #
        # try:
        #     os.remove('out_1_obtainTm_MFE/formodeling.output.pt1.csv')
        #     os.remove('out_1_obtainTm_MFE/formodeling.output.pt2.csv')
        #     os.remove('out_1_obtainTm_MFE/formodeling.output.pt3.csv')
        # except Exception as err:
        #     print("os.remove('out_1_obtainTm_MFE/formodeling.output.pt1.csv') : ", err)
        # os.system('./1_obtainTm_MFE.py')

        try:
            os.remove('DeepCas9/DeepCas9_example_input.txt')
        except Exception as err:
            print("os.remove('DeepCas9/DeepCas9_example_input.txt') : ", err)
        util.make_DeepCas9_input(WORK_DIR, '/out_1_obtainTm_MFE/formodeling.output.pt1.csv', '/DeepCas9/DeepCas9_example_input.txt')


        # util.read_file_wo_header_by_delimiter('out_1_obtainTm_MFE/formodeling.output.pt1.csv')




        print("for : %.2f seconds ::::::::::::::" % (time.time() - start_time))








if __name__ == '__main__':
    print("start >>>>>>>>>>>>>>>>>>")
    test()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))