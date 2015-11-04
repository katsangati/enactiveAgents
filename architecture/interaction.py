__author__ = 'katja'


class Interaction:
    def __init__(self, label, valence):
        self.label = label
        self.valence = valence
        self.experiment = None
        self.result = None
        self.weight = 1
        self.pre_interaction = None
        self.post_interaction = None

    def get_label(self):
        return self.label

    def get_experiment(self):
        return self.experiment

    def set_experiment(self, experiment):
        self.experiment = experiment

    def get_result(self):
        return self.result

    def set_result(self, result):
        self.result = result

    def get_valence(self):
        return self.valence

    def set_valence(self, valence):
        self.valence = valence

    def get_pre_interaction(self):
        return self.pre_interaction

    def set_pre_interaction(self, pre_interaction):
        self.pre_interaction = pre_interaction

    def get_post_interaction(self):
        return self.post_interaction

    def set_post_interaction(self, post_interaction):
        self.post_interaction = post_interaction

    def is_primitive(self):
        return self.pre_interaction is None

    def get_weight(self):
        return self.weight

    def increment_weight(self):
        self.weight += 1

    def __repr__(self):
        return "{0}, valence {1}, weight {2}".format(self.get_label(), self.get_valence(), self.get_weight())

