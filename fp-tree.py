import fp_growth








#给到所有有共同引用的part组合和共同引用数，生成excel
def fp_get():
    wb = load_workbook('fp_db.xlsx')
    ws = wb['Sheet']
    fpgrowth_database = []
    for cell in ws['B']:
        if cell.row > 1:
            content = cell.value.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
            data = content.split(',')
            fpgrowth_database.append(data)
    fp_fin = []
    fp_result = list(find_frequent_itemsets(fpgrowth_database,1,include_support=True))
    for i in range(len(fp_result)):
        if len(fp_result[i][0]) == 2:
            fp_fin.append(fp_result[i])
    #print(fp_result)
    wb = workbook.Workbook()
    ws1 = wb.active
    ws1.append(['part_num1', 'part_num2', "shared citing times"])
    for i in fp_fin:
        ws1.append([i[0][0], i[0][1], i[1]])
    wb.save(f'fp_sharedciting_result.xlsx')
    #print(fp_fin)
    return

#找到和part ID有共同引用的parts并给出共同引用数
def get_relevant_parts(part_id):
    friends = []
    wb = load_workbook('fp_sharedciting_result.xlsx')
    ws = wb['Sheet']
    for cell in ws['A']:
        if cell.value == part_id:
            row = cell.row
            friend = ws['B' + str(row)].value
            relevance = ws['C' + str(row)].value
            friends.append([relevance,friend])
    for cell in ws['B']:
        if cell.value == part_id:
            row = cell.row
            friend = ws['A' + str(row)].value
            relevance = ws['C' + str(row)].value
            friends.append([relevance,friend])
            friends.append([relevance,friend])
            friends.sort(reverse=True)
    print(friends)