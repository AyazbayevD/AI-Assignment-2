from PIL import Image
from figure import Figure
import path_compose as pc
import copy
import math
import random

class Population:
    def __init__(self, orig_image, members, image_size, parents_cnt, min_figure_size, max_figure_size, max_disturbance): #constructor
        self.orig_image = orig_image            #writing down original image
        self.members = copy.deepcopy(members)   #writing down population members
        self.image_size = image_size            #writing down size of images, with which code will work
        self.parents_cnt = parents_cnt          #writing down numbers of images which will be involved in crossover
        self.min_figure_size = min_figure_size  #TODO SEE COMMENTS FOR CONSTANTS IN "main.py"
        self.max_figure_size = max_figure_size  #TODO SEE COMMENTS FOR CONSTANTS IN "main.py"
        self.max_disturbance = max_disturbance  #TODO SEE COMMENTS FOR CONSTANTS IN "main.py"
        self.size = len(members)                #writing down amount of members in one generation population
        self.fitness = []                           #initially, fitnesses are not calculated,
                                                    #elements of the array will be as follows: tuple of fitness score and
                                                    #image for which this fitness is calculated, respectively
        self.generation = 0                     #we initialized object of current class once in 'main.py',
                                                #before we started the process of evolution, that means at 0-th generation

    def calc_fitness_all(self):       #function for calculating fitness for all current generation population
        self.fitness = []             #initially, fitnesses are not calculated
        for i in range(self.size):                                           #traversing every population member
            self.fitness.append([self.calc_fitness_one(self.members[i]), i]) #calculating fitness for it
        self.fitness.sort(reverse=True)    #after fitnesses are calculated, sort them by decreasing of fitnesses

    def calc_fitness_one(self, image_path):            #function for calculating fitness of one particular image
        orig_image = pc.rel_path(self.orig_image)      #composing absolute path name for original image
        art_image = pc.rel_path(image_path)            #composing absolute path name for current child
        orig_pixels = Image.open(orig_image).load()    #getting array of pixels of original image
        art_pixels = Image.open(art_image).load()      #getting array of pixels of current child image
        fitness = 0                                    #initially, fitness is 0
        (height, width) = self.image_size              #writing down height and width of images in pixels
        for i in range(height):                        #considering every possible pixel coordinates
            for j in range(width):
                orig_pixel = orig_pixels[i, j]         #writing down pixels of original image
                art_pixel = art_pixels[i, j]           #writing down pixels of current children image
                x = math.sqrt(((orig_pixel[0] - art_pixel[0]) ** 2) + ((orig_pixel[1] - art_pixel[1]) ** 2) + (
                            (orig_pixel[2] - art_pixel[2]) ** 2))  #first of all writing down constant x as
                                                                   #square root of sum of squares of RGB values differences
                var = 30                                           #then define variance value for NORMAL DISTRIBUTION
                fitness += (1 / (var * math.sqrt(math.pi * 2))) * (math.e ** (((x / var) ** 2) * (-0.5)))
                                                                   #adding to fitness score NORMAL DISTRIBUTION value of x
                                                                   #I decided to choose NORMAL DISTRIBUTION because when pixels
                                                                   #difference is very small it is not so critical. Otherwise, our eyes
                                                                   #cannot build illusion of similarity.
        return fitness

    def find_best(self):                                        #function for finding best parents among current population members
        best_images = []                                        #array of paths to such images
        self.fitness.sort(reverse=True)                         #sorting fitness by decreasing order of fitnesses
        for i in range(self.parents_cnt):                           #traversing only first needed amount of parents
            best_images.append(self.members[self.fitness[i][1]])    #append the path of image to the array
        return best_images

    def crossover(self, child_id, parents):                     #function for making crossover between parents
        child = Image.new("RGB", self.image_size, "white")      #creating child with undetermined pixels, let them be white
        child_pixels = child.load()                             #getting pixels of the child
        parents_pixels = []                                     #array of arrays of pixels of parents
        for i in range(self.parents_cnt):                       #traversing parents paths
            cur_path = pc.rel_path(parents[i])                  #composing absolute path of some parent
            cur_pixels = Image.open(cur_path).load()            #getting pixels of some parent
            parents_pixels.append(cur_pixels)                   #appending this array of pixels into one array
        (height, width) = self.image_size          #writing down height and width of images in pixels
        figure_size = random.randint(self.min_figure_size, self.max_figure_size) #we divide pixels into small squares and put into the
                                                                                 #child this square of random parent
                                                                                 #so we take random square side between pre-defined values
        for i in range(0, height, figure_size):                              #traversing all pixels coordinates
            for j in range(0, width, figure_size):                           #with period of square side value, because we will color
                                                                             #not one pixel, but a bunch of pixels of the child
                parent_id = random.randint(0, self.parents_cnt - 1)          #taking random parent
                for k in range(i, min(height, i + figure_size)):             #traversing current square coordinates
                    for l in range(j, min(width, j + figure_size)):
                        child_pixels[k, l] = parents_pixels[parent_id][k, l] #coloring this square of randomly taken parent into child

        incomplete_path = "image" + str((self.generation + 1) * self.size + child_id)
                                                   #we accumulate all images, because perodically 
                                                   #'permission denied' issue arises, so we calculate 
                                                   #image number of next generation, which will newborn child
                                                   #have
        complete_path = pc.rel_path(incomplete_path)    #compose absolute path for newborn child
        child.save(complete_path, "png")                #save child image into that path
        return incomplete_path          

    def new_population(self, parents):              #function for generate new generation population, given parents
        new_images = []                             #array of new images path
        for i in range(self.size):                  #generating child 'pre-defined amount' times
            child = self.crossover(i, parents)      #generating current child
            new_images.append(child)                #append path of the child to the array
        return new_images

    def mutate_all(self, images):                                   #function for mutation of all children except first needed
                                                                    #TODO EXPLANATION IS IN main.py, SEE max_disturbance CONSTANT
        for i in range(self.size):
            if i >= self.parents_cnt:                               #leaving needed amount of children without mutation
                self.mutate_one(images[i], self.max_disturbance[i]) #mutating other children

    def mutate_one(self, image, max_disturbance):     #function for making mutation of one particular child
        path = pc.rel_path(image)                     #getting absolute path to the current child image
        to_be_mutated_image = Image.open(path)
        image_pixels = to_be_mutated_image.load()     #getting array of pixels of the current child image
        (height, width) = self.image_size             #getting height and width in pixels of child image
        rand_pixel_x = random.randint(0, height - 1)  #taking random coordinates
        rand_pixel_y = random.randint(0, width - 1)
        (red, green, blue) = image_pixels[rand_pixel_x, rand_pixel_y] #taking pixel of current child at random coordinates
        rand_red = random.randint(max(0, red - max_disturbance), min(255, red + max_disturbance))      #calculating new color RGB values
        rand_green = random.randint(max(0, green - max_disturbance), min(255, green + max_disturbance))#as explained in
        rand_blue = random.randint(max(0, blue - max_disturbance), min(255, blue + max_disturbance))   #TODO max_disturbance CONSTANT
                                                                                                       #TODO IN main.py
        figure_size = random.randint(self.min_figure_size, self.max_figure_size) #TODO SEE EXPLANATION OF max_figure_size CONSTANT IN
        figure_center_x = random.randint(figure_size, height - figure_size - 1)  #TODO main.py
        figure_center_y = random.randint(figure_size, width - figure_size - 1)
        figure_pixels = Figure(figure_center_x, figure_center_y, figure_size, self.image_size).calculate_pixels()
                                                            #getting array of pixels of figure with the help of 'Figure' class

        for coordinates in figure_pixels:
            image_pixels[coordinates] = (rand_red, rand_green, rand_blue) #painting figure on top of children (mutation)

        to_be_mutated_image.save(path, "png") #saving mutated child to its path

    def evolve(self):                               #function for evolution of current generation population
        best_images = self.find_best()              #first of all, first best parents for the next generation
        children = self.new_population(best_images) #secondly, make children from that parents
        self.mutate_all(children)                   #thirdly, mutate some of them
        self.members = copy.deepcopy(children)      #update old members to the new children
        self.generation += 1                        #increment generation number
