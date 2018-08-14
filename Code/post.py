import json
import re
from mpi4py import MPI
import time

start_time = time.time()

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()



Grid_File = "melbGrid.json"
Insta_File="bigInstagram.json"

#load grid data
def load_grid(Grid_File):
    set = []
    with open(Grid_File,"r") as f:
        data = json.load(f)
        for x in data['features']:
            set.append(x['properties'])
    return set


def parse_file(line, grids):
    coordinates = re.search('"coordinates":\[([\d.-]+),([\d.-]+)\]', line)
    if coordinates and coordinates.group(1)and coordinates.group(2):
        point = [float(coordinates.group(2)), float(coordinates.group(1))]
        (x,y) = point
        for grid in grids:
            if x >= grid['xmin'] and x <= grid['xmax'] and y >= grid['ymin'] and y <= grid['ymax']:
                return grid["id"]
    return None

grids = load_grid(Grid_File)

#initialize dictionary of grid
grid_dict = {}
for grid in grids:
    grid_dict[grid['id']] = 0

#read data file, assign read task to each process equally
with open(Insta_File, "r") as f:
    line_num = 0
    for line in f:
        line_num += 1
        if(line_num % size) == rank:
            zone = parse_file(line, grids)
            if zone:
                grid_dict[zone] += 1

 #wait for each process, and synchronize
comm.Barrier()

#gather data from each process
data = comm.gather(grid_dict)

#sort and print method
#sort by descending  order, rank by value
def sort(d):
    return sorted(d.items(), key=lambda x:x[1], reverse=True)

#print a dictionary in certain order
def print_dict(format, d):
    for (key,value) in d:
        print(format % (key,value))

    print(" ")

#master process sort data
if rank == 0:
    result = {}
    rows = {}
    cols = {}
    for process in data:
        for (key,value) in process.items():
            if result.get(key)== None:
                result[key] = 0
            result[key] += value

    #gather rows and colums
    for (key,value) in result.items():
        if rows.get((key[0]))==None:
            rows[key[0]] = 0
        rows[key[0]] += value

        if cols.get(key[1])==None:
            cols[key[1]] = 0
        cols[key[1]] += value

    print_dict("%s: %d posts", sort(result))
    print_dict("%s-Row: %d posts", sort(rows))
    print_dict("Column %s: %d posts", sort(cols))

    #print total time to execute the program
    print("Used time:", time.time()-start_time, "s")


