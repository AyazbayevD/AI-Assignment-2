import random
import sys

max_figure_types = 2

class Figure: #class for defining pixels which will be painted and some figure will be painted on top of some image
    def __init__(self, center_x, center_y, figure_size, image_size): #constructor
        self.center_x = center_x                        #defining center point of the figure
        self.center_y = center_y
        self.figure_size = figure_size                  #TODO SEE EXPLANATION OF min_figure_size IN main.py
        self.image_size = image_size                    #writing down size of images with which code is working
        self.type = random.randint(1, max_figure_types) #deciding randomly which figure to build

    def not_exceed_borders(self, x, y):             #function to check if some coordinates are out of image frame
        (height, width) = self.image_size
        if 0 <= x < height and 0 <= y < width:
            return True
        else:
            return False

    def calculate_pixels(self):                     #function to find pixels of some figure
        if self.type == 1:
            return self.calculate_pixels_square()   #depending on type, it is square or rhombus
        elif self.type == 2:                        #THERE ARE ABILITY TO INCLUDE MORE FIGURES
            return self.calculate_pixels_rhombus()
        else:
            print("invalid figure type!")
            sys.exit()

    def calculate_pixels_square(self): #finding pixels of square
        figure_pixels = []             #array of pixels of square
        (height, width) = self.image_size #then according to square properties, we find its pixels
        for i in range(max(0, self.center_x - self.figure_size), min(height, self.center_x + self.figure_size + 1)):
            for j in range(max(0, self.center_y - self.figure_size), min(width, self.center_y + self.figure_size + 1)):
                figure_pixels.append((i, j))
        return figure_pixels

    def calculate_pixels_rhombus(self): #finding pixels of rhombus
        figure_pixels = []              #array of pixels of rhombus
        (height, width) = self.image_size #then according to rhombus properties, we find its pixels
        for i in range(max(0, self.center_x - self.figure_size), min(height, self.center_x + self.figure_size + 1)):
            for j in range(max(0, self.center_y - self.figure_size), min(width, self.center_y + self.figure_size + 1)):
                if abs(i - self.center_x) + abs(j - self.center_y) <= self.figure_size:
                    figure_pixels.append((i, j))
        return figure_pixels
