import math
import drawMap as dm
import readFile as rf
import os


def heuristicFunc(n, goal):
    x= goal[0] - n[0]
    y=goal[1] - n[1]

    result=[math.sqrt(x*x + y*y),abs(x)+abs(y),max(abs(x),abs(y))]

    return result


def A_star(maze,start,goal,visited,i):
    # Chi phi duong di tu diem start den diem hien tai
    Gn = {}  
    Gn[start]=0
    # uoc tinh chi phi den dich 
    Fn = {}     
    Fn[start] = heuristicFunc(start,goal)[i]

    open=[] # tap mo
    open.append(start)

    parent_map ={} # tap cha 

    curPoint=start # diem duoc xet
    path=[]
    cost =0
    while open:
        #neu diem duoc xet la dich
        if curPoint== goal:
            path.append(curPoint) #tra ve duong di dua tren tap cha parent
            while(path[-1] in parent_map):
                path.append(parent_map[path[-1]])
            cost = len(path) -1 
            return path[::-1],cost

        # tim diem lan can
        nearPoint =rf.findNearPoint(curPoint,maze)
        # update tap mo
        for x in nearPoint:             
            if x in visited: # diem lan can da duoc xet 
                continue
            cost = Gn[curPoint] + 1 + heuristicFunc(x,goal)[i]
            if x in open and cost >=  Fn[x]: # chi phi uoc tinh lon hon chi phi truoc
                continue
            if x not in open:
                open.append(x)

            Gn[x] = Gn[curPoint] + 1 #cap nhap chi phi duong di
            Fn[x]=cost # chi phi uoc tinh
            parent_map[x]= curPoint #cap nhat diem cha
                
        visited.append(curPoint)
        open.remove(curPoint)
        # tim diem be nhat trong tap mo
        cur = None 
        cost_cur =None
        for x in open:
            if cur == None  or Fn[x] < cost_cur:
                cur=x
                cost_cur = Fn[x]

        curPoint = cur
        
    
    return path,len(path)-1

def run_astar(file_path_in,file_path_out):

    bonus,maze= rf.read_file(file_path_in)
    
    start = rf.findStartPoint('S',maze)
    goal = rf.findEndPoint(maze)

    for i in range(len(heuristicFunc(start,goal))):
        visited =[]
        path,cost =A_star(maze,start,goal,visited,i)

        plt= dm.visualize_maze(maze,bonus,start,goal,path)

        sample_file_name = "/astar_heuristic_"+str(i+1)
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

            
         
        


        

        
        

            





