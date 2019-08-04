"""
Sorting Algorithm Visualiser

Created 01/08/19
Developed by Fraser Love

Visualiser to be used with sorting algorithms provided in sorting_algorithms.py. There 12
algorithms are provided including: selection sort, bubble sort, insertion sort, shell sort
radix sort, cocktail sort, gnome sort, merge sort, quick sort, heap sort, bitonic sort and
bucket sort. One note for the visualisation of merge sort is that because is splits and then
combines the arrays it was difficult to fully visualise. Instead the current arrays being
merged are shown.

Note - This visualiser only for understanding how sorting algorithms work
and should not be used to compare time complexities as most of the time
spent by the program is drawing the array on screen and not on sorting
If you want to see a direct comarison between algorithm in terms of their
scaling and time complexities go download my sorting algorithm comparison program.
"""

import sorting_algorithms, time, os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

dimensions = (1024, 512) # The y value should be equal to the array length
algorithms = {"SelectionSort": sorting_algorithms.SelectionSort(), \
              "BubbleSort": sorting_algorithms.BubbleSort(), \
              "InsertionSort": sorting_algorithms.InsertionSort(), \
              "ShellSort": sorting_algorithms.ShellSort(), \
              "RadixSort": sorting_algorithms.RadixSort(), \
              "CocktailSort": sorting_algorithms.CocktailSort(), \
              "GnomeSort": sorting_algorithms.GnomeSort(), \
              "MergeSort": sorting_algorithms.MergeSort(), \
              "QuickSort": sorting_algorithms.QuickSort(), \
              "HeapSort": sorting_algorithms.HeapSort(), \
              "BitonicSort": sorting_algorithms.BitonicSort(), \
              "BucketSort": sorting_algorithms.BucketSort()}

if len(sys.argv) > 1:
    if sys.argv[1] == "list":
        for key in algorithms.keys(): print(key, end=" ")
        print("")
        sys.exit(0)

# Pygame Initialisation
pygame.init()
display = pygame.display.set_mode((dimensions[0], dimensions[1]))
display.fill(pygame.Color("white"))

# Plays a sound if you are on Ubuntu/Debian
# First install sox with: sudo apt install sox
# Note: This makes the program a lot slower
def play_sound(swap):
    duration = 0.01
    freq = 20
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq+swap*10))

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();

def update(algorithm, swap1=None, swap2=None, display=display):
    display.fill(pygame.Color("white"))
    pygame.display.set_caption("Sorting Visiualiser     Algorithm: {}     Time: {:.3f}      Status: Sorting".format(algorithm.name, time.time() - algorithm.start_time))
    k = int(dimensions[0]/len(algorithm.array))
    for i in range(len(algorithm.array)):
        colour = (0,0,0)
        if swap1 == algorithm.array[i]:
            colour = (0,255,0)
        elif swap2 == algorithm.array[i]:
            colour = (255,0,0)
        pygame.draw.rect(display, colour, (i*k,dimensions[1],k,-algorithm.array[i]))
    #play_sound(swap2) # - Uncomment if you want sound to play with each swap
    check_events()
    pygame.display.update()

def keep_open(algorithm, display, time):
    pygame.display.set_caption("Sorting Visiualiser     Algorithm: {}     Time: {:.3f}      Status: Done".format(algorithm.name, time))
    while True:
        check_events()
        pygame.display.update()

def main():
    if len(sys.argv) < 2:
        print("Error: Enter a sorting algorithm")
    else:
        try:
            algorithm = algorithms[sys.argv[1]]
            try:
                time_elapsed = algorithm.run()[1]
                keep_open(algorithm, display, time_elapsed)
                pass
            except:
                pass
        except:
            print("Error: {} is not a valid sorting algorithm".format(sys.argv[1]))
            print("Note: Sorting algorithms are in Camel Case")

if __name__ == "__main__":
    main()
