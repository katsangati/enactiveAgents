import pygame


class Environment:
    def __init__(self, agent, screen, clock):
        self.agent = agent
        self.screen = screen
        self.clock = clock
        self.last_result = None

    def draw_agent(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.polygon(self.screen, self.agent.color, self.agent.vertices)
        pygame.display.flip()
        self.clock.tick(4)

    def return_result(self, experiment):
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
    def __init__(self, agent, screen, clock):
        self.agent = agent
        self.screen = screen
        self.clock = clock
        self.enacted_interaction = None

    def enact_primitive_interaction(self, intended_interaction):
        """Returns R2 when curent experience equals previous and differs from penultimate. Returns R1 otherwise"""
        experiment = intended_interaction.get_label()[:2]
        result = None
        if experiment == 'e1':
            if self.agent.move(1):
                result = 'r1'  # moved forward
            else:
                result = 'r2'  # bumped
        elif experiment == 'e2':
            self.agent.rotate(90)
            result = 'r3'
        elif experiment == 'e3':
            self.agent.rotate(-90)
            result = 'r4'
        elif experiment == 'e4':
            if self.agent.feel_front(1):
                result = 'r5'  # clear ahead
            else:
                result = 'r6'  # feel wall

        enacted_interaction = experiment+result
        self.enacted_interaction = enacted_interaction

        return enacted_interaction


class TestEnvironment:
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
        """Returns R2 when curent experience equals previous and differs from penultimate. Returns R1 otherwise"""

        penultimate_interaction = self.get_penultimate_interaction()
        print "penultimate interaction", penultimate_interaction
        previous_interaction = self.get_previous_interaction()
        print "previous interaction", previous_interaction

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


class TestEnvironmentD2:
    """Returns r1 when current experiment is different from previous experiment. Returns r1 otherwise"""
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


class TestEnvironmentD3:
    """Returns R2 when curent experience equals previous and differs from penultimate. Returns R1 otherwise"""
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
