import matplotlib.pyplot as plt
import os
import readFile as rf
import drawMap as dm


def dfs(maze,start,goal):
    stack=[] # lưu đường đi 
    stack.append(start) # thêm dỉnh bắt đầu vào 
    visited =[] # mảng lưu đỉnh đã thăm 
    path =[] 
    parent_map ={}
    cost =0 # biến đếm chi phí 
    while(stack): # khi stack khác rỗng thì chạy 
        cur_point=stack.pop() # đỉnh hiện tại lấy từ stack 
        visited.append(cur_point) #lưu đỉnh vào tập đã thăm 
        
        if cur_point == goal: # nếu đỉnh lấy ra là đích 
            path.append(cur_point) 
            while(path[-1] in parent_map):# truy ngược từ parent_map tìm ra path
                path.append(parent_map[path[-1]])
            cost = len(path) - 1 
            return path[::-1],cost# trả về đườnh đi, chi phí

        near_point =rf.findNearPoint(cur_point,maze) #tìm các successor của curPoint

        #đưa các successor vào tập mở nếu không nằm trong danh sách các điểm đã duyệt 
        for i in near_point:
            if i in visited: # nếu i đã trong tập đã thăm rồi thì bỏ qua
                continue
            if i in stack: # nếu stack có i thì move và thêm lại vào sau 
                stack.remove(i)
            stack.append(i)
            parent_map[i]=cur_point # lưu cha i là cur_point để khi gặp đích truy xuất đường đi 
            

    return path,len(path)-1




def run_dfs(file_path_in,file_path_out):

    bonus,maze= rf.read_file(file_path_in)

    start = rf.findStartPoint('S',maze)
    goal = rf.findEndPoint(maze)

    path,cost = dfs(maze,start,goal)


    plt= dm.visualize_maze(maze,bonus,start,goal,path)

    sample_file_name = "dfs.jpg"
    plt.savefig(file_path_out + '/' +sample_file_name)

    f = open(file_path_out + '/ .txt', "w")
    if cost < 0:
        f.write('NO')
    else:
        f.write(str(cost))
    f.close()
    plt.close()

   






