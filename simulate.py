import pygame
import random
from visualizer import canvas
from environment import TestEnvironmentD2, TestEnvironmentD3, TestEnvironment, Environment, ConstructiveEnvironment
from architecture.existence import Existence, RecursiveExistence, ConstructiveExistence
import os
import argparse

__author__ = 'katja'


def main(mechanism, world, saveimg):

    wd = os.getcwd()
    output_path = '{0}/output/'.format(wd)

    if saveimg:
        # empty the output folder
        map(os.unlink, [os.path.join(output_path, f) for f in os.listdir(output_path)])

    ex = None

    if world == "real":
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

        # Initialize environments and existences
        if mechanism == "simple":
            environment = Environment(kenny, screen, clock)
            ex = Existence(primitive_interactions, environment)
        elif mechanism == "recursive":
            environment = Environment(kenny, screen, clock)
            ex = RecursiveExistence(primitive_interactions, environment)
        elif mechanism == "constructive":
            environment = ConstructiveEnvironment(kenny, screen, clock)
            ex = ConstructiveExistence(primitive_interactions, environment)

        i = 1

        while not done:
            # screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            step_trace = ex.step()
            print (i, step_trace)
            print "\n"

            # pygame.draw.polygon(screen, kenny.color, kenny.vertices)

            if saveimg:
                # save each frame as image
                pygame.image.save(screen, output_path + str(format(i, '03'))+".jpeg")

            # pygame.display.flip()
            # clock.tick(3)
            i += 1

    elif world == "test":
        primitive_interactions = {"i1": ("e1", "r1", -1), "i2": ("e1", "r2", 1),
                                  "i3": ("e2", "r1", -1), "i4": ("e2", "r2", 1)}
        if mechanism == "simple":
            environment = TestEnvironmentD2()
            ex = Existence(primitive_interactions, environment)
        elif mechanism == "recursive":
            environment = TestEnvironmentD3()
            ex = RecursiveExistence(primitive_interactions, environment)
        elif mechanism == "constructive":
            environment = TestEnvironment()
            ex = ConstructiveExistence(primitive_interactions, environment)

        for i in range(0, 20):
            step_trace = ex.step()
            print (i, step_trace)
            print "\n"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mechanism", type=str, help="specify the learning mechanism to be used",
                        choices=["simple", "recursive", "constructive"])
    parser.add_argument("world", type=str, help="specify the world to be used",
                        choices=["test", "real"])
    parser.add_argument("-s", "--saveimg", help="when specified, simulation is saved as images in output folder",
                        action="store_true")
    args = parser.parse_args()
    main(args.mechanism, args.world, args.saveimg)
