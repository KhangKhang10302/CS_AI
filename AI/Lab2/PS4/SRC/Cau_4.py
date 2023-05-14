# Khởi tạo biến toàn cục
used = [] # lưu mệnh đề từng xuất hiện lại tránh bị lập qua mỗi vòng lặp

def split_String(s):# Xử lý nhiễu trong input
    s_new = s
    s_new = s_new.replace(" ", "")
    s_new = s_new.replace("\n", "")
    return s_new

def readFile(file_name): # Đọc File 
    s = []
    f = open(file_name, 'r')
    alpha = f.readline()
    alpha = split_String(alpha)
    n = f.readline()
    n = split_String(n)
    for i in f:
        ss = i
        ss = split_String(ss)
        s.append(ss)
    return alpha, n, s # trả về alpha, n và list s các mệnh đề

# Hàm sắp xếp theo kí tự a-z bubble sort, vì chuỗi có phần tử có dấu - ở đầu nên cần viết chương trình xử lý riêng 
def sort_ascii(list): 
    ls = list.copy()
    n = len(ls)
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            if (len(ls[i]) > 1 ): x = ls[i][1] # TH chuỗi có dấu - (vd : -A) ta so sánh theo chuỗi không có dấu - 
            else: x = ls[i]
            if (len(ls[j]) > 1 ): y = ls[j][1] # 
            else: y = ls[j]

            if(x > y):
                tmp_p = ls[i]
                ls[i] = ls[j]
                ls[j] = tmp_p
    return ls    

#Hàm bổ trợ tạo mệnh đề 
def add_On(ans, sub, pos1, pos2): 
    for i in sub: # xét từng phần tử mệnh đề sub
        tmp = 0 # biến đánh dấu 
        if i != pos1[0][0] and i != pos1[0][1]:
            for j in pos2:
                if (j == i):
                    tmp = 1
                    break
            if (tmp == 0):
                ans.append(i)
    return ans 

# Check và tạo mệnh đề
def union(sub1, sub2): 
    ans = [] # Lưu ans là kq hợp giải 
    pos2 = [] # Lưu các phần tử trùng ở cả hai mệnh đề
    pos1 = [] # Lưu những cặp đối ngẫu

    sub1 = sub1.split('OR') # tách ra literal riêng để dễ xử lý như: so sánh, sắp xếp 
    sub2 = sub2.split('OR') #
    for i in sub1:
        for j in sub2:
            if len(i) - len(j) != 0: # 2 biến chiều dài khác nhau có khả năng đối ngẫu 
                if (len(i) > 1):
                    if i[1] == j[0] : # kiểm tra đối ngẫu 
                        pos1.append((i, j))
                else:
                    if i[0] == j[1]: #
                        pos1.append((i, j))
            if i == j: # Phần tử trùng ở cả 2 mệnh đề
                pos2.append(i)

    if (len(pos1) == 1): # TH chỉ có 1 biến đối ngẫu -> tiến hành các bước hợp giải 
        ans = add_On(ans, sub1, pos1, pos2)
        ans = add_On(ans, sub2, pos1, pos2)
        for i in pos2:
            ans.append(i) 
        return True, ans # trả về True là hợp giải thành công 
    else:
        return False, ans # ngược lại, ans = []

#Phủ định alpha
def Not_alpha(alpha): 
    alpha = alpha.split('OR') # Nếu alpha là mệnh đề thì tách ra các literal 
    not_alpha = []
    for i in alpha : 
        if len(i) == 2:
            not_alpha.append(i[1])
        else:
            ss = '-' + i
            not_alpha.append(ss)
    return not_alpha

# Khởi tạo các giá trị ban đầu theo giả thuyết và kết luận
def initialization(not_alpha, arr_cur, s ): 
    for i in not_alpha: # Thêm dữ liệu từ phủ định alpha
        arr_cur.append(i)
        if i not in used:
            used.append(i)

    for i in s: # Thêm dữ liệu từ giả thuyết
        arr_cur.append(i)
        ss = ''
        s1 = i
        s1 = s1.split('OR')
        for j in s1:
            ss += j
        if ss not in used:
            used.append(ss)

def PL_Resolution(alpha, n, s, file_out): # Robinson
    arr_cur = [] #arr_cur mảng các mệnh đề hiện tại đã được tạo
    add = [] # mảng lưu các mệnh đề mới được tạo thành từ mỗi vòng lặp 
    not_alpha = Not_alpha(alpha)
    initialization(not_alpha, arr_cur, s)
    file = open(file_out, mode = 'w', encoding='utf-8-sig')
    loop = 1
    stopp = 0 # đánh dấu xuất hiện mệnh đề rỗng
    while loop == 1 :
        ans = []
        # 
        for i in range(len(arr_cur)-1):
            for j in range(i + 1, len(arr_cur)):
                tmp, ans = union(arr_cur[i], arr_cur[j]) # hợp giải 2 mệnh đề
                if (tmp == True): # Hợp giải được
                    if ans == []: # Mệnh đề rỗng
                        ans.append('{}') 
                        stopp = 1
                    else:
                        ans = sort_ascii(ans) # Sắp xếp các literal của mệnh đề
                    
                    str1 = '' # chuỗi literal không có từ khóa để dễ lưu
                    for i_ans in ans: 
                        str1 += i_ans
                    if str1 not in used:# Nếu mệnh đề chưa tồn tại trước đó 
                        used.append(str1)
                        str2 = ''
                        for i_ans in ans:
                            str2 += (i_ans + ' OR ')
                        str2 = str2[0:len(str2)-4]
                        add.append(str2) # thêm vào add

        for i in add:# thêm mệnh đề mới được tạo vào arr_cur
            s_a = split_String(i)
            arr_cur.append(s_a) 

        # Xuất sau mỗi lần lặp
        tmp_len = len(add)
        file.write(str(tmp_len))
        file.write('\n')
        for i in add:
            file.write(i)
            file.write('\n')

        if stopp == 1 or len(add) == 0:
            loop = 0
        add.clear()# xóa rỗng cho loop mới

    if stopp == 1:
        file.write('YES')
        file.write('\n')
    else:
        file.write('NO')
        file.write('\n')
    file.close()

#------------- Main --------------
def run(file_in, file_out):
    alpha, n, s =readFile(file_in)
    used.clear()
    PL_Resolution(alpha, n, s, file_out)