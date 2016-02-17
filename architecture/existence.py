from interaction import Interaction
from experiment import Experiment, RecursiveExperiment
from result import Result
from anticipation import Anticipation, RecursiveAnticipation, ConstructiveAnticipation
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
    """

    EXPERIMENTS = dict()
    INTERACTIONS = dict()
    RESULTS = dict()

    def __init__(self, primitive_interactions, environment):
        """
        Initialize existence with a set of primitive interactions and environment.
        :param primitive_interactions: (dict) of primitive interactions of the form
        {(str) interaction meaning: ((str) experiment, (str) result, (int) valence)}
        :param environment: (Environment) that controls which results are returned for a given primitive experiment
        :return: (Existence)
        """
        self.context_interaction = None
        self.mood = None
        self.environment = environment
        self.initialize_interactions(primitive_interactions)

    def step(self):
        """
        Execute a single simulation step.
        :return: (str) performed interaction and mood
        """
        print "Context: ", self.context_interaction
        anticipations = self.anticipate()  # anticipate possible interactions
        experiment = self.select_experiment(anticipations)  # select the best experiment
        result_label = self.environment.return_result(experiment)  # consult the world and return result
        result = self.addget_result(result_label)  # add result to the dictionary
        enacted_interaction = self.get_interaction(experiment.get_label() + result.get_label())
        print "Enacted ", enacted_interaction

        if enacted_interaction.get_valence() > 0:
            self.mood = 'HAPPY'
        else:
            self.mood = 'SAD'

        self.learn_composite_interaction(self.context_interaction, enacted_interaction)
        self.context_interaction = enacted_interaction

        return experiment.get_label() + result.get_label() + " " + self.mood

    def initialize_interactions(self, primitive_interactions):
        """
        Add primitive interactions to existence
        :param primitive_interactions: a set of primitive interactions provided as a dictionary
        {(str) interaction meaning: ((str) experiment, (str) result, (int) valence)}
        """
        for interaction in primitive_interactions:
            meaning = interaction
            experiment_label = primitive_interactions[interaction][0]
            result_label = primitive_interactions[interaction][1]
            valence = primitive_interactions[interaction][2]
            result = self.addget_result(result_label)
            experiment = self.addget_experiment(experiment_label)
            self.addget_primitive_interaction(experiment, result, valence, meaning)

    def addget_primitive_interaction(self, experiment, result, valence=None, meaning=None):
        """
        If a primitive interaction is not in the INTERACTIONS dictionary, add it. Otherwise just return it.
        :param experiment: (str) primitive experiment
        :param result: (str) primitive result
        :param valence: (int) valence of the interaction
        :param meaning: (str) observer's meaning of the interaction
        :return: (interaction) primitive interaction from the INTERACTIONS dictionary
        """
        label = experiment.get_label() + result.get_label()
        if label not in self.INTERACTIONS:
            interaction = Interaction(label)
            interaction.set_experiment(experiment)
            interaction.set_result(result)
            interaction.set_valence(valence)
            interaction.set_meaning(meaning)
            self.INTERACTIONS[label] = interaction
        return self.INTERACTIONS[label]

    def learn_composite_interaction(self, context_interaction, enacted_interaction):
        """
        Learn a new composite interaction or reinforce it if already known.
        :param context_interaction: (Interaction) at time t-1
        :param enacted_interaction: (Interaction) just performed
        """
        if context_interaction is not None:
            label = context_interaction.get_label() + enacted_interaction.get_label()
            if label not in self.INTERACTIONS:
                # valence is a sum of primitive interactions
                valence = context_interaction.get_valence() + enacted_interaction.get_valence()
                interaction = Interaction(label)
                interaction.set_pre_interaction(context_interaction)
                interaction.set_post_interaction(enacted_interaction)
                interaction.set_valence(valence)
                self.INTERACTIONS[label] = interaction
                print "Learn " + label
            else:
                interaction = self.INTERACTIONS[label]
                print 'Incrementing weight for ', interaction
                interaction.increment_weight()

    def anticipate(self):
        """
        Anticipate possible interactions based on current context.
        :return: (list) of Anticipations
        """
        anticipations = []
        if self.context_interaction is not None:
            activated_interactions = self.get_activated_interactions()
            for activated_interaction in activated_interactions:
                # retrieve proposed interactions
                proposed_interaction = activated_interaction.get_post_interaction()
                # proclivity is a product of the weight of the whole interaction and a valence of proposed
                proclivity = activated_interaction.get_weight() * proposed_interaction.get_valence()
                anticipations.append(Anticipation(proposed_interaction, proclivity))
                print "Afforded: ", proposed_interaction, " proclivity: " + str(proclivity)
        return anticipations

    def get_activated_interactions(self):
        """
        Retrieve activated interactions based on current context.
        :return: (list) of Interactions
        """
        activated_interactions = []
        # loop through all known interactions
        for key in self.INTERACTIONS:
            activated_interaction = self.INTERACTIONS[key]
            # see if known interaction's pre-interactions is the same as interaction performed at t-1
            if activated_interaction.get_pre_interaction() == self.context_interaction:
                activated_interactions.append(activated_interaction)
        return activated_interactions

    def select_experiment(self, anticipations):
        """Select experiment from proposed anticipations"""
        if len(anticipations) > 0:
            #anticipations.sort(key=lambda x: x.compare(), reverse=True)  # choose by proclivity
            anticipations.sort(key=lambda x: x.compare(), reverse=True)  # choose by valence
            afforded_interaction = anticipations[0].get_interaction()
            if afforded_interaction.get_valence() >= 0:
                intended_interaction = afforded_interaction
                print "Intending ", intended_interaction
                chosen_experiment = intended_interaction.get_experiment()
            else:
                # if proposed interaction leads to negative valence, choose at random
                chosen_experiment = self.get_random_experiment(afforded_interaction)
                print "Don't like the affordance, intending experiment " + chosen_experiment.get_label()
        else:
            # if nothing was anticipated, choose at random
            chosen_experiment = self.get_random_experiment(None)
            print "Don't know what to do, intending experiment " + chosen_experiment.get_label()
        return chosen_experiment

    def get_random_experiment(self, interaction):
        random_experiment = random.choice(self.EXPERIMENTS.values())
        if interaction is None:
            return random_experiment
        else:
            # trying to choose a random experiment but avoid choosing one that was part of the rejected interaction
            bad_experiment = interaction.get_experiment()
            chosen_experiment = random.choice(self.EXPERIMENTS.values())
            while chosen_experiment == bad_experiment:
                chosen_experiment = random.choice(self.EXPERIMENTS.values())
            return random_experiment

    def addget_result(self, label):
        if label not in self.RESULTS:
            self.RESULTS[label] = Result(label)
        return self.RESULTS[label]

    def addget_experiment(self, label):
        if label not in self.EXPERIMENTS:
            self.EXPERIMENTS[label] = Experiment(label)
        return self.EXPERIMENTS[label]

    def addget_interaction(self, label):
        if label not in self.INTERACTIONS:
            self.INTERACTIONS[label] = Interaction(label)
        return self.INTERACTIONS[label]

    def get_interaction(self, label):
        if label in self.INTERACTIONS:
            return self.INTERACTIONS[label]
        else:
            return None


class RecursiveExistence(Existence):
    """Implements recursive self-programming.
    Context is now of depth 2: prev_context_interaction at t-2, and context_interaction at t-1"""

    def __init__(self, primitive_interactions, environment):
        """Initialize existence with a set of primitive interactions provided as a dictionary:
        {(str) interaction meaning: ((str) experiment, (str) result, (int) valence)"""
        Existence.__init__(self, primitive_interactions, environment)
        self.context_pair_interaction = None  # context at previous two steps (t-2, t-1)

    def step(self):
        print "Memory: ", self.INTERACTIONS.keys()
        anticipations = self.anticipate()
        for anticipation in anticipations:
            print "Anticipated: ", anticipation
        experiment = self.select_experiment(anticipations)  # recursive experiment
        print "Selected experiment: " + experiment.get_label()
        intended_interaction = experiment.get_intended_interaction()
        print "Intending: ", intended_interaction
        print "Intending experiment: ", intended_interaction.get_experiment().get_label()
        enacted_interaction = self.enact(intended_interaction)

        print "Enacted ", enacted_interaction
        if enacted_interaction != intended_interaction and experiment.is_abstract:
            failed_result = self.addget_result(enacted_interaction.get_label().upper())
            print "failed result: ", failed_result.get_label()
            valence = enacted_interaction.get_valence()
            print "experiment: ", str(experiment)
            enacted_interaction = self.addget_primitive_interaction(experiment, failed_result, valence)
            print "Really enacted ", enacted_interaction

        if enacted_interaction.get_valence() >= 0:
            self.mood = 'HAPPY'
        else:
            self.mood = 'SAD'

        # learn context_pair_interaction, context_interaction, enacted_interaction
        self.learn_recursive_interaction(enacted_interaction)
        return enacted_interaction.__repr__() + " " + self.mood

    def initialize_interactions(self, primitive_interactions):
        for interaction in primitive_interactions:
            meaning = interaction
            experiment_label = primitive_interactions[interaction][0]
            result_label = primitive_interactions[interaction][1]
            valence = primitive_interactions[interaction][2]
            experiment = self.addget_abstract_experiment(experiment_label)
            result = self.addget_result(result_label)
            self.addget_primitive_interaction(experiment, result, valence, meaning)

        for experiment in self.EXPERIMENTS.values():
            interaction = Interaction(experiment.get_label() + "r2")
            interaction.set_valence(1)
            interaction.set_experiment(experiment)
            experiment.set_intended_interaction(interaction)

    def addget_abstract_experiment(self, label):
        if label not in self.EXPERIMENTS:
            experiment = RecursiveExperiment(label)
            self.EXPERIMENTS[label] = experiment
        return self.EXPERIMENTS[label]

    def enact(self, intended_interaction):
        if intended_interaction.is_primitive():
            return self.enact_primitive_interaction(intended_interaction)
            # experiment = intended_interaction.get_experiment()
            # result = self.return_result(experiment)
            # return experiment, result
        else:
            # enact pre-interaction
            enacted_pre_interaction = self.enact(intended_interaction.get_pre_interaction())
            if enacted_pre_interaction != intended_interaction.get_pre_interaction():
                return enacted_pre_interaction
            else:
                # enact post-interaction
                enacted_post_interaction = self.enact(intended_interaction.get_post_interaction())
                return self.addget_composite_interaction(enacted_pre_interaction, enacted_post_interaction)

    def enact_primitive_interaction(self, intended_interaction):
        """Implements the cognitive coupling between the agent and the environment.
        Tries to enact primitive intended_interaction."""
        experiment = intended_interaction.get_experiment()
        result_label = self.environment.return_result(experiment)
        result = self.addget_result(result_label)
        return self.addget_primitive_interaction(experiment, result)

    def select_experiment(self, anticipations):
        anticipations.sort(key=lambda x: x.compare(), reverse=True)  # choose by valence
        selected_anticipation = anticipations[0]
        return selected_anticipation.get_experiment()

    def anticipate(self):
        anticipations = self.get_default_anticipations()
        # print "Default anticipations: ", anticipations
        if self.context_interaction is not None:
            activated_interactions = self.get_activated_interactions()
            for activated_interaction in activated_interactions:
                # print "activated interaction: ", activated_interaction
                experiment = activated_interaction.get_post_interaction().get_experiment()
                # print "activated experiment: " + experiment.get_label()
                proclivity = activated_interaction.get_weight() * activated_interaction.get_post_interaction().get_valence()
                # print "activated proclivity: " + str(proclivity)
                anticipation = RecursiveAnticipation(experiment, proclivity)
                # print "activated anticipation: ", anticipation
                if anticipation not in anticipations:
                    anticipations.append(anticipation)
                else:
                    index = anticipations.index(anticipation)
                    anticipations[index].add_proclivity(proclivity)
                # print "Afforded ", anticipation
        return anticipations

    def get_default_anticipations(self):
        """All known experiments are proposed by default with proclivity 0"""
        anticipations = []
        for experiment in self.EXPERIMENTS.values():
            if not experiment.is_abstract:
                anticipation = RecursiveAnticipation(experiment, 0)
                anticipations.append(anticipation)
        random.shuffle(anticipations) # shuffle order
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

    def get_context_interaction(self):
        return self.context_interaction

    def set_context_interaction(self, enacted_interaction):
        self.context_interaction = enacted_interaction

    def get_context_pair_interaction(self):
        return self.context_pair_interaction

    def set_context_pair_interaction(self, enacted_pair_interaction):
        self.context_pair_interaction = enacted_pair_interaction

    # Learning:
    def learn_recursive_interaction(self, enacted_interaction):
        enacted_pair_interaction = None
        if self.context_interaction is not None:
            # if hist[-1]: learn(hist[-1], enacted)
            enacted_pair_interaction = self.addreinforce_composite_interaction(self.context_interaction, enacted_interaction)

            if self.context_pair_interaction is not None:
                # if hist[-1] and hist[-2]
                # learn <penultimate <previous current>>
                self.addreinforce_composite_interaction(self.context_pair_interaction.get_pre_interaction(), enacted_pair_interaction)
                # learn <<penultimate previous> current>
                self.addreinforce_composite_interaction(self.context_pair_interaction, enacted_interaction)

        self.set_context_interaction(enacted_interaction)
        self.set_context_pair_interaction(enacted_pair_interaction)

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
            experiment_label = interaction.get_label().upper()
            new_experiment = self.addget_abstract_experiment(experiment_label)
            new_experiment.set_abstract()
            new_experiment.set_intended_interaction(interaction)
            interaction.set_experiment(new_experiment)
        return interaction


class ConstructiveExistence(RecursiveExistence):
    """
    In constructive existence the basic unit of analysis and implementation is interaction, not experiments and results.
    """
    def __init__(self, primitive_interactions, environment):
        RecursiveExistence.__init__(self, primitive_interactions, environment)

    # Existence 50.2
    def step(self):
        # print "Memory: ", self.INTERACTIONS.keys()
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

        if enacted_interaction.get_valence() >= 0:
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
            abstract_experiment = RecursiveExperiment(label)
            abstract_experiment.set_intended_interaction(interaction)
            abstract_experiment.set_abstract()
            interaction.set_experiment(abstract_experiment)
            self.EXPERIMENTS[label] = abstract_experiment
        return self.EXPERIMENTS[label]

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
            self.addget_abstract_experiment(interaction)
        return interaction

    # Existence 50.2
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
                anticipation = ConstructiveAnticipation(proposed_interaction, proclivity)
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

    # Existence 50.2
    def get_default_anticipations(self):
        anticipations = []
        for interaction in self.INTERACTIONS.values():
            if interaction.is_primitive():
                # print "interaction is primitive"
                anticipation = ConstructiveAnticipation(interaction, 0)
                # print "adding anticipation", anticipation
                anticipations.append(anticipation)
        # sort default anticipations by valence - this could be random...
        anticipations.sort(key=lambda x: x.get_interaction().get_valence(), reverse=True)
        #anticipations.sort(key=lambda x: x.get_interaction().get_label())
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

    def select_interaction(self, anticipations):
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

    # # Existence 50 and 50.1
    # def step(self):
    #     anticipations = self.anticipate()
    #     print "Anticipations: ", anticipations
    #     experiment = self.select_experiment(anticipations)  # RecursiveExperiment
    #     print "Selected experiment: ", experiment
    #     intended_interaction = experiment.get_intended_interaction()
    #     print "Intended interaction: ", intended_interaction
    #     enacted_interaction = self.enact(intended_interaction)
    #     print "Enacted interaction: ", enacted_interaction
    #     # existence 50
    #     if enacted_interaction != intended_interaction:
    #         experiment.add_enacted_interaction(enacted_interaction)
    #
    #     # # existence 50.1
    #     # if enacted_interaction != intended_interaction:
    #     #     label = enacted_interaction.get_label().upper()
    #     #     failed_result = self.addget_result(label)
    #     #     if enacted_interaction.get_experiment() is None:
    #     #         enacted_interaction.set_experiment(experiment)
    #     #         enacted_interaction.set_result(failed_result)
    #     #     elif enacted_interaction.get_experiment() != experiment:
    #     #         valence = enacted_interaction.get_valence()
    #     #         enacted_interaction = self.addget_primitive_interaction(experiment, failed_result, valence)
    #
    #     if enacted_interaction.get_valence() > 0:
    #         self.mood = 'HAPPY'
    #     else:
    #         self.mood = 'SAD'
    #
    #     self.learn_recursive_interaction(enacted_interaction)
    #
    #     return enacted_interaction.__repr__() + " " + self.mood

    # def anticipate(self):
    #     """The proclivity of anticipation is now balanced depending on the odds of obtaining the afforded interaction
    #     and the odds of obtaining a different enacted interaction"""
    #     anticipations = self.get_default_anticipations()
    #     activated_interactions = self.get_activated_interactions()
    #     if self.context_interaction is not None:
    #         for activated_interaction in activated_interactions:
    #             experiment = activated_interaction.get_post_interaction().get_experiment()
    #             proclivity = activated_interaction.get_weight() * activated_interaction.get_post_interaction().get_valence()
    #             anticipation = RecursiveAnticipation(experiment, proclivity)
    #             if anticipation not in anticipations:
    #                 anticipations.append(anticipation)
    #             else:
    #                 index = anticipations.index(anticipation)
    #                 anticipations[index].add_proclivity(proclivity)
    #             # print "Afforded " + anticipation.__repr__()
    #
    #     for anticipation in anticipations:
    #         enacted_interactions = anticipation.get_experiment().get_enacted_interactions()
    #         for interaction in enacted_interactions:
    #             for activated_interaction in activated_interactions:
    #                 if interaction == activated_interaction.get_post_interaction():
    #                     proclivity = activated_interaction.get_weight() * interaction.get_valence()
    #                     anticipation.add_proclivity(proclivity)
    #     return anticipations

    # def get_default_anticipations(self):
    #     anticipations = []
    #     for experiment in self.EXPERIMENTS.values():
    #         default_experiment = experiment
    #         if default_experiment.get_intended_interaction().is_primitive():
    #             anticipation = RecursiveAnticipation(experiment, 0)
    #             anticipations.append(anticipation)
    #     random.shuffle(anticipations) # shuffle order
    #     return anticipations
