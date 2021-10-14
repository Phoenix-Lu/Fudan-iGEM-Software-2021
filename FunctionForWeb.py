from TreeMap import tree_data_set, set_tree,tree_data_process
from SearchEngine import take_search_result
from openpyxl import  load_workbook
import json
import global_vary



#return格式：list[dic{onename:str,path:str,related_parts:lst[],signi:lst[]},dic{}]

def get_Json_searching_data(target_part):
    global_vary._init()
    wb = load_workbook('whole_collection_processed.xlsx')
    ws= wb['Sheet1']
    global_vary.set_value('ws', ws)
    search_results = take_search_result(target_part, ws)#需要返回一个strlist
    if len(search_results) == 0:
        return 0
    back_lst = []
    for an_result in search_results:
        an_result_dic = {}
        an_result_dic['part_name'] = an_result
        tree_data = tree_data_set(an_result)
        parts_and_significance = tree_data_process(tree_data)
        set_tree(tree_data)
        tree_path = str(an_result) + "tree.html"#path要保存
        an_result_dic['tree_path'] = tree_path
        an_result_dic['related_parts'] = parts_and_significance[0]
        an_result_dic['signif'] = parts_and_significance[1]
        back_lst.append(an_result_dic)
    print(json.dumps(back_lst, indent=4))
    return json.dumps(back_lst, indent=4)

def main():
    get_Json_searching_data('BBa_I11050')

main()




#def call_for_blast(target_part):


