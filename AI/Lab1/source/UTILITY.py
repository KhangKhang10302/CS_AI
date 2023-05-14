
import A_STAR as AS
import math
import drawMap as dm
import readFile as rf

#tìm các điểm có lợi khi đi từ một điểm đến đích
def setBonus(path,bonus,start,goal):
    result=[]
    for x in bonus:
        if x in path: 
            continue
        cost_start = AS.heuristicFunc(start,goal)[1] # ước tính chi phí từ điểm bắt đầu đến kết thúc

        #ước tính tổng khoảng cách khi đi qua điểm thưởng 
        cost_bonus = AS.heuristicFunc(start,(x[0],x[1]))[1] + AS.heuristicFunc((x[0],x[1]),goal)[1]

        if cost_start > cost_bonus + x[2]: #điều kiện có lợi
            result.append(x)
        
    return result

def utility(maze,bonus,start,goal):

    curPoint=start
    path =[]

    visited =[]
    visited.append(start)
    cost=0

    if AS.A_star(maze,start,goal,visited,1)[0]:
        visited =[]
        visited.append(start)
        while curPoint!=goal:          
            
            set_bonus=setBonus(path,bonus,curPoint,goal)        # các điểm điểm thưởng có lợi khi đi từ curPoint tới đích
            cost_max =None
            G = None     
            for x in set_bonus: # lấy điểm thưởng ở xa đích nhất
                cost_bonus = AS.heuristicFunc((x[0],x[1]),goal)[1] 
                if cost_max == None or cost_bonus > cost_max:
                    cost_max=cost_bonus
                    G = x

            if(G in bonus): #loại ra khỏi tập điểm thưởng
                bonus.remove(G)
                Goal_bonus=(G[0],G[1])
                c =G[2]
            else:
                Goal_bonus = goal
                c = 0

            path_1 =  AS.A_star(maze,curPoint,Goal_bonus,visited,1)[0] # tìm đường đi từ curPoint đến điểm thưởng 
                                                                     #và không được đi qua những điểm đã đc đi qua ở chặng trước
            
            path_2 = AS.A_star(maze,Goal_bonus,goal, path + path_1,1)[0] # tìm đường đi từ điểm thưởng đến đích 

            if path_2:         # nếu tồn tại đường đi đến đích, chọn path_1
                path = path + path_1
                cost = cost + c
                curPoint = Goal_bonus # đi tiếp từ điểm thưởng này

            visited = [x for x in path]
            
    path = list(dict.fromkeys(path))

    cost = cost + len(path)-1 
    return path,cost
def run_utility(file_path_in,file_path_out):

    bonus,maze= rf.read_file(file_path_in)
    backup_bonus =[x for x in bonus]
    start = rf.findStartPoint('S',maze)
    goal = rf.findEndPoint(maze)

    path,cost = utility(maze,bonus,start,goal)

    f = open(file_path_out + '/algo1.txt', "w")
    if cost < 0:
        f.write('NO')
    else:
        f.write(str(cost))
    f.close()
    plt= dm.visualize_maze(maze,backup_bonus,start,goal,path)
    

    sample_file_name = "algo1.jpg"
    plt.savefig(file_path_out + '/' +sample_file_name)
    plt.close()









    

