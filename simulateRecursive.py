import pygame
import random
from visualizer import canvas
from architecture.existence import Existence, RecursiveExistence
from environment import Environment
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
    # ex = Existence(primitive_interactions)
    environment = Environment(kenny)
    ex = RecursiveExistence(primitive_interactions, environment)
    i = 1

    while not done:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        anticipations = ex.anticipate()
        experiment = ex.select_experiment(anticipations)

        intended_interaction = experiment.get_intended_interaction()
        intended_interaction.set_experiment(experiment)
        enacted_interaction = ex.enact(intended_interaction)

        if enacted_interaction != intended_interaction and experiment.is_abstract:
            failed_result = ex.addget_result(enacted_interaction.get_label().upper())
            valence = enacted_interaction.get_valence()
            enacted_interaction = ex.addget_primitive_interaction(experiment, failed_result, valence)

        if enacted_interaction.get_valence() >= 0:
            ex.mood = 'HAPPY'
        else:
            ex.mood = 'SAD'

        # learn context_pair_interaction, context_interaction, enacted_interaction
        ex.learn_recursive_interaction(enacted_interaction)

        print (i, experiment.get_label(), environment.last_result, str(enacted_interaction.get_valence()))

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
