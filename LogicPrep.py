

class LogicPreps:
    def __init__(self):
        pass

    def del_ele_in_list(self, trgt_list, ele):
        return [elem for elem in trgt_list if elem != ele]

    def sort_list_by_ele(self, data_list, ele_idx, up_down_flag=True):
        result_list = []
        for tmp_arr in sorted(data_list, key=lambda tmp_arr: tmp_arr[ele_idx], reverse=up_down_flag):
            result_list.append(tmp_arr)
        return result_list

