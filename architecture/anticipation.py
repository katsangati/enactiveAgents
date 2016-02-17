__author__ = 'katja'


class Anticipation:
    """Anticipation is created from each proposed primitive interaction."""
    def __init__(self, interaction, proclivity):
        self.interaction = interaction
        self.proclivity = proclivity

    def get_interaction(self):
        return self.interaction

    def get_proclivity(self):
        return self.proclivity

    def add_proclivity(self, num):
        self.proclivity += num

    def compare(self):
        """Anticipations are compared by valence they have"""
        return self.interaction.get_valence()

    def __repr__(self):
        return "{0} proclivity {1}".format(self.interaction.get_label(), self.proclivity)


class RecursiveAnticipation(Anticipation):
    """An recursive anticipation is created for each proposed experiment."""

    def __init__(self, experiment, proclivity):
        Anticipation.__init__(self, None, proclivity)
        self.experiment = experiment

    def compare(self):
        """Anticipations are compared by proclivity they have"""
        return self.get_proclivity()

    def set_experiment(self, experiment):
        self.experiment = experiment

    def get_experiment(self):
        return self.experiment

    def __repr__(self):
        return "{0} proclivity {1}".format(self.experiment.get_label(), self.proclivity)

    def __eq__(self, other):
        """Anticipations are equal to each other if they propose the same experiment"""
        return self.get_experiment() == other.get_experiment()


class ConstructiveAnticipation(Anticipation):
    def __init__(self, interaction, proclivity):
        Anticipation.__init__(self, interaction, proclivity)

    def compare(self):
        """Anticipations are compared by proclivity they have"""
        return self.get_proclivity()

    def __eq__(self, other):
        """Anticipations are equal to each other if they propose the same experiment"""
        return self.get_interaction() == other.get_interaction()
