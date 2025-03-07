import os
import typer
import random
from enum import Enum

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from sort import Bubble, Insertion, Selection, Merge, Quick, Heap, Shell, Cocktail, Gnome, Radix, Bitonic

app = typer.Typer()

WIDTH, HEIGHT = 1536, 768

class SortingAlgorithm(str, Enum):
    BUBBLE = 'bubble'
    INSERTION = 'insertion'
    SELECTION = 'selection'
    MERGE = 'merge'
    QUICK = 'quick'
    HEAP = 'heap'
    SHELL = 'shell'
    COCKTAIL = 'cocktail'
    GNOME = 'gnome'
    RADIX = 'radix'
    BITONIC = 'bitonic'


def draw_array(screen, arr, colors):
    screen.fill('black')
    bar_width = WIDTH // len(arr)
    for i, (value, color) in enumerate(zip(arr, colors)):
        pygame.draw.rect(screen, color, (i * bar_width, HEIGHT - value, bar_width, value))
    pygame.display.flip()


def run_sorting(algorithm: str):
    # Calculate number of bars based on width
    num_bars = WIDTH // 3  # Assuming each bar is 5 pixels wide
    
    # Create array with heights from 1 to HEIGHT
    arr = [int(i * (HEIGHT / num_bars)) for i in range(1, num_bars + 1)]
    random.shuffle(arr)
    colors = ['white'] * len(arr)
    
    sorting_algorithms = {
        'bubble': Bubble(delay_ms=0),
        'insertion': Insertion(delay_ms=0),
        'selection': Selection(delay_ms=50),
        'merge': Merge(delay_ms=5),
        'quick': Quick(delay_ms=10),
        'heap': Heap(delay_ms=10),
        'shell': Shell(delay_ms=5),
        'cocktail': Cocktail(delay_ms=0),
        'gnome': Gnome(delay_ms=0),
        'radix': Radix(delay_ms=20),
        'bitonic': Bitonic(delay_ms=5)
    }
    
    sorter = sorting_algorithms.get(algorithm.lower())
    sorting_steps = sorter.sort(arr)
    running = True

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f'{algorithm.capitalize()}')
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        try:
            result = next(sorting_steps)
            if isinstance(result, tuple):
                arr, active_indices = result
                colors = ['white'] * len(arr)
                if len(active_indices) >= 1:
                    colors[active_indices[0]] = 'green'
                if len(active_indices) >= 2:
                    colors[active_indices[1]] = 'red'
            else:
                arr = result
                colors = ['white'] * len(arr)
        except StopIteration:
            # When sorting is complete, show all bars in green
            colors = ['green'] * len(arr)
            draw_array(screen, arr, colors)
            pygame.display.flip()
        
        draw_array(screen, arr, colors)
        # Prevent division by zero by using a small epsilon
        epsilon = 1e-9  # Small value to prevent division by zero
        clock.tick(1 / max(sorter.delay, epsilon))
    
    pygame.quit()


@app.command()
def main(algorithm: SortingAlgorithm = typer.Argument(..., help='Sorting algorithm to visualise.', show_default=False)):
    '''
    Visualise sorting algorithms.
    
    Available algorithms: bubble, insertion, selection, merge, quick, heap, shell, cocktail, gnome, radix, bitonic, bucket
    '''
    run_sorting(algorithm.value)

if __name__ == '__main__':
    app()
