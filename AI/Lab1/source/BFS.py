import drawMap as dm
import readFile as rf
import queue



def bfs(u, v, matrix,used,trace):
    dx = [ -1, 1, 0, 0 ]
    dy = [ 0, 0, -1, 1 ]
    cnt = 0 # đếm số lượng đỉnh mở
    cnt += 1
    used[u][v]=1 # mảng đánh dấu tọa đôj đã thăm hay chưa 
    h = queue.Queue() #hàng đợi các đỉnh mở 
    h.put(u)
    h.put(v)
    while h.qsize()!=0  : # khi còn đỉnh trong queue thì chạy
        uu=h.get()
        vv=h.get()
        for i in range(4): 
            if (uu + dx[i] >= 0) and (uu + dx[i] < len(matrix)) and (vv + dy[i] >= 0) and (vv + dy[i] < len(matrix[0])): # kiểm tra xem đỉnh chuẩn bị đi có out khỏi ma trận không
                u1 = uu + dx[i] #tọa độ x đỉnh kề cb thăm
                v1 = vv + dy[i] #tọa độ x đỉnh kề cb thăm
                if (used[u1][v1] == 0) and (matrix[u1][v1] != 'x'): #Kiểm tra đỉnh đã thăm chưa và có được phép đi không
                    h.put(u1) #cho toa độ x cua đỉnh vào queue
                    h.put(v1) #cho toa độ y cua đỉnh vào queue
                    cnt+=1  #đếm vào tập đỉnh mở
                    used[u1][v1] = used[uu][vv] + 1 #đánh dấu đỉnh đã thăm rồi
                    trace[u1][v1] = i #mảng lưu đường đi gán đỉnh được đi từ hướng i
    
    return cnt


def makearray2D(matrix):
    arr = []
    for i in range(len(matrix)):
        arr.append([])
        for  j in range(len(matrix[0])):
            arr[i].append(0)      
    return arr

def tracee(start, end,trace):# truy ngược tìm đường đi bắt đầu từ end
    xx = end[0] 
    yy = end[1] 
    route = []
    route.append((xx, yy))

    # thực hiện truy dừng khi gặp lại đỉnh bắt đầu tùy vào được đi từ hướng nào mà truy ra 
    while (xx != start[0] or yy !=start[1]):
        if(trace[xx][yy] == 0):
            xx = xx + 1
        elif (trace[xx][yy] == 1):
            xx = xx - 1
        elif (trace[xx][yy] == 2):
            yy = yy + 1
        else:
            yy = yy - 1
        route.append((xx, yy))
    return route
    


def run_bfs(file_path_in,file_path_out):
    bonus_points, matrix = rf.read_file(file_path_in)
    s = matrix
    start = rf.findStartPoint('S',matrix)
    end = rf.findEndPoint(s)
    used = makearray2D(matrix) # tạo mảng đánh dấu tọa độ đỉnh đã thăm hay chưa 
    trace = makearray2D(matrix) # tạo mảng lưu hướng đi của một đỉnh

    cnt = bfs(start[0], start[1], matrix,used,trace)
    
    
    route = []
    if used[end[0]][end[1]] != 0: #nếu có đường đi thoát khỏi mê cung 
        route = tracee(start, end,trace) # truy ra đường đi 
        route.reverse() # đường đi khi truy bị ngược nên đảo lại
   
    
    plt = dm.visualize_maze(matrix,bonus_points,start,end, route)
    sample_file_name = "bfs.jpg"
    plt.savefig(file_path_out + '/' +sample_file_name)

    f = open(file_path_out + '/bfs.txt', "w")
    if used[end[0]][end[1]] - 1 < 0:
        f.write('NO')
    else:
        f.write(str(used[end[0]][end[1]] - 1))
    f.close()
    plt.close()



    







