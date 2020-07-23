import time
import os

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

def main():
    util = Util.Utils()
    logic_preps = LogicPrep.LogicPreps()
    total_list = []
    csv_sources = util.get_files_from_dir(WORK_DIR + INPUT_DIR + P_NAME + '/*.csv')



    for chr_file_path in csv_sources:
        Tm_MFE_input_list = util.read_file_wo_header_by_delimiter(chr_file_path)
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
            # TODO filter out duple elements
            sorted_total_list = logic_preps.sort_list_by_ele(total_list, -1)
            total_list = sorted_total_list[:TOP_N]
            # 4. end add data to total_list

    try:
        os.remove('total_result_' + P_NAME + '.txt')
    except Exception as err:
        print("os.remove('total_result_" + P_NAME + ".txt') : ", err)
    util.make_top_N_total_list('total_result_' + P_NAME + '.txt', total_list)

if __name__ == '__main__':
    start_time = time.time()
    print("start [" + P_NAME + "]>>>>>>>>>>>>>>>>>>")
    main()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.time() - start_time))