import time
import os
import numpy as np
import shutil


import Util
import LogicPrep
############### start to set env ###############
WORK_DIR = os.getcwd() + "/"
P_NAME = WORK_DIR[:-1].split("/")[-1]
INPUT_DIR = "input/crab_eating_deep_pe_input/"
# INPUT_DIR = "input/marmoset_deep_pe_input/"
OUTPUT = "output/"
TOP_N = 1000
BATCH_SIZE = 1000
############### end setting env ################


def test():
    util = Util.Utils()
    logic_preps = LogicPrep.LogicPreps()
    total_list = []
    tmp_total_list = []
    # test file with 2673 rows, 7 hours
    # Tm_MFE_input_list = util.read_file_wo_header_by_delimiter(WORK_DIR + INPUT_DIR + "deep_pe_input_chr_NTIC01034945.1.csv")
    # 800 rows
    Tm_MFE_input_list = util.read_file_wo_header_by_delimiter(WORK_DIR + INPUT_DIR + "deep_pe_input_chr_NTIC01000447.1.csv")
    # test file with 13 rows
    # Tm_MFE_input_list = util.read_file_wo_header_by_delimiter(WORK_DIR + INPUT_DIR + "deep_pe_input_chr_NTIC01023672.1.csv")
    # Tm_MFE_input_list = util.read_file_wo_header_by_delimiter(WORK_DIR + INPUT_DIR + "deep_pe_input_chr_NTIC01035998.1.csv")
    filtered_Tm_MFE_input_list = logic_preps.del_ele_in_list(Tm_MFE_input_list, [''])

    Tm_MFE_input_chunks = [filtered_Tm_MFE_input_list[x:x + BATCH_SIZE] for x in
                           range(0, len(filtered_Tm_MFE_input_list), BATCH_SIZE)]

    for Tm_MFE_input_arr in Tm_MFE_input_chunks:
    # for tmp_arr in filtered_Tm_MFE_input_list:  # one by one
        # 1. start 1_obtainTm_MFE.py
        # # 1-1. del old input file
        try:
            os.remove('Tm_MFE_example.txt')
        except Exception as err:
            print("os.remove('Tm_MFE_example.txt') : ", err)
        # # 1-2. make new input file
        util.make_1_obtainTm_MFE_input(Tm_MFE_input_arr)
        # util.make_1_obtainTm_MFE_input([tmp_arr])  # one by one
        # # 1-3. del old result
        try:
            os.remove('out_1_obtainTm_MFE/formodeling.output.pt1.csv')
            os.remove('out_1_obtainTm_MFE/formodeling.output.pt2.csv')
            os.remove('out_1_obtainTm_MFE/formodeling.output.pt3.csv')
        except Exception as err:
            print("os.remove('out_1_obtainTm_MFE/formodeling.output.pt1.csv') : ", err)
        # # 1-4. make new result
        os.system('python ./1_obtainTm_MFE.py')
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

    try:
        os.remove('total_result_' + P_NAME + '.txt')
    except Exception as err:
        print("os.remove('total_result_" + P_NAME + ".txt') : ", err)
    util.make_top_N_total_list('total_result_' + P_NAME + '.txt', total_list)
    try:
        os.remove('tmp_total_result_' + P_NAME + '.txt')
    except Exception as err:
        print("os.remove('tmp_total_result_" + P_NAME + ".txt') : ", err)
    util.make_top_N_total_list('tmp_total_result_' + P_NAME + '.txt', tmp_total_list)




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

def make_excel_to_csv():
    util = Util.Utils()
    sources_excel = util.get_files_from_dir(WORK_DIR + INPUT_DIR + "*.xlsx")
    for excel_fn in sources_excel:
        util.make_excel_to_csv(excel_fn, "xlsx")

def divide_files_by_dir():
    split_num = 15
    util = Util.Utils()
    csv_sources = util.get_files_from_dir(WORK_DIR + INPUT_DIR + '*.csv')
    splited_csv_sources = np.array_split(csv_sources, split_num)

    cnt = 1
    for csv_arr in splited_csv_sources:
        dir_name = WORK_DIR + INPUT_DIR + "P" + str(cnt) + "/"
        os.makedirs(dir_name, exist_ok=True)
        for csv_file in csv_arr:
            # csv_file = str(tmp_csv_file)
            file_nm = csv_file.split("\\")[3]
            # print(csv_file)
            # print(file_nm)
            shutil.copy(csv_file, dir_name + file_nm)


        cnt += 1







if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [" + P_NAME + "]>>>>>>>>>>>>>>>>>>")
    test()
    # local_test()
    # read_file()
    # make_excel_to_csv()
    # divide_files_by_dir()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))