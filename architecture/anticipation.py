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
        """Anticipations are compared by proclivity they have"""
        return self.get_proclivity()

    def __eq__(self, other):
        """Anticipations are equal to each other if they propose the same experiment"""
        return self.get_interaction() == other.get_interaction()

    def __repr__(self):
        return "{0} proclivity {1}".format(self.interaction.get_label(), self.proclivity)
