import pygame
import random
from visualizer import canvas
from architecture.existence import Existence
__author__ = 'katja'


if __name__ == '__main__':

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((canvas.WIDTH, canvas.HEIGHT))
    done = False

    start_location = (random.randint(canvas.BORDER,canvas.WIDTH-canvas.BORDER),
                      random.randint(canvas.BORDER,canvas.HEIGHT-canvas.BORDER))
    kenny = canvas.Agent(start_location)
    ex = Existence()
    i = 1

    while not done:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        result = None
        anticipations = ex.anticipate()
        experiment = ex.select_experiment(anticipations)
        if experiment.get_label() == 'e1':
            if kenny.move(1):
                result = 'r1'  # moved forward
            else:
                result = 'r2'  # bumped
        elif experiment.get_label() == 'e2':
            kenny.rotate(90)
            result = 'r3'
        elif experiment.get_label() == 'e3':
            kenny.rotate(-90)
            result = 'r4'
        elif experiment.get_label() == 'e4':
            if kenny.feel_front(1):
                result = 'r5'  # clear ahead
            else:
                result = 'r6'  # feel wall

        if result is not None:
            enacted_interaction = ex.get_interaction(experiment.get_label() + result)
            print "Enacted " + enacted_interaction.__repr__()

            if enacted_interaction.get_valence() > 0:
                ex.mood = 'HAPPY'
            else:
                ex.mood = 'SAD'

            ex.learn_composite_interaction(ex.context_interaction, enacted_interaction)
            ex.context_interaction = enacted_interaction

            print (i, experiment.get_label(), result, str(enacted_interaction.get_valence()))

        pygame.draw.polygon(screen, kenny.color, kenny.vertices)
        pygame.display.flip()
        clock.tick(60)
        i += 1


