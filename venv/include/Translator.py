# manul_indicator
color_list=['w','r','g']
#0是保持不变，1是买进，2是卖出
STATE=[0,1,2]
indicate_list=[]
act_sign_list=[]
position_state=1  #0代表空仓，1代表持仓

def position_state_translate(sign_list):
    global position_state
    for index in range(len(sign_list)):

        #如果是满仓，不指示继续买，只保持当前状态
         if position_state==1 and sign_list[index]==STATE[1]:
             act_sign_list.append(STATE[0])

        #如果是空仓，不指示继续卖，只保持当前状态
         elif position_state==0 and sign_list[index]==STATE[2]:
             act_sign_list.append(STATE[0])

         else:
             act_sign_list.append(sign_list[index])
             if sign_list[index]==STATE[1]:
                 position_state=1

             if sign_list[index]==STATE[2]:
                 position_state=0

    print(str(act_sign_list))
    return act_sign_list


def color_translate(sign_list):

    for index in range(len(sign_list)):

        if sign_list[index]==0:
            indicate_list.append(color_list[0])

        elif sign_list[index]==1:
            indicate_list.append(color_list[1])

        elif sign_list[index]==2:
            indicate_list.append(color_list[2])

    return indicate_list


