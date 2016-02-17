import pygame
import random
from visualizer import canvas
from environment import TestEnvironmentD1, TestEnvironmentD2, TestEnvironment, Environment, ConstructiveEnvironment
from architecture.existence import Existence, RecursiveExistence, ConstructiveExistence
import os
import argparse
from imagesaver import ImageSaver

__author__ = 'katja'


def main(mechanism, world, saveimg):
    """
    The main script that runs the simulation.
    :param mechanism: which mechanism will be used to simulate behavior (simple, recursive, constructive)
    :param world: which world will be used for simulation (command-line simple world, real world)
    :param saveimg: will the simulation output be saved
    """

    # initialize existence
    ex = None

    if world == "real":
        # initialize pygame environment
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((canvas.WIDTH, canvas.HEIGHT))
        done = False

        # initialize output path
        wd = os.getcwd()
        output_path = '{0}/output/'.format(wd)
        imgsaver = None
        if saveimg:
            # empty the output folder
            map(os.unlink, [os.path.join(output_path, f) for f in os.listdir(output_path)])
            imgsaver = ImageSaver(output_path)

        # pick random start location
        start_location = (random.randint(canvas.BORDER,canvas.WIDTH-canvas.BORDER),
                          random.randint(canvas.BORDER,canvas.HEIGHT-canvas.BORDER))
        # initialize agent
        kenny = canvas.Agent(start_location)

        # initialize primitive interactions
        primitive_interactions = {"move forward": ("e1", "r1", 2), "bump": ("e1", "r2", -50),
                                  "turn left": ("e2", "r3", -1), "turn right": ("e3", "r4", -1),
                                  "touch empty": ("e4", "r5", -1), "touch wall": ("e4", "r6", -2)}

        # initialize environments and existences
        if mechanism == "simple":
            environment = Environment(kenny, screen, clock)
            ex = Existence(primitive_interactions, environment)
        elif mechanism == "recursive":
            environment = Environment(kenny, screen, clock)
            ex = RecursiveExistence(primitive_interactions, environment)
        elif mechanism == "constructive":
            environment = ConstructiveEnvironment(kenny, screen, clock, imgsaver)
            ex = ConstructiveExistence(primitive_interactions, environment)

        i = 1
        while not done:
            # screen.fill((0, 0, 0))
            # quit if close button is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # perform one simulation step (that might consist of several primitive steps)
            step_trace = ex.step()
            print (i, step_trace)
            print "\n"
            i += 1

            # pygame.draw.polygon(screen, kenny.color, kenny.vertices)
            # if saveimg:
            #     # save each frame as image
            #     pygame.image.save(screen, output_path + str(format(i, '03'))+".jpeg")
            # pygame.display.flip()
            # clock.tick(3)

    elif world == "test":
        primitive_interactions = {"i1": ("e1", "r1", -1), "i2": ("e1", "r2", 1),
                                  "i3": ("e2", "r1", -1), "i4": ("e2", "r2", 1)}
        if mechanism == "simple":
            environment = TestEnvironmentD1()
            ex = Existence(primitive_interactions, environment)
        elif mechanism == "recursive":
            environment = TestEnvironmentD2()
            ex = RecursiveExistence(primitive_interactions, environment)
        elif mechanism == "constructive":
            environment = TestEnvironment()
            ex = ConstructiveExistence(primitive_interactions, environment)

        for i in range(0, 15):
            step_trace = ex.step()
            print (i, step_trace)
            print "\n"


if __name__ == '__main__':
    # run with  python simulate.py constructive real > kennylog.txt
    parser = argparse.ArgumentParser()
    parser.add_argument("mechanism", type=str, help="specify the learning mechanism to be used",
                        choices=["simple", "recursive", "constructive"])
    parser.add_argument("world", type=str, help="specify the world to be used",
                        choices=["test", "real"])
    parser.add_argument("-s", "--saveimg", help="when specified, simulation is saved as images in output folder",
                        action="store_true")
    args = parser.parse_args()
    main(args.mechanism, args.world, args.saveimg)

