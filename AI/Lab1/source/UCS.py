import matplotlib.pyplot as plt
import readFile as rf
import drawMap as dm


def ucs(maze,start,goal):
    
    #lưu chi phí di chuyển từ điểm bắt đầu đến điểm đang xét
    Gn = {}  
    Gn[start]=0

    #tập các điểm đã mở
    visited =[]

    #tập các điểm biên
    openNodes = []
    openNodes.append(start)

    parent_map ={} 

    #điểm đang xét
    curPoint=start

    path=[]
    #chi phí di chuyển
    cost = 0 
    while openNodes:

        visited.append(curPoint)
        openNodes.remove(curPoint)

        #kiểm tra đích
        if curPoint== goal:
            path.append(curPoint)
            while(path[-1] in parent_map):
                path.append(parent_map[path[-1]])
            cost = len(path) -1 
            return path[::-1],cost

        #tìm các successor của curPoint   
        nearPoint = rf.findNearPoint(curPoint,maze)

        #đưa các successor vào tập mở nếu không nằm trong danh sách các điểm đã duyệt 
        for x in nearPoint:
            if x in visited:
                continue

            #cập nhật chi phí di chuyển từ điểm bắt đầu đến curPoint
            cost = Gn[curPoint] +1 
       
            # x nằm trong danh sách các điểm mở và chi phí di chuyển đến curPoint lớn hơn chi phí di chuyển đến x
            if x in openNodes and cost>=Gn[x]:
                continue            
            
            if x not in openNodes:
                openNodes.append(x)
            
            parent_map[x]=curPoint
            Gn[x]=cost


        #tìm điểm có chi phí đến nó nhỏ nhất trong tập mở
        cur = None 
        cost_cur =None
        for x in openNodes:
            if cur == None  or Gn[x] < cost_cur:
                cur=x
                cost_cur = Gn[x]

        curPoint = cur
        
        
    return path,len(path)-1

def run_ucs(file_path_in,file_path_out):

    bonus,maze= rf.read_file(file_path_in)

    start = rf.findStartPoint('S',maze)
    goal = rf.findEndPoint(maze)

    path,cost = ucs(maze,start,goal)

    plt= dm.visualize_maze(maze,bonus,start,goal,path)

    sample_file_name = "ucs.jpg"
    plt.savefig(file_path_out + '/' +sample_file_name)
   
    f = open(file_path_out + '/ucs.txt', "w")
    if cost < 0:
        f.write('NO')
    else:
        f.write(str(cost))
    f.close()
    plt.close()


