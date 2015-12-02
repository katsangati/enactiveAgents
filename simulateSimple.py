import pygame
import random
from visualizer import canvas
from architecture.existence import Existence
import os
import sys
import argparse

__author__ = 'katja'


def main(saveimg):

    wd = os.getcwd()
    output_path = '{0}/output/'.format(wd)

    if saveimg:
        # empty the output folder
        map(os.unlink, [os.path.join(output_path, f) for f in os.listdir(output_path)])

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((canvas.WIDTH, canvas.HEIGHT))
    done = False

    start_location = (random.randint(canvas.BORDER,canvas.WIDTH-canvas.BORDER),
                      random.randint(canvas.BORDER,canvas.HEIGHT-canvas.BORDER))
    kenny = canvas.Agent(start_location)

    primitive_interactions = {"move forward": ("e1", "r1", 5), "bump": ("e1", "r2", -10),
                              "turn left": ("e2", "r3", -1), "turn right": ("e3", "r4", -1),
                              "touch empty": ("e4", "r5", -1), "touch wall": ("e4", "r6", -2)}
    ex = Existence(primitive_interactions)
    i = 1

    while not done:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        resultstr = None
        anticipations = ex.anticipate()
        experiment = ex.select_experiment(anticipations)
        if experiment.get_label() == 'e1':
            if kenny.move(1):
                resultstr = 'r1'  # moved forward
            else:
                resultstr = 'r2'  # bumped
        elif experiment.get_label() == 'e2':
            kenny.rotate(90)
            resultstr = 'r3'
        elif experiment.get_label() == 'e3':
            kenny.rotate(-90)
            resultstr = 'r4'
        elif experiment.get_label() == 'e4':
            if kenny.feel_front(1):
                resultstr = 'r5'  # clear ahead
            else:
                resultstr = 'r6'  # feel wall

        result = ex.addget_result(resultstr)
        if result is not None:
            enacted_interaction = ex.addget_primitive_interaction(experiment, result)
            print "Enacted " + enacted_interaction.__repr__()

            if enacted_interaction.get_valence() > 0:
                ex.mood = 'HAPPY'
            else:
                ex.mood = 'SAD'

            ex.learn_composite_interaction(ex.context_interaction, enacted_interaction)
            ex.context_interaction = enacted_interaction

            print (i, experiment.get_label(), result.get_label(), str(enacted_interaction.get_valence()))

        pygame.draw.polygon(screen, kenny.color, kenny.vertices)

        if saveimg:
            # save each frame as image
            pygame.image.save(screen, output_path + str(format(i, '03'))+".jpeg")

        pygame.display.flip()
        clock.tick(10)
        i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("mechanism", type=str, help="specify the learning mechanism to be used",
    #                     choices=["sequence_learning", "hierarchical_learning"])
    #parser.add_argument("saveimg", help="when set to 1, simulation is saved as images in output folder", type=int)
    parser.add_argument("-s", "--saveimg", help="when specified, simulation is saved as images in output folder",
                        action="store_true")
    args = parser.parse_args()
    main(args.saveimg)