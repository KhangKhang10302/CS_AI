import os 
import Cau_4

OUTPUT='./OUTPUT'
INPUT ='./INPUT'

if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)
    
i=1
with os.scandir(INPUT) as level_2:
    for f in level_2:
        out_path = OUTPUT + '\output'+str(i) + '.txt'
            
        Cau_4.run(f.path, out_path)
        i=i+1