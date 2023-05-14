import os
import matplotlib.pyplot as plt
import heapq

import numpy as np

#---------------------vẽ map -----------------------
def visualize_maze(matrix, bonus, start, end, route=None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[i])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v') #^
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^') #v        
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    #2. Drawing the map
    ax=plt.figure(dpi=100).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=100,color='black')
    
    colors = np.random.rand(len(bonus))
    plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                s=100,c=[i for i in colors])

    plt.scatter([i[3] for i in bonus],[-i[2] for i in bonus],
                s=100,c=[i for i in colors])
    # for i in bonus :
    #     # colors = 'blue'
    #     colors = np.random.rand(1)
    #     plt.scatter([i[1]],[-i[0]],
    #         s=100,c=colors)
    #     plt.scatter([i[3]],[-i[2]],
    #         s=100,c=colors)

    plt.scatter(start[1],-start[0],marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='silver')

    plt.text(end[1],-end[0],'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    #plt.show()


    return plt
#--------------------------đọc file-----------------------------------
import numpy as np

 
a= [1,0,0,-1]
b= [0,-1,1,0]

def read_file(file_name: str = 'maze.txt'):  # hàm đọc có đọc có các ô dịch chuyển
    f=open(file_name,'r')
    n_gate_points = int(next(f)[:-1])
    gate_points = []
    for i in range(n_gate_points): 
        x, y, xx, yy = map(int, next(f)[:-1].split(' '))
        gate_points.append((x, y, xx, yy))

    text=f.read()
    matrix=[list(i) for i in text.splitlines()]
    f.close()

    return gate_points, matrix


def findStartPoint(element, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return (i, j)
def findEndPoint(matrix):
    column=len(matrix[0])
    row=len(matrix)
    for i in range(len(matrix[0])):
        if(matrix[0][i]==" "):
            return (0,i)
    for i in range(len(matrix[row-1])):
        if(matrix[row-1][i]==" "):
            return (row-1,i)
    for i in range(len(matrix)):
        if(matrix[i][0]==' ' ):
            return (i,0)
        if(  matrix[i][column-1]==' '):
            return (i,column-2)



def findNearPoint(p,maze):
    near_point=[]
    column=len(maze[0])
    row=len(maze)
    for i in range(4) :
        m =p[0]+a[i]
        n= p[1]+b[i]
        if( m>=0 and  n>=0 and m<row and n <column and maze[m][n]!='x' ):
            near_point.append((m,n))
    return near_point

#-----------------------thuật toán----------------------------------------

def makearray2D(matrix): # tạo mảng 2 chiều đánh dấu 
    arr = []
    for i in range(len(matrix)):
        arr.append([])
        for  j in range(len(matrix[0])):
            arr[i].append(0)      
    return arr
def makearray3D(matrix):# tạo mảnh 3 chiều đánh dấu
    arr = []
    for i in range(len(matrix)):
        arr.append([])
        for  j in range(len(matrix[0])):
            arr[i].append([])      
            for  k in range(2):
                arr[i][j].append(0)
    return arr

def tracee(start, end, trace, gate ):# truy cuất đường đi 
    xx = end[0] 
    yy = end[1] 
    route = []
    route.append((xx, yy))
    while (xx != start[0] or yy !=start[1]):
        
        if(trace[xx][yy] == 0):
            xx = xx + 1
        elif (trace[xx][yy] == 1):
            xx = xx - 1
        elif (trace[xx][yy] == 2):
            yy = yy + 1
        elif (trace[xx][yy] == 3):
            yy = yy - 1
        else:                       # nếu là ô dịch chuyển 
            res = gate[xx][yy][0]
            yy = gate[xx][yy][1]
            xx = res

        route.append((xx, yy))
    return route

def ucs_advance(matrix, start, gate):
    d = makearray2D(matrix)
    trace = makearray2D(matrix)

    dx = [ -1, 1, 0, 0 ]
    dy = [ 0, 0, -1, 1 ]
    
    # khởi tạo trọng số ban đầu là vô cùng lớn
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            d[i][j] = 10000000 

    d[start[0]] [start[1]]= 0 # bắt đầu ở start

    pq = []
    heapq.heappush(pq, (0, start[0], start[1], 0)) # hàng đợi ưu tiên lưu trọng số, tọa đô x y, giá trị đánh dấu

    while (len(pq) != 0) : 
        tmp = heapq.heappop(pq)
        du = tmp[0]
        uu = tmp[1]
        vv = tmp[2]
        check = tmp[3]# biến đánh dấu = 1 nếu cổng dịch chuyển được đến = phép dịch chuyển.
        if(matrix[uu][vv] == 'o' and check == 0):
            continue

        if (du != d[uu][vv]): #nếu đỉnh lấy ra trọng số khác trọng số ngắn nhất hiện tại => ko tốt bỏ qua 
            continue
    
        for i in range(4):
            if (uu + dx[i] >= 0) and (uu + dx[i] < len(matrix)) and (vv + dy[i] >= 0) and (vv + dy[i] < len(matrix[0])): # đảm bảo ô sắp đi không out khỏi biên
                u1 = uu + dx[i]
                v1 = vv + dy[i]
                if (matrix[u1][v1] != 'x'): # TH có thể đi
                    if (matrix[u1][v1] == ' ' and d[u1][v1] > du + 1 ) : # mà là ô trống 
                        d[u1][v1] = du + 1
                        heapq.heappush(pq, (d[u1][v1], u1, v1, 0))
                        trace[u1][v1] = i
                    elif (matrix[u1][v1] == 'o' ) : # mà là ô dịch chuyển
                        u11 = gate[u1][v1][0]
                        v11 = gate[u1][v1][1]
                        if( d[u11][v11] > du + 1):
                            # cho ô cuối cổng vào heap
                            d[u11][v11] = du + 1
                            heapq.heappush(pq, (d[u11][v11], u11, v11, 1)) # ô cuối cổng được đến = dịch chuyển nên check = 1
                            trace[u11][v11] = 4
                            # cho luôn ô đầu cổng vào heap
                            d[u1][v1] = du + 1
                            heapq.heappush(pq, (d[u1][v1], u1, v1, 0))# ô đầu cổng cũng cung được push vào heap nhưng cho check =0
                            trace[u1][v1] = i
    return d, trace


def run_advance(file_path_in,file_path_out):
    gate_points, matrix = read_file(file_path_in)
    start = findStartPoint('S', matrix)
    end = findEndPoint(matrix)
    
    gate = makearray3D(matrix)

    for i in gate_points: # lưu các cổng thông nhau qua lại 
        gate[i[0]][i[1]][0] = i[2]
        gate[i[0]][i[1]][1] = i[3]

        gate[i[2]][i[3]][0] = i[0]
        gate[i[2]][i[3]][1] = i[1]

    d, trace = ucs_advance(matrix, start, gate)

    f = open(file_path_out + '/algo2.txt', "w")
    route = []

    if (d[end[0]][end[1]] != 10000000): 

        f.write(str(d[end[0]][end[1]]))
        

        route = tracee(start, end, trace, gate)
        route.reverse()
        

    else:
       f.write('NO')
    f.close()

    plt =visualize_maze(matrix,gate_points,start,end, route)
    sample_file_name = "algo2.jpg"
    plt.savefig(file_path_out + '/' +sample_file_name)
    plt.close()
