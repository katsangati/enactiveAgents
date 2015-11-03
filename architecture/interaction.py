__author__ = 'katja'


class Interaction:
    def __init__(self, label, valence):
        self.label = label
        self.valence = valence
        self.experiment = None
        self.result = None

    def get_label(self):
        return self.label

    def get_experiment(self):
        return self.experiment

    def get_result(self):
        return self.result

    def set_experiment(self, experiment):
        self.experiment = experiment

    def set_result(self, result):
        self.result = result

    def get_valence(self):
        return self.valence

    def set_valence(self, valence):
        self.valence = valence

    # def __repr__(self):
    #     return self.getLabel() + ',' + self.getValence()

# class Interaction031(Interaction03):
#     weight = 0
#     def __init__(self, label):
#         Interaction03.__init__(self,label)
#
#     def getWeight(self):
#         return self.weight
#
#     def incrementWeight(self):
#         self.weight +=1
#
#     def __repr__(self):
#         return "{0}, valence {1}, weight {2}".format(self.getLabel(),self.getValence(),self.getWeight())
#     __author__ = 'michel'
#
# from interaction01 import Interaction01
# from experiment import Experiment
# from result import Result
#
#
# class Interaction03(Interaction01):
#     valence = 0.0
#     preInteraction=None
#     postInteraction=None
#
#     def __init__(self, label):
#         Interaction01.__init__(self, label)
#
#     def getValence(self):
#         return self.valence
#
#     def setValence(self, valence):
#         self.valence = valence
#
#     def getPreInteraction(self):
#         return self.preInteraction
#
#     def setPreInteraction(self,preInteraction):
#         self.preInteraction = preInteraction
#
#     def getPostInteraction(self):
#         return self.postInteraction
#
#     def setPostInteraction(self,postInteraction):
#         self.postInteraction = postInteraction
#
#     def isPrimitive(self):
#         return self.preInteraction==None
#
#     def __repr__(self):
#         return "{0}, {1}".format(self.getLabel(),self.getValence())