"""
Time Complexity Graphs of Sorting Algorithms

Created 04/08/19
Developed by Fraser Love

This program helps to visualise the time complexities of different sorting algorithms by drawing a graph
to show how the mean time of x sorts by each algorithm relates to the length of the given array.

Usage - If no other arguments are provided the program will run in normal mode and just display the graph. Other modes
such as verbose mode(-v) and output mode(-o) are avaliable aswell. Verbose mode will show the mean value of time taken
after each sort by displaying it in the console. Output mode will output the mean values of time taken for each sorting
algorithm to sort each array to a csv file where the data can be used for further analysis.

Some suggested settings (Leave all else as default)
cutoff = True, max_values[0] = 10000, step = 10
cutoff = False, max_values[0] = 1000, step = 1
"""
import sorting_algorithms, time ,csv, os, sys, math
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Sorting Algorithm Variables
cutoff = False # If true sorting algorithms above graph will no longer be used for sorting
               # This is good for large max values as sorting will only be done by more efficient algorithms
               # Note - this will make the max and min values only based on the current times for algorithms still in use
iterations = 10 # Amount of results incuded in average values
step = 1 # Step between each length of the array
algorithms = [sorting_algorithms.SelectionSort(), sorting_algorithms.BubbleSort(), sorting_algorithms.InsertionSort(), sorting_algorithms.ShellSort(), \
              sorting_algorithms.RadixSort(), sorting_algorithms.CocktailSort(), sorting_algorithms.GnomeSort(), sorting_algorithms.MergeSort(), \
              sorting_algorithms.QuickSort(), sorting_algorithms.HeapSort(), sorting_algorithms.BucketSort()]
off_graph = [False]*11 # Array of booleans to check if algorithms are off the graph

# Graph Variables
window = (1920, 800) # Window size
dimensions = (1800, 800) # Graph size
padding = 80 # Padding of axis from side of window
text_padding = 40 # Padding from axis to text
scale_padding = 10 # Padding from axis to scale
legend_padding = 20 # Padding between legend keys
legend_square_padding = 20 # Padding between the colour square and legend text
legend_square_size = 15 # Size of colour square size
pnt_size = 3 # Size of the point representing each measurement
scale_font_size = (dimensions[0] + dimensions[1]) // 150 # Formula for calculating font size based on window size
legend_font_size = (dimensions[0] + dimensions[1]) // 200 # Formula for calculating font size based on window size
button_size = (70,25) # Size of the start and stop buttons
axis_text = ('Array Length (n)', 'Time (s)')
axis_weight = 1 # The thickness of the axis
max_values = 1000, 0.05 # Max values of each axis in n and s
scale = (max_values[0]/10, max_values[1]/10) #In array length and seconds

#Colours
black = (0,0,0)
white = (255,255,255)
light_grey = (200,200,200)
algorithm_legend = ["#005C09", "#235789", "#C1292E", "#F1D302", "#F56416", "#499F68", "#55DDE0", "#5C1900", "#A83571", "#6900D9", "#29BF12"]

# CSV Variables
header = ["Array Length", "Selection", "Bubble", "Insertion", "Shell", "Radix", "Cocktail", "Gnome", "Merge", "Quick", "Heap", "Bucket"]

def init_pygame():
    pygame.init()
    pygame.font.init()
    display = pygame.display.set_mode((window[0], window[1]))
    pygame.display.set_caption("Sorting Algorithm Time Complexities")
    scale_font = pygame.font.SysFont('Ubuntu', scale_font_size)
    legend_font = pygame.font.SysFont('Ubuntu', legend_font_size)
    display.fill(white)
    return display, scale_font, legend_font

def init_graph(display, scale_font):
    x_text_size = scale_font.size(axis_text[0])
    x_axis_text = scale_font.render(axis_text[0], True, black, white)
    y_text_size = scale_font.size(axis_text[1])
    y_text_size = (y_text_size[1], y_text_size[0])
    y_axis_text = scale_font.render(axis_text[1], True, black, white)
    y_axis_text = pygame.transform.rotate(y_axis_text, 90)
    display.blit(x_axis_text, [(dimensions[0] - x_text_size[0])/2, dimensions[1] - padding + text_padding])
    display.blit(y_axis_text, [padding - text_padding - y_text_size[0], (dimensions[1] - y_text_size[1])/2])
    y_axis = pygame.draw.rect(display, black, (padding,dimensions[1] - padding,axis_weight,-dimensions[1] + padding*2))
    x_axis = pygame.draw.rect(display, black, (padding,dimensions[1] - padding,dimensions[0] - padding*2,axis_weight))
    pygame.display.update()

def gen_scale(display, scale_font):
    for i in range(0,11):
        pygame.draw.rect(display, black, (padding + int(i * (dimensions[0] - padding*2) / 10),dimensions[1] - padding,axis_weight,10))
        pygame.draw.rect(display, light_grey, (padding + int(i * (dimensions[0] - padding*2) / 10),dimensions[1] - padding,axis_weight,-dimensions[1] + padding*2))
        x_scale_num = scale_font.render(str(int(i)*scale[0]), True, black, white)
        x_scale_size = scale_font.size(str(int(i)*scale[0]))
        display.blit(x_scale_num, [padding + int(i * (dimensions[0] - padding*2) / 10) - x_scale_size[0]/2,dimensions[1] - padding + scale_padding])
    for i in range(10,-1,-1):
        pygame.draw.rect(display, black, (padding, padding + int(i * (dimensions[1] - padding*2) / 10),-6,axis_weight))
        pygame.draw.rect(display, light_grey, (padding, padding + int(i * (dimensions[1] - padding*2) / 10),dimensions[0] - padding*2,axis_weight))
        y_scale_num = scale_font.render("{:.3f}".format(int(i)*scale[1]), True, black, white)
        y_scale_size = scale_font.size("{:.3f}".format(int(i)*scale[1]))
        y_scale_size = (y_scale_size[1], y_scale_size[0])
        y_scale_num = pygame.transform.rotate(y_scale_num, 90)
        display.blit(y_scale_num, [padding - scale_padding - y_scale_size[0], dimensions[1] - padding - y_scale_size[1]/2 - int(i * (dimensions[1] - padding*2) / 10)])
    pygame.display.update()

def gen_legend(display, legend_font):
    for i in range(11):
        pygame.draw.rect(display, pygame.Color(algorithm_legend[i]), (dimensions[0] - padding + scale_padding,padding + i*legend_padding,legend_square_size,legend_square_size))
        legend_text = legend_font.render(header[i + 1], True, black, white)
        display.blit(legend_text, [dimensions[0] - padding + scale_padding + legend_square_padding,padding + i*legend_padding - 1])
        pygame.display.update()

def draw_results(display, array_length, value, index):
    if dimensions[1] - padding - int(value/max_values[1]*(dimensions[1]-padding*2)) - math.ceil(pnt_size/2) > padding:
        pygame.draw.rect(display, pygame.Color(algorithm_legend[index]),(padding + int(array_length/max_values[0]*(dimensions[0]-padding*2)) - math.ceil(pnt_size/2), dimensions[1] - padding - int(value/max_values[1]*(dimensions[1]-padding*2)) - math.ceil(pnt_size/2), pnt_size, pnt_size))
    pygame.display.update()

def setup_csv(output):
    if output:
        file = open('times.csv', 'w')
        writer = csv.writer(file)
        writer.writerow(header)
        return file, writer
    else:
        return [], []

def check_modes():
    verbose = False
    output = False
    try:
        for arg in sys.argv:
            if arg == "-v": # Verbose mode
                verbose = True
            if arg == "-o": # Output to CSV
                output = True
    except:
        pass
    return verbose, output

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();

def options(display, paused, scale_font):
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(display, light_grey,(dimensions[0] - padding + scale_padding,padding + 16*legend_padding,button_size[0],button_size[1]))
    start_text = scale_font.render("Start", True, black, light_grey)
    start_size = scale_font.size("Start")
    display.blit(start_text, [dimensions[0] - padding + scale_padding + button_size[0]/2 - int(start_size[0]/2),padding + 16*legend_padding + button_size[1]/2 - int(start_size[1]/2)])
    pygame.draw.rect(display, light_grey,(dimensions[0] - padding + scale_padding,padding + 18*legend_padding,button_size[0],button_size[1]))
    stop_text = scale_font.render("Stop", True, black, light_grey)
    stop_size = scale_font.size("Stop")
    display.blit(stop_text, [dimensions[0] - padding + scale_padding + button_size[0]/2 - int(stop_size[0]/2),padding + 18*legend_padding + button_size[1]/2 - int(stop_size[1]/2)])
    click = pygame.mouse.get_pressed()
    if dimensions[0] - padding + scale_padding+button_size[0] > mouse[0] > dimensions[0] - padding + scale_padding and padding + 16*legend_padding+button_size[1] > mouse[1] > padding + 16*legend_padding:
        if click[0] == 1:
            paused = False
    if dimensions[0] - padding + scale_padding+button_size[0] > mouse[0] > dimensions[0] - padding + scale_padding and padding + 18*legend_padding+button_size[1] > mouse[1] > padding + 18*legend_padding:
        if click[0] == 1:
            paused = True
    pygame.display.update()
    return paused

def show_stats(display, min, max, array_length, legend_font):
    pygame.draw.rect(display, white, (dimensions[0] - padding + scale_padding,padding + 12*legend_padding,200,80))
    min_text = legend_font.render("CurrentMin: {} {:.5f}".format(min[1], min[0]), True, black, white)
    display.blit(min_text, [dimensions[0] - padding + scale_padding,padding + 12*legend_padding])
    max_text = legend_font.render("CurrentMax: {} {:.5f}".format(max[1], max[0]), True, black, white)
    display.blit(max_text, [dimensions[0] - padding + scale_padding,padding + 13*legend_padding])
    length_text = legend_font.render("Array Length: {}".format(array_length), True, black, white)
    display.blit(length_text, [dimensions[0] - padding + scale_padding,padding + 14*legend_padding])
    pygame.display.update()

def pause(display, paused, scale_font):
    while paused:
        check_events()
        paused = options(display, paused, scale_font)

def keep_open():
    while True:
        check_events()

def main_loop(display, verbose, output, scale_font, legend_font, file, writer):
    paused = False
    array_length = 2
    while array_length <= max_values[0]:
        to_write = [str(array_length)]
        max = [0, ""]
        min = [0, ""]
        for algorithm in algorithms:
            if off_graph[algorithms.index(algorithm)] == False:
                sum = 0
                for i in range(iterations):
                    sum += algorithm.run(array_length)[1]
                mean = sum / iterations
                if mean > max_values[1] and cutoff == True:
                    off_graph[algorithms.index(algorithm)] = True
                draw_results(display, array_length, mean, algorithms.index(algorithm))
                if mean < min[0] or min[0] == 0:
                    min[0], min[1] = mean, header[algorithms.index(algorithm)+1]
                if mean > max[0]:
                    max[0], max[1] = mean, header[algorithms.index(algorithm)+1]
                if verbose:
                    print(algorithm.name, mean)
                to_write.append(str(mean))
                paused = options(display, paused, scale_font)
                if paused:
                    pause(display, paused, scale_font)
            else:
                to_write.append("")
        if output:
            writer.writerow(to_write)
        check_events()
        show_stats(display, min, max, array_length, legend_font)
        array_length += step - (array_length % step)
    if output:
        file.close()
    keep_open()

def main():
    verbose, output = check_modes()
    display, scale_font, legend_font = init_pygame()
    init_graph(display, scale_font)
    gen_scale(display, scale_font)
    gen_legend(display, legend_font)
    file, writer = setup_csv(output)
    main_loop(display, verbose, output, scale_font, legend_font, file, writer)

if __name__ == "__main__":
    main()
