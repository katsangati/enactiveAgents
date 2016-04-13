from experiment import Experiment
from interaction import Interaction
from anticipation import Anticipation
import random

__author__ = 'katja'


class Existence:
    """A class implementing the agent control-and-learning mechanism.
    The agent operates by executing and learning interactions, and is motivated to perform those interactions that have
    positive valences.
    Interactions can be of two types. Primitive interactions are tuples of (experiment, result, valence). Composite
    interactions are interactions which consist of primitive interactions.
    When a given experiment is performed and a given result is obtained, the corresponding Interaction is considered
    enacted.
    In constructive existence the basic unit of analysis and implementation is interaction, not experiments and results.
    """

    EXPERIMENTS = dict()
    INTERACTIONS = dict()

    def __init__(self, primitive_interactions, environment):
        """
        Initialize existence with a set of primitive interactions and environment.
        :param primitive_interactions: (dict) of primitive interactions of the form
        {(str) interaction meaning: ((str) experiment, (str) result, (int) valence)}
        :param environment: (Environment) that controls which results are returned for a given primitive experiment
        :return: (Existence)
        """
        self.context_interaction = None
        self.context_pair_interaction = None  # context at previous two steps (t-2, t-1)
        self.mood = None
        self.environment = environment
        self.initialize_interactions(primitive_interactions)

    def step(self):
        print "Memory: ", self.INTERACTIONS.keys()
        anticipations = self.anticipate()
        for anticipation in anticipations:
            print "Anticipated: ", anticipation
        intended_interaction = self.select_interaction(anticipations)
        print "Intended interaction: ", intended_interaction
        enacted_interaction = self.enact(intended_interaction)
        print "Enacted interaction: ", enacted_interaction

        # if intended interaction failed, record the alternative
        if enacted_interaction != intended_interaction:
            intended_interaction.add_alternative_interaction(enacted_interaction)
            print "Alternative interactions:", intended_interaction.get_alternative_interactions()

        if enacted_interaction.get_valence() > 0:
            self.mood = 'HAPPY'
        else:
            self.mood = 'SAD'

        self.learn_recursive_interaction(enacted_interaction)

        return enacted_interaction.__repr__() + " " + self.mood

    def initialize_interactions(self, primitive_interactions):
        for key in primitive_interactions:
            meaning = key
            experiment_label = primitive_interactions[key][0]
            result_label = primitive_interactions[key][1]
            interaction_label = experiment_label + result_label
            valence = primitive_interactions[key][2]
            primitive_interaction = self.addget_interaction(interaction_label)
            primitive_interaction.set_valence(valence)
            primitive_interaction.set_meaning(meaning)
            # creating default experiments to begin with
            self.addget_abstract_experiment(primitive_interaction)

    def addget_abstract_experiment(self, interaction):
        """
        All experiments are now abstract, namely they are interactions.
        """
        label = interaction.get_label().upper()
        if label not in self.EXPERIMENTS:
            abstract_experiment = Experiment(label)
            abstract_experiment.set_intended_interaction(interaction)
            abstract_experiment.set_abstract()
            interaction.set_experiment(abstract_experiment)
            self.EXPERIMENTS[label] = abstract_experiment
        return self.EXPERIMENTS[label]

    # Learning:
    def learn_recursive_interaction(self, enacted_interaction):
        enacted_pair_interaction = None
        if self.context_interaction is not None:
            # if hist[-1]: learn(hist[-1], enacted)
            enacted_pair_interaction = self.addreinforce_composite_interaction(self.context_interaction,
                                                                               enacted_interaction)

            if self.context_pair_interaction is not None:
                # if hist[-1] and hist[-2]
                # learn <penultimate <previous current>>
                self.addreinforce_composite_interaction(self.context_pair_interaction.get_pre_interaction(),
                                                        enacted_pair_interaction)
                # learn <<penultimate previous> current>
                self.addreinforce_composite_interaction(self.context_pair_interaction, enacted_interaction)

        self.set_context_interaction(enacted_interaction)
        self.set_context_pair_interaction(enacted_pair_interaction)

    def get_context_interaction(self):
        return self.context_interaction

    def set_context_interaction(self, enacted_interaction):
        self.context_interaction = enacted_interaction

    def get_context_pair_interaction(self):
        return self.context_pair_interaction

    def set_context_pair_interaction(self, enacted_pair_interaction):
        self.context_pair_interaction = enacted_pair_interaction

    def addreinforce_composite_interaction(self, pre_interaction, post_interaction):
        composite_interaction = self.addget_composite_interaction(pre_interaction, post_interaction)
        composite_interaction.increment_weight()

        if composite_interaction.get_weight() == 1:
            print "Learned: ", composite_interaction
        else:
            print "Reinforced: ", composite_interaction

        return composite_interaction

    def addget_composite_interaction(self, pre_interaction, post_interaction):
        """Record in or get from a composite interaction in memory.
        If a new composite interaction is created, then a new abstract experience is also created and associated to it.
        """
        label = "<" + pre_interaction.get_label() + post_interaction.get_label() + ">"
        interaction = self.get_interaction(label)
        if interaction is None:
            interaction = self.addget_interaction(label)
            interaction.set_pre_interaction(pre_interaction)
            interaction.set_post_interaction(post_interaction)
            valence = pre_interaction.get_valence() + post_interaction.get_valence()
            interaction.set_valence(valence)
            meaning = "<" + pre_interaction.get_meaning() + "," + post_interaction.get_meaning() + ">"
            interaction.set_meaning(meaning)
            self.addget_abstract_experiment(interaction)
        return interaction

    def anticipate(self):
        anticipations = self.get_default_anticipations()
        print "Default anticipations: ", anticipations
        activated_interactions = self.get_activated_interactions()
        # print "Activated interactions: ", activated_interactions
        if self.context_interaction is not None:
            for activated_interaction in activated_interactions:
                proposed_interaction = activated_interaction.get_post_interaction()
                # print "activated experiment: " + experiment.get_label()
                proclivity = activated_interaction.get_weight() * proposed_interaction.get_valence()
                anticipation = Anticipation(proposed_interaction, proclivity)
                # print "activated anticipation: " + anticipation.__repr__()
                if anticipation not in anticipations:
                    anticipations.append(anticipation)
                else:
                    index = anticipations.index(anticipation)
                    # increment proclivity if anticipation is already in the list
                    anticipations[index].add_proclivity(proclivity)
                # print "Afforded " + anticipation.__repr__()

            for anticipation in anticipations:
                index = anticipations.index(anticipation)
                alternative_interactions = anticipation.get_interaction().get_alternative_interactions()
                for interaction in alternative_interactions:
                    for activated_interaction in activated_interactions:
                        # combine proclivity with alternative interactions
                        if interaction == activated_interaction.get_post_interaction():
                            proclivity = activated_interaction.get_weight() * interaction.get_valence()
                            anticipations[index].add_proclivity(proclivity)
        return anticipations

    def get_activated_interactions(self):
        context_interactions = []
        if self.context_interaction is not None:
            context_interactions.append(self.context_interaction)
            if not self.context_interaction.is_primitive():
                context_interactions.append(self.context_interaction.get_post_interaction())
            if self.context_pair_interaction is not None:
                context_interactions.append(self.context_pair_interaction)
        print "Context: ", context_interactions
        activated_interactions = []
        for key in self.INTERACTIONS:
            activated_interaction = self.INTERACTIONS[key]
            if not activated_interaction.is_primitive():
                if activated_interaction.get_pre_interaction() in context_interactions:
                    activated_interactions.append(activated_interaction)
        for activated_interaction in activated_interactions:
            print "Activated: ", activated_interaction
        return activated_interactions

    def get_default_anticipations(self):
        anticipations = []
        for interaction in self.INTERACTIONS.values():
            if interaction.is_primitive():
                # print "interaction is primitive"
                anticipation = Anticipation(interaction, 0)
                # print "adding anticipation", anticipation
                anticipations.append(anticipation)
        # # sort default anticipations by valence
        # anticipations.sort(key=lambda x: x.get_interaction().get_valence(), reverse=True)
        # shuffle default anticipations
        random.shuffle(anticipations)
        return anticipations

    def enact(self, intended_interaction):
        # if interaction is primivite, consult the world and get what was actually enacted
        if intended_interaction.is_primitive():
            enacted_interaction_label = self.environment.enact_primitive_interaction(intended_interaction)
            enacted_interaction = self.addget_interaction(enacted_interaction_label)
            return enacted_interaction
        else:
            # if interaction is composite, try to enact its pre-interaction
            enacted_pre_interaction = self.enact(intended_interaction.get_pre_interaction())
            # if enacting failed, break the sequence and return
            if enacted_pre_interaction != intended_interaction.get_pre_interaction():
                return enacted_pre_interaction
            else:
                # if enacting pre-interaction succeeded, try to enact post-interaction
                enacted_post_interaction = self.enact(intended_interaction.get_post_interaction())
                return self.addget_composite_interaction(enacted_pre_interaction, enacted_post_interaction)

    @staticmethod
    def select_interaction(anticipations):
        anticipations.sort(key=lambda x: x.compare(), reverse=True)  # choose by proclivity
        selected_anticipation = anticipations[0]
        intended_interaction = selected_anticipation.get_interaction()
        # if intended_interaction.get_valence() < 0:
        #     intended_interaction = self.get_random_interaction(intended_interaction)
        #     print "Don't like the affordance, intending random interaction..."
        return intended_interaction

    def get_random_interaction(self, interaction):
        random_interaction = random.choice(self.INTERACTIONS.values())
        if interaction is None:
            return random_interaction
        else:
            bad_experiment = interaction.get_experiment()
            chosen_experiment = random_interaction.get_experiment()
            while chosen_experiment == bad_experiment:
                random_interaction = random.choice(self.INTERACTIONS.values())
            return random_interaction

    def addget_interaction(self, label):
        if label not in self.INTERACTIONS:
            self.INTERACTIONS[label] = Interaction(label)
        return self.INTERACTIONS[label]

    def get_interaction(self, label):
        if label in self.INTERACTIONS:
            return self.INTERACTIONS[label]
        else:
            return None
