import time
import os


import Util
############### start to set env ###############
WORK_DIR = os.getcwd() + "/"
INPUT_DIR = "input/crab_eating_deep_pe_input/"
# INPUT_DIR = "input/marmoset_deep_pe_input/"
OUTPUT = "output/"
############### end setting env ################


def main():
    util = Util.Utils()

    sources_csv = util.get_files_from_dir(WORK_DIR + INPUT_DIR + "*.csv")

    obj = util.read_file_wo_header_by_delimiter(WORK_DIR + INPUT_DIR + "deep_pe_input_chr_NTIC01005446.1.csv")
    print(obj)
    print(len(obj))







def make_excel_to_csv():
    util = Util.Utils()
    sources_excel = util.get_files_from_dir(WORK_DIR + INPUT_DIR + "*.xlsx")
    for excel_fn in sources_excel:
        util.make_excel_to_csv(excel_fn, "xlsx")




if __name__ == '__main__':
    start_time = time.time()
    print("start >>>>>>>>>>>>>>>>>>")
    main()
    # make_excel_to_csv()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.time() - start_time))