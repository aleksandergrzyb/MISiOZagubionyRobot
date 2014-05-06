from argparse import ArgumentParser
from random import randint

map_row_num = 10
map_col_num = 10
map_path = ""

def generate_map():
    if map_row_num < 3 or map_col_num < 3:
        return 'Map must be 3x3 or gigger'
    tiles_type = []
    for i in range(map_row_num):
        for j in range(map_col_num):
            tiles_type.append()
            tiles_type[i].append(randint(1,3))
    bldgs = []   # buildings
    for i in range(map_row_num):
        for j in range(map_col_num):
            if tiles_type[i][j] == 1:
                # teren o niskiej zabudowie
                for a in range(4):
                    for b in range(8):
                        l = randint(1,4)
                        w = randint(1,3)
                        h = randint(1,3)
                        x = 1 + a*5
                        y = 1 + b*3
                        if l < 4:
                            x += randint(0, 4-l)
                        if w < 3:
                            y += randint(0, 3-y)
                        bldgs.append({"length":l, "width":w, "height":h,\
                                      "x":x, "y":y})
            if tiles_type[i][j] == 2:
                # teren o średniej zabudowie
            if tiles_type[i][j] == 3:
                # teren o wysokiej zabudowie
    # losowy obrót o 0, 90, 180 lub 270 stopni
    # dodanie wsp. bazowych do wsp. bezwzględnych
                        
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", "--rows", dest="map_row_num",
                        help="number of rows", metavar="ROWS", default=10)
    parser.add_argument("-c", "--cols", dest="map_col_num",
                        help="number of columns", metavar="COLS", default=10)
    parser.add_argument("-f", "--file", dest="map_path",
                        help="file path for saving", metavat="PATH", default='./map')