import time
import os


import Util
import LogicPrep
############### start to set env ###############
WORK_DIR = os.getcwd() + "/"
INPUT_DIR = "input/crab_eating_deep_pe_input/"
# INPUT_DIR = "input/marmoset_deep_pe_input/"
OUTPUT = "output/"
TOP_N = 1000
############### end setting env ################

def test():
    util = Util.Utils()
    logic_preps = LogicPrep.LogicPreps()
    total_list = []
    tmp_total_list = []
    Tm_MFE_input_list = util.read_file_wo_header_by_delimiter(WORK_DIR + INPUT_DIR + "deep_pe_input_chr_NTIC01034945.1.csv")
    filtered_Tm_MFE_input_list = logic_preps.del_ele_in_list(Tm_MFE_input_list, [''])

    for tmp_arr in filtered_Tm_MFE_input_list:
        # 1. start 1_obtainTm_MFE.py
        # # 1-1. del old input file
        try:
            os.remove('Tm_MFE_example.txt')
        except Exception as err:
            print("os.remove('Tm_MFE_example.txt') : ", err)
        # # 1-2. make new input file
        util.make_1_obtainTm_MFE_input([tmp_arr])
        # # 1-3. del old result
        try:
            os.remove('out_1_obtainTm_MFE/formodeling.output.pt1.csv')
            os.remove('out_1_obtainTm_MFE/formodeling.output.pt2.csv')
            os.remove('out_1_obtainTm_MFE/formodeling.output.pt3.csv')
        except Exception as err:
            print("os.remove('out_1_obtainTm_MFE/formodeling.output.pt1.csv') : ", err)
        # # 1-4. make new result
        os.system('./1_obtainTm_MFE.py')
        # 1. end 1_obtainTm_MFE.py

        # 2. start DeepCas9
        # # 2-1. del old input file
        try:
            os.remove('DeepCas9/DeepCas9_example_input.txt')
        except Exception as err:
            print("os.remove('DeepCas9/DeepCas9_example_input.txt') : ", err)
        # # 2-2. make new input file
        util.make_DeepCas9_input(WORK_DIR, '/out_1_obtainTm_MFE/formodeling.output.pt1.csv', '/DeepCas9/DeepCas9_example_input.txt')
        # # 2-3. del old result
        try:
            os.remove('DeepCas9/RANK_final_DeepCas9.txt')
        except Exception as err:
            print("os.remove('DeepCas9/RANK_final_DeepCas9.txt') : ", err)
        # # 2-4. make new result
        os.system('python DeepCas9/Test.py')
        # 2. end DeepCas9

        # 3. start DeepPE
        # # 3-1. del old input file
        try:
            os.remove('DeepPE/DeepPE_example_input.txt')
        except Exception as err:
            print("os.remove('DeepPE/DeepPE_example_input.txt') : ", err)

        # # 3-2. make new input file
        file_list = ['DeepCas9/DeepCas9_example_input.txt'
            , 'DeepCas9/RANK_final_DeepCas9.txt'
            , 'DeepPE/DeepPE_example_input.txt']
        util.make_DeepPE_input(WORK_DIR, file_list)
        # # 3-3. del old result
        try:
            os.remove('DeepPE/DeepPE_example_output.xlsx')
        except Exception as err:
            print("os.remove('DeepPE/DeepPE_example_output.xlsx') : ", err)
        # # 3-4. make new result
        os.system('python DeepPE/MainTest.py')
        # 3. end DeepPE

        # 4. start add data to total_list
        try:
            os.remove('DeepPE/DeepPE_example_output.csv')
        except Exception as err:
            print("os.remove('DeepPE/DeepPE_example_output.csv') : ", err)
        util.make_excel_to_csv('DeepPE/DeepPE_example_output.xlsx', 'xlsx', '0')

        result_list = util.read_file_by_delimiter('DeepPE/DeepPE_example_output.csv')
        filtered_result_list = logic_preps.del_ele_in_list(result_list, [''])
        total_list.extend(filtered_result_list)
        tmp_total_list.extend(filtered_result_list)
        sorted_total_list = logic_preps.sort_list_by_ele(total_list, -1)
        tmp_total_list = logic_preps.sort_list_by_ele(tmp_total_list, -1)
        total_list = sorted_total_list[:TOP_N]
        # 4. end add data to total_list

    util.make_top_N_total_list('total_result.txt', total_list)
    util.make_top_N_total_list('tmp_total_result.txt', tmp_total_list)




def local_test():
    util = Util.Utils()
    logic_preps = LogicPrep.LogicPreps()

    try:
        os.remove('DeepPE/DeepPE_example_output.csv')
    except Exception as err:
        print("os.remove('DeepPE/DeepPE_example_output.csv') : ", err)
    util.make_excel_to_csv('DeepPE/DeepPE_example_output.xlsx', 'xlsx', '0')

    result_list = util.read_file_by_delimiter('DeepPE/DeepPE_example_output.csv')
    filtered_result_list = logic_preps.del_ele_in_list(result_list, [''])
    for tmp_arr in filtered_result_list:
        print(tmp_arr)

    print(":::::::::::::::::::")
    sorted_result_list = logic_preps.sort_list_by_ele(filtered_result_list, -1)
    util.make_top_N_total_list('total_result.txt', sorted_result_list)

    for tmp_arr in sorted_result_list:
        print(tmp_arr)


def read_file():
    tmp_list = []
    with open("D:/000_WORK/KimHuiKwon/20200714/recieved_files/20200714/Supplemetary Code 1. DeepPE/DeepPE code/DeepPE_example_input.txt", "r") as f:

        while True:
            tmp_line = f.readline()
            if tmp_line == '':
                break
            tmp_list.append(tmp_line)
    print(tmp_list)






if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start >>>>>>>>>>>>>>>>>>")
    test()
    # local_test()
    # read_file()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))