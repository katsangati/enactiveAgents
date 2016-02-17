import pygame


class Environment:
    """
    Class that implements the basic real-world environment.
    """
    def __init__(self, agent, screen, clock):
        self.agent = agent
        self.screen = screen
        self.clock = clock
        self.last_result = None

    def draw_agent(self):
        """
        Draw the screen and the agent in it and display.
        """
        self.screen.fill((0, 0, 0))
        pygame.draw.polygon(self.screen, self.agent.color, self.agent.vertices)
        pygame.display.flip()
        self.clock.tick(4)

    def return_result(self, experiment):
        """
        Consult the world and return primitive result in response to the experiment initiated by the agent.
        :param experiment: (Experiment) experiment issued by the agent
        :return: (str) result
        """
        result = None
        if experiment.get_label() == 'e1':
            if self.agent.move(1):
                result = 'r1'  # moved forward
                self.draw_agent()
            else:
                result = 'r2'  # bumped
                self.draw_agent()
        elif experiment.get_label() == 'e2':
            self.agent.rotate(90)
            result = 'r3'
            self.draw_agent()
        elif experiment.get_label() == 'e3':
            self.agent.rotate(-90)
            result = 'r4'
            self.draw_agent()
        elif experiment.get_label() == 'e4':
            if self.agent.feel_front(1):
                result = 'r5'  # clear ahead
                self.draw_agent()
            else:
                result = 'r6'  # feel wall
                self.draw_agent()

        self.last_result = result
        return result


class ConstructiveEnvironment:
    """
    Class that implements constructive environment, in which interactions are the basic primitives.
    """
    # TIMESTEP = 1
    def __init__(self, agent, screen, clock, imgsaver):
        self.agent = agent
        self.screen = screen
        self.clock = clock
        self.last_interaction = None
        self.imgsaver = imgsaver

    def draw_agent(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.polygon(self.screen, self.agent.color, self.agent.vertices)
        pygame.display.flip()
        self.clock.tick(10)
        if self.imgsaver:
            self.imgsaver.save_next_img(self.screen)
        # pygame.image.save(self.screen, output_path + str(format(self.TIMESTEP, '03'))+".jpeg")
        # self.TIMESTEP += 1

    def enact_primitive_interaction(self, intended_interaction):
        """
        Consult the world and return enacted interaction in response to the agent's intended interaction.
        :param intended_interaction: (Interaction) interaction attempted by the agent
        :return: (Interaction) interaction actually enacted
        """
        experiment = intended_interaction.get_label()[:2]
        result = None
        if experiment == 'e1':
            if self.agent.move(1):
                result = 'r1'  # moved forward
                self.draw_agent()
            else:
                result = 'r2'  # bumped
                self.draw_agent()
        elif experiment == 'e2':
            self.agent.rotate(90)
            result = 'r3'
            self.draw_agent()
        elif experiment == 'e3':
            self.agent.rotate(-90)
            result = 'r4'
            self.draw_agent()
        elif experiment == 'e4':
            if self.agent.feel_front(1):
                result = 'r5'  # clear ahead
                self.draw_agent()
            else:
                result = 'r6'  # feel wall
                self.draw_agent()

        enacted_interaction = experiment+result
        self.last_interaction = enacted_interaction

        return enacted_interaction


class TestEnvironmentD1:
    """
    Command-line environment of depth 1.
    Returns r2 when current experiment is different from previous experiment. Returns r1 otherwise.
    """
    def __init__(self):
        self.previous_experiment = None

    def set_previous_experiment(self, previous_experiment):
        self.previous_experiment = previous_experiment

    def get_previous_experiment(self):
        return self.previous_experiment

    def return_result(self, experiment):
        previous_experiment = self.get_previous_experiment()
        current_experiment = experiment.get_label()

        if experiment == previous_experiment:
            result = "r1"
        else:
            result = "r2"

        self.set_previous_experiment(experiment)

        return result


class TestEnvironmentD2:
    """Command-line environment of depth 2.
    Returns r2 when current experience equals previous and differs from penultimate. Returns r1 otherwise.
    """
    def __init__(self):
        self.penultimate_experiment = None
        self.previous_experiment = None

    def set_penultimate_experiment(self, penultimate_experiment):
        self.penultimate_experiment = penultimate_experiment

    def get_penultimate_experiment(self):
        return self.penultimate_experiment

    def set_previous_experiment(self, previous_experiment):
        self.previous_experiment = previous_experiment

    def get_previous_experiment(self):
        return self.previous_experiment

    def return_result(self, experiment):
        penultimate_experiment = self.get_penultimate_experiment()
        previous_experiment = self.get_previous_experiment()
        current_experiment = experiment.get_label()

        if experiment == previous_experiment and experiment != penultimate_experiment:
            result = "r2"
        else:
            result = "r1"

        self.set_penultimate_experiment(previous_experiment)
        self.set_previous_experiment(experiment)

        return result


class TestEnvironment:
    """
    Command-line environment of depth 2, which implements constructive principle.
    Returns r2 when current experience equals previous and differs from penultimate.
    Returns R1 otherwise.
    """
    def __init__(self):
        self.penultimate_interaction = None
        self.previous_interaction = None

    def set_penultimate_interaction(self, penultimate_interaction):
        self.penultimate_interaction = penultimate_interaction

    def get_penultimate_interaction(self):
        return self.penultimate_interaction

    def set_previous_interaction(self, previous_interaction):
        self.previous_interaction = previous_interaction

    def get_previous_interaction(self):
        return self.previous_interaction

    def enact_primitive_interaction(self, intended_interaction):
        penultimate_interaction = self.get_penultimate_interaction()
        # print "penultimate interaction", penultimate_interaction
        previous_interaction = self.get_previous_interaction()
        # print "previous interaction", previous_interaction

        if "e1" in intended_interaction.get_label():
            if previous_interaction is not None \
                    and (penultimate_interaction is None or "e2" in penultimate_interaction and "e1" in previous_interaction):
                enacted_interaction = "e1r2"
            else:
                enacted_interaction = "e1r1"
        else:
            if previous_interaction is not None \
                    and (penultimate_interaction is None or "e1" in penultimate_interaction and "e2" in previous_interaction):
                enacted_interaction = "e2r2"
            else:
                enacted_interaction = "e2r1"

        self.set_penultimate_interaction(previous_interaction)
        self.set_previous_interaction(enacted_interaction)

        return enacted_interaction
