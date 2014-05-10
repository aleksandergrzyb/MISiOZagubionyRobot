from argparse import ArgumentParser
from random import randint, random
from Tkinter import *

# Example of use
# python map.py -r 5 -c 5 -f /home/jacek/mapa.txt -v

class MapGenerator:
    def __init__(self, path_to_file, rows, cols):
        self.rows = rows
        self.cols = cols
        self.path = path_to_file
        self.num_of_bldgs = 0

    def generate_map(self):
        if self.rows < 1 or self.cols < 1:
            return 'Map must be 3x3 or bigger'
        tiles_type = []
        # Pick type of tile
        # TODO change range of tiles generation to 3
        for i in range(self.rows):
            tiles_type.append([])
            for j in range(self.cols):
                tiles_type[i].append(randint(1,1))

        # Each building is represented by 5 params
        # height, length and width
        # x and y position of bottom leftmost corner
        self.height = []
        self.length = []
        self.width = []
        self.x = []
        self.y = []
        for i in range(self.rows):
            for j in range(self.cols):
                # low, dense buildings
                if tiles_type[i][j] == 1:
                    for a in range(0, 4):
                        for b in range(0, 6):
                            l = 1.0 + 2.0*random()
                            w = 1.0 + random()
                            h = 0.0 + 10.0*random()
                            x = 1.0 + float(a)*5.0
                            y = 1.0 + float(b)*3.0
                            if l < 4.0:
                                x += (4.0-l)*random()
                            if w < 3.0:
                                y += (3.0-w)*random()

                            x += float(i)*20.0
                            y += float(j)*20.0
                            self.height.append(h)
                            self.length.append(l)
                            self.width.append(w)
                            self.x.append(x)
                            self.y.append(y)
                            self.num_of_bldgs += 1
                if tiles_type[i][j] == 2:
                    pass
                    # TODO teren o sredniej zabudowie
                if tiles_type[i][j] == 3:
                    pass
                    # TODO teren o wysokiej zabudowie
        # TODO
        # random rotation of 0, 90, 180 or 270 degrees
        # dodanie wsp. bazowych do wsp. bezwzglednych

    def save_map(self, path="/home/jacek/Studia/MISIO/MISiOZagubionyRobot/mapa.txt"):
        self.path = path
        with open(self.path, 'w') as f:
            f.write('%d \n' % self.num_of_bldgs)
            f.write('%d %d \n' % (self.rows, self.cols))
            for i in range(self.num_of_bldgs):
                f.write('%.2f %.2f %.2f %.2f %.2f \n' % (self.x[i], self.y[i],self.height[i], self.width[i], self.length[i]))
                          
    def simple_vis(self):
        # Simple visualization of the created map
        # Using Tkinter
        master = Tk()
        dis = Canvas(master, width=self.rows*160, height=self.cols*160)
        for i in range(self.num_of_bldgs):
            if self.height[i] <= 3.33:
                dis.create_rectangle(self.x[i]*8, self.y[i]*8, self.x[i]*8+self.length[i]*8, self.y[i]*8+self.width[i]*8, fill="blue") 
            elif self.height[i] <= 6.66:
                dis.create_rectangle(self.x[i]*8, self.y[i]*8, self.x[i]*8+self.length[i]*8, self.y[i]*8+self.width[i]*8, fill="green") 
            else:
                dis.create_rectangle(self.x[i]*8, self.y[i]*8, self.x[i]*8+self.length[i]*8, self.y[i]*8+self.width[i]*8, fill="red") 
        dis.pack()
        mainloop()
                                        
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", "--rows", dest="map_row_num",
                        help="number of rows", metavar="ROWS", default=10)
    parser.add_argument("-c", "--cols", dest="map_col_num",
                        help="number of columns", metavar="COLS", default=10)
    parser.add_argument("-f", "--file", dest="map_path",
                        help="file path for saving", metavar="PATH", default='./map')
    parser.add_argument("-v", "--visualize", dest="map_visualize",
                        help="visualize the map", metavar="VISUAL", action='store_const',
                        const=True, default=False)
    args = parser.parse_args()
    MG = MapGenerator(args.map_path, int(args.map_row_num), int(args.map_col_num))
    MG.generate_map()
    MG.save_map()
    if args.map_visualize == 1:
        MG.simple_vis()