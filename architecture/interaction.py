__author__ = 'katja'


class Interaction:
    """
    An interaction is a basic sensorimotor pattern available to the agent.
    An interaction can be primitive or composite. If primitive, it is an association of experiment and result.
    If composite, it has pre- and post-interaction parts.
    Each interaction has valence and weight.
    """
    def __init__(self, label):
        self.label = label
        self.valence = 0
        self.experiment = None
        self.result = None
        self.meaning = None
        self.weight = 0
        self.pre_interaction = None
        self.post_interaction = None
        self.alternative_interactions = []

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
        if self.is_primitive():
            return self.valence
        else:
            pre = self.get_pre_interaction()
            post = self.get_post_interaction()
            return pre.get_valence() + post.get_valence()

    def set_valence(self, valence):
        self.valence = valence

    def get_meaning(self):
        return self.meaning

    def set_meaning(self, meaning):
        self.meaning = meaning

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

    def add_alternative_interaction(self, interaction):
        if interaction not in self.alternative_interactions:
            self.alternative_interactions.append(interaction)

    def get_alternative_interactions(self):
        return self.alternative_interactions

    def __repr__(self):
        return "{0}, valence {1}, weight {2}".format(self.get_label(), self.get_valence(), self.get_weight())
