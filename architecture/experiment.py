__author__ = 'katja'


class Experiment:
    """ A primitive experiment that can be chosen by the agent """
    def __init__(self, label):
        self.label = label

    def get_label(self):
        return self.label

    def is_abstract(self):
        return False

    def __repr__(self):
        return "{0}".format(self.get_label())


class RecursiveExperiment(Experiment):
    """
    An experiment that can be primitive or abstract.
    An abstract experiment has an intended_interaction, which is a sensorimotor pattern an agent can try to enact.
    It also has a list of enacted_interactions, which are interactions that might be enacted instead of intended ones.
    """
    def __init__(self, label):
        Experiment.__init__(self, label)
        self.is_abstract = False
        self.intended_interaction = None
        self.enacted_interactions = []

    def is_abstract(self):
        return self.is_abstract

    def set_abstract(self):
        self.is_abstract = True

    def set_intended_interaction(self, intended_interaction):
        self.intended_interaction = intended_interaction

    def get_intended_interaction(self):
        return self.intended_interaction

    def add_enacted_interaction(self, enacted_interaction):
        if enacted_interaction not in self.enacted_interactions:
            self.enacted_interactions.append(enacted_interaction)

    def get_enacted_interactions(self):
        return self.enacted_interactions
