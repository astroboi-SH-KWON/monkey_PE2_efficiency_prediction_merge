import time
import glob
import xlrd
import csv
import os
import re

class Utils:
    def __init__(self):
        pass

    def make_excel_to_csv(self, path, ext, sheet_nm='Sheet'):
        wb = xlrd.open_workbook(path)
        sh = wb.sheet_by_name(sheet_nm)
        csv_nm = path.replace(ext, 'csv')
        your_csv_file = open(csv_nm, 'w')
        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))

        your_csv_file.close()

    def get_files_from_dir(self, path):
        return glob.glob(path)

    def read_file_wo_header_by_delimiter(self, path, separator=','):
        result_list = []
        with open(path, "r") as f:
            print("header : ", f.readline().replace("\n", ""))
            while True:
                tmp_line = f.readline()
                if tmp_line == '':
                    break

                tmp_arr = tmp_line.replace("\n", "").split(separator)
                result_list.append(tmp_arr)

        return result_list

    def make_1_obtainTm_MFE_input(self, data_list):
        os.remove('Tm_MFE_example.txt')
        with open("Tm_MFE_example.txt", "a") as f:
            for tmp_arr in data_list:
                # f.write(tmp_arr[3].replace('"', '').replace("'", ""))
                f.write("".join(re.findall("[a-zA-Z]+", tmp_arr[3])) + "\n")

