import random
from visualizer import canvas
from environment import *
from architecture.existence import Existence, HomeoExistence
import os
import argparse
from imagesaver import ImageSaver

__author__ = 'katja'


def main(world, mechanism, saveimg):
    """
    The main script that runs the simulation.
    :param world: which world will be used for simulation (command-line test world, real world)
    :param saveimg: will the simulation output be saved
    """

    # initialize existence
    # random.seed(1234)

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
        start_location = (random.randint(canvas.BORDER, canvas.WIDTH-canvas.BORDER),
                          random.randint(canvas.BORDER, canvas.HEIGHT-canvas.BORDER))
        # initialize agent
        kenny = canvas.Agent(start_location)

        # initialize primitive interactions
        primitive_interactions = {"move forward": ("e1", "r1", 2), "bump": ("e1", "r2", -50),
                                  "turn left": ("e2", "r3", -1), "turn right": ("e3", "r4", -1),
                                  "touch empty": ("e4", "r5", 0), "touch wall": ("e4", "r6", -1)}

        # initialize environments and existences
        environment = ConstructiveEnvironment(kenny, screen, clock, imgsaver)
        ex = Existence(primitive_interactions, environment)

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

    elif world == "test":

        if mechanism == "nonh":
            primitive_interactions = {"i1": ("e1", "r1", -1), "i2": ("e1", "r2", 1),
                                  "i3": ("e2", "r1", -1), "i4": ("e2", "r2", 1)}
            environment = TestEnvironment()
            ex = Existence(primitive_interactions, environment)

        elif mechanism == "h1":
            # suppose H is a homeostatic value
            # e1r1 - check H positive, e1r2 - check H negative
            # e2r1 - eat successfully, e2r2 - fail at eating
            primitive_interactions = {"H_up": ("e1", "r1", 1), "H_same": ("e1", "r2", 0),
                                     "H_lower": ("e1", "r3", -1), "eat": ("e2", "r1", 0)}
            environment = HomeoEnvironment1()
            ex = Existence(primitive_interactions, environment)

        elif mechanism == "h2":
            primitive_interactions = {"H_up": ("e1", "r1", 1), "H_same": ("e1", "r2", 0),
                                      "H_lower": ("e1", "r3", -1), "eat": ("e2", "r1", 0),
                                      "move_fwd": ("e3", "r1", 1), "nmove_fwd": ("e3", "r2", -1)}
            environment = HomeoEnvironment2()
            ex = Existence(primitive_interactions, environment)

        elif mechanism == "h3":
            primitive_interactions = {"H_up": ("e1", "r1", 1), "H_same": ("e1", "r2", 0),
                                      "H_lower": ("e1", "r3", -1), "eat": ("e2", "r1", 0),
                                      "move_fwd": ("e3", "r1", 1), "nmove_fwd": ("e3", "r2", -1)}
            environment = HomeoEnvironment3()
            ex = Existence(primitive_interactions, environment)

        elif mechanism == "h4":
            primitive_interactions = {"H_up": ("e1", "r1", 0), "H_same": ("e1", "r2", 0),
                                      "H_lower": ("e1", "r3", 0), "eat": ("e2", "r1", 0),
                                      "move_fwd": ("e3", "r1", 0), "nmove_fwd": ("e3", "r2", 0)}

            environment = HomeoEnvironment4()
            ex = HomeoExistence(primitive_interactions, environment)

        else:
            primitive_interactions = {"eat": ("e2", "r1", 0), "move_fwd": ("e3", "r1", 0), "nmove_fwd": ("e3", "r2", 0)}
            for i in range(11):
                primitive_interactions["H"+str(i)] = ("e1", "r"+str(i), 0)

            environment = HomeoEnvironment5()
            ex = HomeoExistence(primitive_interactions, environment)

        print "Primitive interactions: ", primitive_interactions
        print "Mechanism: ", mechanism
        print "\n"

        for i in range(0, 500):
            step_trace = ex.step()
            print (i, step_trace)
            print "\n"
        print "Last memory state: "
        for k in ex.INTERACTIONS.keys():
            print ex.INTERACTIONS[k]


if __name__ == '__main__':
    # run with  python simulate.py real > kennylog.txt
    parser = argparse.ArgumentParser()
    parser.add_argument("world", type=str, help="specify the world to be used",
                        choices=["test", "real"])
    parser.add_argument("mechanism", type=str, help="specify the homeostatic mechanism to be used",
                        choices=["nonh", "h1", "h2", "h3", "h4", "h5"])
    parser.add_argument("-s", "--saveimg", help="when specified, simulation is saved as images in output folder",
                        action="store_true")
    args = parser.parse_args()
    main(args.world, args.mechanism, args.saveimg)
