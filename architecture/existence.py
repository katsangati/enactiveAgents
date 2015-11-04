from interaction import Interaction
from experiment import Experiment
from result import Result
from anticipation import Anticipation
import random

__author__ = 'katja'


class Existence:
    LABEL_E1 = "e1"
    LABEL_E2 = "e2"
    LABEL_E3 = "e3"
    LABEL_E4 = "e4"

    LABEL_R1 = "r1"
    LABEL_R2 = "r2"
    LABEL_R3 = "r3"
    LABEL_R4 = "r4"
    LABEL_R5 = "r5"
    LABEL_R6 = "r6"

    MOODS = ['HAPPY', 'SAD']
    EXPERIMENTS = dict()
    INTERACTIONS = dict()
    RESULTS = dict()

    def __init__(self):
        e1 = self.add_experiment(self.LABEL_E1)
        e2 = self.add_experiment(self.LABEL_E2)
        e3 = self.add_experiment(self.LABEL_E3)
        e4 = self.add_experiment(self.LABEL_E4)

        r1 = self.add_result(self.LABEL_R1)
        r2 = self.add_result(self.LABEL_R2)
        r3 = self.add_result(self.LABEL_R3)
        r4 = self.add_result(self.LABEL_R4)
        r5 = self.add_result(self.LABEL_R5)
        r6 = self.add_result(self.LABEL_R6)

        self.add_primitive_interaction(e1, r1, 1)
        self.add_primitive_interaction(e1, r2, -5000)
        self.add_primitive_interaction(e2, r3, -1)
        self.add_primitive_interaction(e3, r4, -1)
        self.add_primitive_interaction(e4, r5, -1)
        self.add_primitive_interaction(e4, r6, -1)

        self.context_interaction = None
        self.mood = None

    # def step(self):
    #     anticipations = self.anticipate()
    #     # chosen_interaction = self.select_interaction(anticipations)
    #     # print "Intending " + chosen_interaction.__repr__()
    #     # if chosen_interaction is not None:
    #     #     experiment = chosen_interaction.get_experiment()
    #     # else:
    #     #     experiment = self.get_random_experiment()
    #
    #     experiment = self.select_experiment(anticipations)
    #     result = self.return_result(experiment)
    #
    #     enacted_interaction = self.get_interaction(experiment.get_label() + result.get_label())
    #     print "Enacted " + enacted_interaction.__repr__()
    #
    #     if enacted_interaction.get_valence() > 0:
    #         self.mood = 'HAPPY'
    #     else:
    #         self.mood = 'SAD'
    #
    #     self.learn_composite_interaction(self.context_interaction, enacted_interaction)
    #     self.context_interaction = enacted_interaction
    #
    #     return experiment
#        return experiment.get_label() + result.get_label() + " " + self.mood

    def add_primitive_interaction(self, experiment, result, valence):
        label = experiment.get_label() + result.get_label()
        if label not in self.INTERACTIONS:
            interaction = Interaction(label, valence)
            interaction.set_experiment(experiment)
            interaction.set_result(result)
            interaction.set_valence(valence)
            self.INTERACTIONS[label] = interaction

    # def get_primitive_interaction(self, experiment, result):
    #     label = experiment.get_label() + result.get_label()
    #     return self.INTERACTIONS[label]

    def get_interaction(self, label):
        return self.INTERACTIONS[label]

    # def learn_composite_interaction(self, context_interaction, enacted_interaction):
    #     pre_interaction = context_interaction
    #     post_interaction = enacted_interaction
    #     if pre_interaction is not None:
    #         interaction = self.add_composite_interaction(pre_interaction, post_interaction)
    #         interaction.increment_weight()
    #
    # def add_composite_interaction(self, pre_interaction, post_interaction):
    #     valence = pre_interaction.get_valence() + post_interaction.get_valence()
    #     label = pre_interaction.get_label() + post_interaction.get_label()
    #     interaction = self.set_or_get_interaction(label, valence)
    #     interaction.set_pre_interaction(pre_interaction)
    #     interaction.set_post_interaction(post_interaction)
    #     interaction.set_valence(valence)
    #     print "learn " + interaction.get_label()
    #     return interaction
    #
    # def set_or_get_interaction(self, label, valence):
    #     if label not in self.INTERACTIONS:
    #         self.INTERACTIONS[label] = Interaction(label, valence)
    #     return self.INTERACTIONS[label]

    def learn_composite_interaction(self, context_interaction, enacted_interaction):
        if context_interaction is not None:
            label = context_interaction.get_label() + enacted_interaction.get_label()
            if label not in self.INTERACTIONS:
                valence = context_interaction.get_valence() + enacted_interaction.get_valence()
                interaction = Interaction(label, valence)
                interaction.set_pre_interaction(context_interaction)
                interaction.set_post_interaction(enacted_interaction)
                interaction.set_valence(valence)
                self.INTERACTIONS[label] = interaction
                print "Learn " + label
            else:
                interaction = self.INTERACTIONS[label]
                print 'Incrementing weight for ' + interaction.__repr__()
                interaction.increment_weight()

    def anticipate(self):
        anticipations = []
        if self.context_interaction is not None:
            activated_interactions = self.get_activated_interactions()
            for activated_interaction in activated_interactions:
                proposed_interaction = activated_interaction.get_post_interaction()
                proclivity = activated_interaction.get_weight() * proposed_interaction.get_valence()
                #print "activated weight: " + str(activated_interaction.get_weight())
                anticipations.append(Anticipation(proposed_interaction, proclivity))
                print "Afforded " + proposed_interaction.__repr__() + " proclivity: " + str(proclivity)
        return anticipations

    def get_activated_interactions(self):
        activated_interactions = []
        for key in self.INTERACTIONS:
            activated_interaction = self.INTERACTIONS[key]
            if activated_interaction.get_pre_interaction() == self.context_interaction:
                activated_interactions.append(activated_interaction)
        return activated_interactions

#     @staticmethod
#     def select_interaction(anticipations):
#         if len(anticipations) > 0:
# #            anticipations.sort(key=lambda x: x.compare(), reverse=True)
#             anticipations.sort(key=lambda x: x.get_proclivity(), reverse=True)
#             afforded_interaction = anticipations[0].get_interaction()
#             if afforded_interaction.get_valence() >= 0:
#                 intended_interaction = afforded_interaction
#             else:
#                 intended_interaction = None
#         else:
#             intended_interaction = None
#         return intended_interaction

    def select_experiment(self, anticipations):
        if len(anticipations) > 0:
            anticipations.sort(key=lambda x: x.get_proclivity(), reverse=True)
            afforded_interaction = anticipations[0].get_interaction()
            if afforded_interaction.get_valence() >= 0:
                intended_interaction = afforded_interaction
                print "Intending " + intended_interaction.__repr__()
                chosen_experiment = intended_interaction.get_experiment()
            else:
                bad_experiment = afforded_interaction.get_experiment()
                chosen_experiment = self.get_random_experiment()
                while chosen_experiment == bad_experiment:
                    chosen_experiment = self.get_random_experiment()
                print "Don't like the affordance, intending experiment " + chosen_experiment.get_label()
        else:
            chosen_experiment = self.get_random_experiment()
            print "Don't know what to do, intending experiment " + chosen_experiment.get_label()
        return chosen_experiment

    def get_random_experiment(self):
        random_key = random.sample(self.EXPERIMENTS, 1)[0]
        random_experiment = self.EXPERIMENTS[random_key]
        return random_experiment

    def add_result(self, label):
        if label not in self.RESULTS:
            self.RESULTS[label] = Result(label)
        return self.RESULTS[label]

    def get_result(self, label):
        return self.RESULTS[label]

    def add_experiment(self, label):
        if label not in self.EXPERIMENTS:
            self.EXPERIMENTS[label] = Experiment(label)
        return self.EXPERIMENTS[label]

    def get_experiment(self, label):
        return self.EXPERIMENTS[label]

    # def return_result(self, experiment):
    #     if self.context_interaction is not None:
    #         if experiment == self.context_interaction.get_experiment():
    #             result = self.get_result(self.LABEL_R1)
    #         else:
    #             result = self.get_result(self.LABEL_R2)
    #     else:
    #         result = self.get_result(self.LABEL_R2)
    #     return result

