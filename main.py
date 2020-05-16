from PIL import Image               #importing library for image manipulation
from population import Population
import path_compose as pc
import os
import sys

#initial images consist from single simple colors, names are written in the array
initial_population = ["brown", "red", "green", "purple", "pink", "black", "yellow", "orange", "white", "blue"]
orig_image = "monalisa.png" #original image name like which result should look like
parents_cnt = 2          #number of best images which will be involved in crossover
image_height = 512       #height of images with which we will work in pixels
image_width = 512        #width of images with which we will work in pixels
image_size = (image_height, image_width)                 #tuple of height and width, it is convenient
min_figure_size = 3      #one mutation draws one square or rhombus with random size, so it is kinda minimum bound of range for random size
max_figure_size = 30     #one mutation draws one square or rhombus with random size, so it is kinda maximum bound of range for random size
                         #size of square is the side length / 2, size of rhombus is the distance from center to sharp corner.
                         #SQUARES ARE ALWAYS PARALLEL TO IMAGE FRMAE SIDES, RHOMBUSES ARE SUCH SQUARES BUT ROTATED BY 45 DEGREES
max_disturbance = [0, 0, 16, 16, 16, 16, 16, 16, 16, 16]#when we mutate, we draw as aforementioned square or rhombus, and max_disturbance
                                                        #determines how color is chosen for the figure. We write down the values of RGB
                                                        #of random pixel of the child which is going to be mutated. Then we change them
                                                        #by differing each of them randomly. The defined max_disturbance value is the
                                                        #range for random difference. So the figure is colored with a new color we obtained.
                                                        #It is array because we can define mutation disturbance for each children.
                                                        #For two first children it is 0 because we do not want our fitness to decrease
                                                        #if every mutated child will be worse than parents
def resize_image():                   #function for compressing or stretching original image till the size with which we will work
    path = pc.rel_path(orig_image)    #taking absolute path of the original image
    image = Image.open(path)
    image = image.resize(image_size)  #changing size of the original image
    image.save(path)                  #saving changes into the file system

def init_population():                       #function for creating initial images
    paths = []                               #array for defining absolute paths to initial images
    for i in range(len(initial_population)):
        cur_path = pc.rel_path(i)                           #composing absolute path to the initial image number i (numbering from 0)
        paths.append(cur_path)                              #insert composed path into array of absolute paths
        cur_color = initial_population[i]                   #taking pre-defined color for initial image number i
        new_image = Image.new("RGB", image_size, cur_color) #creating new image with pre-defined size and color
        new_image.save(cur_path, "png")                     #saving created image with the composed path
    return paths


def start():                    #function for starting the algorithm
    resize_image()              #TODO SEE COMMENTS OF FUNCTION
    paths = init_population()   #TODO SEE COMMENTS OF FUNCTION
    cur_folk = Population(orig_image, paths, image_size, parents_cnt, min_figure_size, max_figure_size, max_disturbance)
                                                                #we create object of class Population, this class stays for all needed
                                                                #information about current population to be saved in one place. First of
                                                                #all, we pass arguments to the constructor, some of which are pre-defined
                                                                #constants, which I explained when defined constants. Also, class have
                                                                #array of absolute paths for current generation population, and functions
                                                                #for making crossover, mutation and calculating fitness.
    while True:                                    #process will run infinitely - the more generation number - the better images generated
        cur_folk.calc_fitness_all()                #before another one generation evolution, calculate fitnesses of current generation
        for i in range(len(cur_folk.fitness)):
            print(cur_folk.fitness[i][0], end=" ") #printing fitness of every current generation member
            if i == len(cur_folk.fitness) - 1:     #it is convenient to monitor progress of evolution
                print("")
        print(cur_folk.generation)                 #generation is also for convenience of monitoring the evolution
        cur_folk.evolve()                          #evolve current generation, that is make new children


start() #start evolution process

