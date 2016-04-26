import pygame


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
                    and (penultimate_interaction is None or "e2" in penultimate_interaction and
                         "e1" in previous_interaction):
                enacted_interaction = "e1r2"
            else:
                enacted_interaction = "e1r1"
        else:
            if previous_interaction is not None \
                    and (penultimate_interaction is None or "e1" in penultimate_interaction and
                         "e2" in previous_interaction):
                enacted_interaction = "e2r2"
            else:
                enacted_interaction = "e2r1"

        self.set_penultimate_interaction(previous_interaction)
        self.set_previous_interaction(enacted_interaction)

        return enacted_interaction


class HomeoEnvironment1:
    """
    Environment that implements a homeostatic principle.
    """
    def __init__(self):
        self.prev_hlevel = -1
        self.hlevel = -1
        self.counter = 0

    def set_hlevel(self, hlevel):
        self.hlevel = hlevel

    def get_hlevel(self):
        return self.hlevel

    def set_prev_hlevel(self, hlevel):
        self.prev_hlevel = hlevel

    def get_prev_hlevel(self):
        return self.prev_hlevel

    def enact_primitive_interaction(self, intended_interaction):
        hlevel = self.get_hlevel()
        prev_hlevel = self.get_prev_hlevel()
        print "H previous: ", str(prev_hlevel)
        print "H current: ", str(hlevel)


        if "e1" in intended_interaction.get_label():
            if hlevel > prev_hlevel:
                enacted_interaction = "e1r1"
            elif hlevel == prev_hlevel:
                enacted_interaction = "e1r2"
            else:
                enacted_interaction = "e1r3"
        else:  # current_experiment == "e2":
            enacted_interaction = "e2r1"
            new_hlevel = 1
            self.set_hlevel(new_hlevel)

        print "setting previous to: ", str(hlevel)
        self.set_prev_hlevel(hlevel)

        self.counter += 1
        if self.counter % 5 == 0:
            self.set_hlevel(-1)

        return enacted_interaction


class HomeoEnvironment2:
    """
    Environment that implements a homeostatic principle.
    """
    def __init__(self):
        self.prev_hlevel = -1
        self.hlevel = -1
        self.counter = 0

    def set_hlevel(self, hlevel):
        self.hlevel = hlevel

    def get_hlevel(self):
        return self.hlevel

    def set_prev_hlevel(self, hlevel):
        self.prev_hlevel = hlevel

    def get_prev_hlevel(self):
        return self.prev_hlevel

    def enact_primitive_interaction(self, intended_interaction):
        hlevel = self.get_hlevel()
        prev_hlevel = self.get_prev_hlevel()
        print "H previous: ", str(prev_hlevel)
        print "H current: ", str(hlevel)

        if "e1" in intended_interaction.get_label():
            if hlevel > prev_hlevel:
                enacted_interaction = "e1r1"
            elif hlevel == prev_hlevel:
                enacted_interaction = "e1r2"
            else:
                enacted_interaction = "e1r3"

        elif "e2" in intended_interaction.get_label():
            enacted_interaction = "e2r1"
            new_hlevel = 1
            self.set_hlevel(new_hlevel)

        else:  # "move"
            if hlevel == 1:
                enacted_interaction = "e3r1"
                new_hlevel = -1
                self.set_hlevel(new_hlevel)
            else:
                enacted_interaction = "e3r2"

        print "setting previous to: ", str(hlevel)
        self.set_prev_hlevel(hlevel)

        self.counter += 1
        # if self.counter % 5 == 0:
        #     self.set_hlevel(-1)

        return enacted_interaction


class HomeoEnvironment3:
    """
    Environment that implements a homeostatic principle.
    """
    def __init__(self):
        self.prev_hlevel = 5
        self.hlevel = 5
        self.hrange = range(11)
        self.counter = 0

    def set_hlevel(self, hlevel):
        self.hlevel = hlevel

    def get_hlevel(self):
        return self.hlevel

    def set_prev_hlevel(self, hlevel):
        self.prev_hlevel = hlevel

    def get_prev_hlevel(self):
        return self.prev_hlevel

    def enact_primitive_interaction(self, intended_interaction):
        hlevel = self.get_hlevel()
        prev_hlevel = self.get_prev_hlevel()
        print "H previous: ", str(prev_hlevel)
        print "H current: ", str(hlevel)

        if "e1" in intended_interaction.get_label():
            if hlevel > prev_hlevel:
                enacted_interaction = "e1r1"
            elif hlevel == prev_hlevel:
                enacted_interaction = "e1r2"
            else:
                enacted_interaction = "e1r3"

        elif "e2" in intended_interaction.get_label():
            enacted_interaction = "e2r1"
            if hlevel < self.hrange[-1]:
                new_hlevel = hlevel + 1
            else:
                new_hlevel = hlevel
            print intended_interaction.get_meaning(), str(new_hlevel)
            self.set_hlevel(new_hlevel)

        else:  # "move"
            if hlevel > self.hrange[0]:
                enacted_interaction = "e3r1"
                new_hlevel = hlevel - 1
            else:
                enacted_interaction = "e3r2"
                new_hlevel = hlevel
            self.set_hlevel(new_hlevel)

        self.counter += 1
        if self.counter % 3 == 0:
            print "decrementing H"
            if hlevel > self.hrange[0]:
                new_hlevel = hlevel - 1
            else:
                new_hlevel = hlevel
            self.set_hlevel(new_hlevel)

        print "setting previous to: ", str(hlevel)
        self.set_prev_hlevel(hlevel)

        return enacted_interaction


class HomeoEnvironment4:
    """
    Environment that implements a homeostatic principle.
    """
    def __init__(self):
        self.prev_hlevel = 5
        self.hlevel = 5
        self.hrange = range(11)
        self.counter = 0

    def set_hlevel(self, hlevel):
        self.hlevel = hlevel

    def get_hlevel(self):
        return self.hlevel

    def set_prev_hlevel(self, hlevel):
        self.prev_hlevel = hlevel

    def get_prev_hlevel(self):
        return self.prev_hlevel

    def enact_primitive_interaction(self, intended_interaction):
        hlevel = self.get_hlevel()
        prev_hlevel = self.get_prev_hlevel()
        print "H previous: ", str(prev_hlevel)
        print "H current: ", str(hlevel)
        valence = 0

        if "e1" in intended_interaction.get_label():
            if hlevel > prev_hlevel:
                enacted_interaction = "e1r1"
            elif hlevel == prev_hlevel:
                enacted_interaction = "e1r2"
            else:
                enacted_interaction = "e1r3"

        elif "e2" in intended_interaction.get_label():
            enacted_interaction = "e2r1"
            if hlevel < self.hrange[-1]:
                new_hlevel = hlevel + 1
            else:
                new_hlevel = hlevel
            valence = (hlevel - 5) * -1
            self.set_hlevel(new_hlevel)

        else:  # "move"
            if hlevel > self.hrange[0]:
                enacted_interaction = "e3r1"
                new_hlevel = hlevel - 1
            else:
                enacted_interaction = "e3r2"
                new_hlevel = hlevel
            self.set_hlevel(new_hlevel)

        self.set_prev_hlevel(hlevel)

        self.counter += 1
        if self.counter % 5 == 0:
            if hlevel > self.hrange[0]:
                new_hlevel = hlevel - 1
            else:
                new_hlevel = hlevel
            self.set_hlevel(new_hlevel)

        return enacted_interaction, valence


class HomeoEnvironment5:
    """
    Environment that implements a homeostatic principle.
    """
    def __init__(self):
        self.prev_hlevel = 5
        self.hlevel = 5
        self.hrange = range(11)
        self.counter = 0

    def set_hlevel(self, hlevel):
        self.hlevel = hlevel

    def get_hlevel(self):
        return self.hlevel

    def set_prev_hlevel(self, hlevel):
        self.prev_hlevel = hlevel

    def get_prev_hlevel(self):
        return self.prev_hlevel

    def enact_primitive_interaction(self, intended_interaction):
        hlevel = self.get_hlevel()
        prev_hlevel = self.get_prev_hlevel()
        print "H previous: ", str(prev_hlevel)
        print "H current: ", str(hlevel)
        valence = 0

        if "e1" in intended_interaction.get_label():
            enacted_interaction = "e1r" + str(hlevel)

        elif "e2" in intended_interaction.get_label():
            enacted_interaction = "e2r1"
            if hlevel < self.hrange[-1]:
                new_hlevel = hlevel + 1
            else:
                new_hlevel = hlevel
            valence = (hlevel - 5) * -1
            self.set_hlevel(new_hlevel)

        else:  # "move"
            if hlevel > self.hrange[0]:
                enacted_interaction = "e3r1"
                new_hlevel = hlevel - 1
            else:
                enacted_interaction = "e3r2"
                new_hlevel = hlevel
            self.set_hlevel(new_hlevel)

        self.set_prev_hlevel(hlevel)

        # self.counter += 1
        # if self.counter % 5 == 0:
        #     if hlevel > self.hrange[0]:
        #         new_hlevel = hlevel - 1
        #     else:
        #         new_hlevel = hlevel
        #     self.set_hlevel(new_hlevel)

        return enacted_interaction, valence
