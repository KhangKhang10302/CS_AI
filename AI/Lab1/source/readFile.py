import numpy as np


a= [1,0,0,-1]
b= [0,-1,1,0]

def read_file(file_name: str = 'maze.txt'):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))

  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()

  return bonus_points, matrix


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