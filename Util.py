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
            # ignore header
            print("header : ", f.readline().replace("\n", ""))
            while True:
                tmp_line = f.readline()
                if tmp_line == '':
                    break

                tmp_arr = tmp_line.replace("\n", "").split(separator)
                result_list.append(tmp_arr)

        return result_list

    def read_file_by_delimiter(self, path, separator=','):
        result_list = []
        with open(path, "r") as f:
            while True:
                tmp_line = f.readline()
                if tmp_line == '':
                    break

                tmp_arr = tmp_line.replace("\n", "").split(separator)
                result_list.append(tmp_arr)

        return result_list

    def read_file_first_line(self, path):
        with open(path, "r") as f:
            return f.readline().replace("\n", "")

    def make_1_obtainTm_MFE_input(self, data_list):
        with open("Tm_MFE_example.txt", "a") as f:
            for tmp_arr in data_list:
                f.write("".join(re.findall("[a-zA-Z]+", tmp_arr[3])) + "\n")

    def make_DeepCas9_input(self, work_dir, src_path, result_path):
        src_list = self.read_file_by_delimiter(work_dir + src_path)
        with open(work_dir + result_path, "a") as f:
            f.writelines(
                'Wide target sequence (47)\tPrime edited sequence\tPBS length\tRT length\tPBS-RT length\t"Tm1\n(PBS)"\t"Tm 2\n(target DNA region corresponding to RT template)"\t"Tm 3\n(reverse transcribed cDNA and PAM-opposite DNA strand)"\t"Tm 4\n(RT template region and reverse transcribed cDNA)"\t"deltaTm\n(Tm3-Tm2)"\t"GC count_1\n(PBS)"\t"GC count_2\n(RT)"\t"GC count_3\n(PBS-RT)"\t"GC contents_1\n(PBS)"\t"GC contents_2\n(RT)"\t"GC contents_3\n(PBS-RT)"\t"MFE_1\n(pegRNA)"\t"MFE_2\n(-spacer)"\t"MFE_3\n(RT-PBS-PolyT)"\t"MFE_4\n(spacer only)"\t"MFE_5\n(Spacer+Scaffold)"\tDeepSpCas9 score\n')
            for tmp_arr in src_list:
                tmp_str = ""
                for tm_val in tmp_arr:
                    tmp_str += tm_val + "\t"
                # remove the last \t
                f.writelines(tmp_str[:-1] + "\n")

    def read_cas9_val(self, path):
        cas9_val = .0
        with open(path, "r") as f:
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            tmp = f.readline().replace("\n", "").strip().split(",")
            cas9_val += float(tmp[1])
        return cas9_val

    def make_DeepPE_input(self, work_dir, file_list):
        deep_cas9_input = file_list[0]
        deep_cas9_output = file_list[1]
        deep_PE_input = file_list[2]

        deep_cas9_input_list = self.read_file_by_delimiter(work_dir + deep_cas9_input, '\t')
        cas9_val = self.read_cas9_val(work_dir + deep_cas9_output)

        with open(work_dir + deep_PE_input, "a") as f:
            f.writelines('Wide target sequence (47)\tPrime edited sequence\tPBS length\tRT length\tPBS-RT length\t"Tm1\n(PBS)"\t"Tm 2\n(target DNA region corresponding to RT template)"\t"Tm 3\n(reverse transcribed cDNA and PAM-opposite DNA strand)"\t"Tm 4\n(RT template region and reverse transcribed cDNA)"\t"deltaTm\n(Tm3-Tm2)"\t"GC count_1\n(PBS)"\t"GC count_2\n(RT)"\t"GC count_3\n(PBS-RT)"\t"GC contents_1\n(PBS)"\t"GC contents_2\n(RT)"\t"GC contents_3\n(PBS-RT)"\t"MFE_1\n(pegRNA)"\t"MFE_2\n(-spacer)"\t"MFE_3\n(RT-PBS-PolyT)"\t"MFE_4\n(spacer only)"\t"MFE_5\n(Spacer+Scaffold)"\tDeepSpCas9 score\n')
            for idx in range(17, len(deep_cas9_input_list)):
                for tmp_arr in deep_cas9_input_list[idx]:
                    f.writelines(tmp_arr + "\t")
                f.writelines(str(cas9_val) + "\n")

    def make_top_N_total_list(self, path, data_list):
        with open(path, "a") as f:
            f.writelines('Wide target sequence (47)\tPrime edited sequence\tPBS length\tRT length\tPBS-RT length\tTm1(PBS)\tTm 2(target DNA region corresponding to RT template)\tTm 3(reverse transcribed cDNA and PAM-opposite DNA strand)\tTm 4(RT template region and reverse transcribed cDNA)\tdeltaTm(Tm3-Tm2)\tGC count_1(PBS)\tGC count_2(RT)\tGC count_3(PBS-RT)\tGC contents_1(PBS)\tGC contents_2(RT)\tGC contents_3(PBS-RT)\tMFE_1(pegRNA)\tMFE_2(-spacer)\tMFE_3(RT-PBS-PolyT)\tMFE_4(spacer only)\tMFE_5(Spacer+Scaffold)\tDeepSpCas9 score\tDeepPE score\n')
            for val_arr in data_list:
                tmp_str = ""
                for tm_val in val_arr:
                    tmp_str += tm_val.replace('"', '') + "\t"
                # remove the last \t
                f.writelines(tmp_str[:-1] + "\n")




