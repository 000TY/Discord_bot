import random
import datetime

def isint(s):  # 整数値を表しているかどうかを判定
    try:
        int(s, 10)  # 文字列を実際にint関数で変換してみる
    except ValueError:
        return False  # 例外が発生＝変換できないのでFalseを返す
    else:
        return True  # 変換できたのでTrueを返す

def conv_to_str(list0):
    list1 = ""
    total = 0

    for i in list0:
        list1 = list1 + " " + str(i)
        total += i
    
    return([list1.lstrip(), total])

# サイコロ
def dice(wait_message):
    list0 = []
    if "d" in wait_message:
        wait_list = wait_message.split("d")
    elif "D" in wait_message:
        wait_list = wait_message.split("D")
    elif "ｄ" in wait_message:
        wait_list = wait_message.split("ｄ")
    elif "Ｄ" in wait_message:
        wait_list = wait_message.split("Ｄ")
    else:
        return("入力形式が違います。")        
    if True is isint(wait_list[0]) is isint(wait_list[1]):
        i = int(wait_list[0])
        temp = i
        surface = int(wait_list[1])
        temp = str(temp) + "d" + str(surface)
        if i == 0:
            pass
        else:
            while i != 0:
                output = random.randint(1,surface)
                list0.append(output)
                i -= 1
            list1 = ""
            #total = 0
            re = conv_to_str(list0)
            list1 = re[0]
            total = re[1]
            
            #list1 + list1.replace(" ", " ")
            if int(wait_list[0]) == 1:
                if int(wait_list[0]) == 1 and surface == 100 and total >= 96:
                    return(str(list1) + "\n" + "ファンブル")
                elif int(wait_list[0]) == 1 and surface == 100 and total <= 5:
                    return(str(list1) + "\n" + "クリティカル")
                else:    
                    return(str(list1))
            else:
                if int(wait_list[0]) == 1 and surface == 100 and total >= 96:
                    return(str(list1) + "\n" + "合計 " + str(total) + "\n" + "ファンブル")
                elif int(wait_list[0]) == 1 and surface == 100 and total <= 5:
                    return(str(list1) + "\n" + "合計 " + str(total) + "\n" + "クリティカル")
                else:    
                    return(str(list1) + "\n" + "合計 " + str(total))
    else:
        return("入力形式が違います。")

# CCB
def CCB(wait_message):
    if wait_message.find("ccb") == 0:
        wait_message = wait_message.lstrip("ccb")
    elif wait_message.find("CCB") == 0:
        wait_message = wait_message.lstrip("CCB")
    elif wait_message.find("ｃｃｂ") == 0:
        wait_message = wait_message.lstrip("ｃｃｂ")
    elif wait_message.find("ＣＣＢ") == 0:
        wait_message = wait_message.lstrip("ＣＣＢ")
    else:
        return("入力形式が違います。")

    if wait_message.find("<=") == 0:
        judge = 0
        wait_message = wait_message.lstrip("<=")
    elif wait_message.find("＜＝") == 0:
        judge = 0
        wait_message = wait_message.lstrip("＜＝")
    elif wait_message.find("==") == 0:
        judge = 1
        wait_message = wait_message.lstrip("==")
    elif wait_message.find("＝＝") == 0:
        judge = 1
        wait_message = wait_message.lstrip("＝＝")
    elif wait_message.find(">=") == 0:
        judge = 2
        wait_message = wait_message.lstrip(">=")
    elif wait_message.find("＞＝") == 0:
        judge = 2
        wait_message = wait_message.lstrip("＞＝")
    elif wait_message.find("!=") == 0:
        judge = 3
        wait_message = wait_message.lstrip("!=")
    elif wait_message.find("！＝") == 0:
        judge = 3
        wait_message = wait_message.lstrip("！＝")
    else:
        return("入力形式が違います。")

    if isint(wait_message):
        num = int(wait_message)
        if num == 0:
            return("入力形式が違います。")
        else:
            output = random.randint(1,100)

            if judge == 0:
                result = output <= num
            elif judge == 1:
                result = output == num
            elif judge == 2:
                result = output >= num
            elif judge == 3:
                result = output != num

            if result == True:
                if output <= 5:
                    return(f"{output}\nクリティカル")
                elif output <= 95:
                    return(f"{output}\n成功")
                elif output >= 96:
                    return(f"{output}\nファンブル")
            elif result == False:
                if output <= 95:
                    return(f"{output}\n失敗")
                elif output >= 96:
                    return(f"{output}\nファンブル")
    else:
        return("入力形式が違います。")

# クリティカル or ファンブル
def c_or_f(critical=True, fumble=True):
    limit = True
    count = 0
    list0 = []
    list1 = ""
    while limit != False:
        num = random.randint(1,100)
        list0.append(num)

        if num <= 5 and critical == True or num >= 96 and fumble==True:
            limit = False
        count += 1

        #print(num)
    list1 = conv_to_str(list0)[0]

    return(F"{list1}\n{count}回目です")


# おみくじ
def omikuzi():
    omikuzi = [["大吉", 1, 7],["吉", 2, 6],["中吉", 3, 5],["小吉", 3, 4],["末吉", 2, 3],["凶", 1, 2],["大凶", 1, 1],]   #おみくじの結果リストの作成

    count = 0
    total = 0

    ratio = []
    while count != len(omikuzi):
        total += omikuzi[count][1]
        ratio.append(total - 1)
        count += 1

    num = random.randint(0,total - 1)  #ランダムな数字の生成

    num_1 = 0
    num_2 = 0

    while num_2 == 0:
        if num <= ratio[num_1]:
            num_3 = num_1
            num_2 = 1
        num_1 += 1

    return([omikuzi[num_3][0], omikuzi[num_3][2]])

# 時間
def nowtime():
    dt_now = datetime.datetime.now()
    return(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
