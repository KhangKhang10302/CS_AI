import math
import drawMap as dm
import readFile as rf
import os



def heuristicFunc(n, goal):
    x= goal[0] - n[0]
    y=goal[1] - n[1]

    result=[math.sqrt(x*x + y*y),abs(x)+abs(y),max(abs(x),abs(y))]

    return result

def gbfs(maze,start,goal,i):
    
    #heuristic ước tính chi phí đến đích từ điểm hiện tại
    Hn = {}     
    Hn[start] = heuristicFunc(start,goal)[i]

    #tập các điểm biên
    open=[]
    open.append(start)
    

    #tập các điểm đã mở
    close =[]

    parent_map ={} 

    curPoint=start
    path=[]
    cost = 0
    while open:
        open.remove(curPoint)
        close.append(curPoint)

        #kiểm tra đích
        if curPoint== goal:
            path.append(curPoint)
            while(path[-1] in parent_map):
                path.append(parent_map[path[-1]])
            cost = len(path) -1 
            return path[::-1],cost

        #tìm các successor của curPoint 
        nearPoint =rf.findNearPoint(curPoint,maze)

        #đưa các successor vào tập mở nếu không nằm trong danh sách các điểm đã duyệt 
        for x in nearPoint:             
            if x in close:
                continue
            
            #tính heuristic của điểm x
            Heuristic = heuristicFunc(x,goal)[i]

            if x not in open:
                open.append(x)

            Hn[x]=Heuristic
            parent_map[x]= curPoint
        
        
        #tìm điểm có ước lượng nhỏ nhất trong tập mở
        cur = None 
        cost_cur =None
        for x in open:
            if cur == None  or Hn[x] < cost_cur:
                cur=x
                cost_cur = Hn[x]

        curPoint = cur
        
    return path,len(path)-1
def run_gbfs(file_path_in,file_path_out):

    bonus,maze= rf.read_file(file_path_in)

    start = rf.findStartPoint('S',maze)
    goal = rf.findEndPoint(maze)

    for i in range(len(heuristicFunc(start,goal))):
        path,cost = gbfs(maze,start,goal,i)
        plt= dm.visualize_maze(maze,bonus,start,goal,path)

        sample_file_name = "/gbfs_heuristic_"+str(i+1)
        path_out =  file_path_out+ sample_file_name

        if not os.path.exists(path_out):
                os.makedirs(path_out)

        plt.savefig(path_out + sample_file_name+ ".jpg")

        f = open(path_out  + sample_file_name +'.txt', "w")
        if cost < 0:
            f.write('NO')
        else:
            f.write(str(cost))
        f.close()
        plt.close()

