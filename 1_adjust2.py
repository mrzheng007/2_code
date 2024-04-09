import os
import pandas as pd

#1. read file & save result
# read setting
read_path_1 = r'F:\program\Thomas\2_vehqueue\1_data\240331\任务三'
read_name_1 = 'FNN_E2_queue.csv'
read_path_2 = r'F:\program\Thomas\2_vehqueue\1_data\240331\任务三'
read_name_2 = 'result_class4_E2_queue.csv'
read_file_1 = os.path.join(read_path_1, read_name_1)
read_file_2 = os.path.join(read_path_2, read_name_2)

# save setting
save_path = r'F:\program\Thomas\2_vehqueue\3_result\240401'
save_name = 'adjust2_queue_FNN_E2_queue.csv'
save_file = os.path.join(save_path, save_name)


#2.prcessing
df_test = pd.read_csv(read_file_1)
df_class = pd.read_csv(read_file_2)

df_test = df_test[['VehNo', 'queue', 'pre_queue']]
df_class = df_class[['VehNo', 'result', 'Headway']]
df = pd.merge(df_test, df_class, on='VehNo', how='left')

def Adjust(front_queue, pre_queue, result):
    f = front_queue
    p = pre_queue
    r = result
    #case1：0-0
    if r == 0:
        if f != 0:
            a = p
        else:
            a = 0
    # case2：1-0
    elif r == 1:
        if f != 1:
            a = p
        else:
            a = 0
    # case3：0-1
    elif r == 2:
        if f != 0:
            a = p
        else:
            a = 1
    # case4：1-1
    else:
        if f != 1:
            a = p
        else:
            a = 1
    return a


df['front_queue'] = df['pre_queue'].shift(1)
df['adjust_queue'] = df['pre_queue'].apply(lambda x: x)
df['adjust_frontqueue'] = df['front_queue'].apply(lambda x: x)
print(df)
for i in range(len(df)):
    i_max = len(df) - 1
    pre_queue = df.loc[i, 'pre_queue']
    adjust_value = Adjust(df.loc[i, 'adjust_frontqueue'], df.loc[i, 'pre_queue'],  df.loc[i, 'result'])
    df.loc[i, 'adjust_queue'] = adjust_value

    print(i)
    print(df.loc[i, 'front_queue'], df.loc[i, 'adjust_frontqueue'], df.loc[i, 'result'])
    print('adjust结果：', adjust_value)
    # print(df)
    if adjust_value != pre_queue and i < i_max:
        df.loc[i+1, 'adjust_frontqueue'] = adjust_value
        print("yes")



# 计算正确率
df['调整前预测情况'] = df.apply(lambda x: 1 if x['queue'] == x['pre_queue'] else 0, axis=1)
df['调整后预测情况'] = df.apply(lambda x: 1 if x['queue'] == x['adjust_queue'] else 0, axis=1)
rio_pre_queue = (df['调整前预测情况'].sum() / len(df)) * 100
rio_adjust_queue = (df['调整后预测情况'].sum() / len(df)) * 100
print("调整前预测正确率：", rio_pre_queue)
print("调整后预测正确率：", rio_adjust_queue)
print(df)
save_list = ['VehNo', 'queue', 'pre_queue', 'result', 'adjust_queue', 'Headway']
df[save_list].to_csv(save_file, index=False, encoding='utf_8_sig')
