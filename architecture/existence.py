__author__ = 'katja'

from interaction import Interaction
from experiment import Experiment
from result import Result


class Existence:
    LABEL_E1 = "e1"
    LABEL_E2 = "e2"
    LABEL_R1 = "r1"
    LABEL_R2 = "r2"
    MOODS = ['HAPPY', 'SAD']
    EXPERIMENTS = dict()
    INTERACTIONS = dict()
    RESULTS = dict()

    mood = None
    previousExperiment = None

    def __init__(self):
        e1 = self.add_experiment(self.LABEL_E1)
        e2 = self.add_experiment(self.LABEL_E2)
        r1 = self.add_result(self.LABEL_R1)
        r2 = self.add_result(self.LABEL_R2)
        self.add_primitive_interaction(e1, r1, -1)
        self.add_primitive_interaction(e1, r2, 1)
        self.add_primitive_interaction(e2, r1, -1)
        self.add_primitive_interaction(e2, r2, 1)
        self.previousExperiment = e1

    def step(self):
        experiment = self.previousExperiment
        #anticipated_result = self.predict(experiment)
        if self.mood == 'SAD':
            experiment = self.get_other_experiment(experiment)
        result = self.return_result(experiment)
        enacted_interaction = self.get_primitive_interaction(experiment, result)

        if enacted_interaction.get_valence() > 0:
            self.mood = 'HAPPY'
        else:
            self.mood = 'SAD'

        self.previousExperiment = experiment
        return experiment.get_label() + result.get_label() + " " + self.mood

    def predict(self, experiment):
        predicted_interaction = None
        predicted_result = None
        for key, inter in self.INTERACTIONS.items():
            if inter.get_experiment() == experiment:
                predicted_interaction = inter
        if predicted_interaction is not None:
            predicted_result = predicted_interaction.get_result()
        return predicted_result

    def add_primitive_interaction(self, experiment, result, valence):
        label = experiment.get_label() + result.get_label()
        if not (label in self.INTERACTIONS):
            inter = Interaction(label, valence)
            inter.set_experiment(experiment)
            inter.set_result(result)
            inter.set_valence(valence)
            self.INTERACTIONS[label] = inter
        return self.INTERACTIONS[label]

    def get_primitive_interaction(self, experiment, result):
        label = experiment.get_label() + result.get_label()
        return self.INTERACTIONS[label]

    def add_result(self, label):
        if not (label in self.RESULTS):
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

    def get_other_experiment(self, experiment):
        for key, exp in self.EXPERIMENTS.items():
            if exp != experiment:
                return exp
        return experiment

    def return_result(self, experiment):
        if experiment == self.get_experiment(self.LABEL_E1):
            return self.get_result(self.LABEL_R1)
        else:
            return self.get_result(self.LABEL_R2)






#     def step(self):
#         anticipations = self.anticipate()
#         experience = self.selectInteraction(anticipations).getExperience()
#         result = self.returnResult030(experience)
#         enactedInteraction = self.getInteraction(experience.getLabel() + result.getLabel())
#         print "Enacted "+ enactedInteraction.__repr__()
#         if enactedInteraction.getValence() >= 0:
#             self.mood = 'PLEASED'
#         else:
#             self.mood = 'PAINED'
#
#         self.learnCompositeInteraction(enactedInteraction)
#
#         self.setEnactedInteraction(enactedInteraction)
#
#         return self.mood
#
#     def learnCompositeInteraction(self, interaction):
#         preInteraction = self.getEnactedInteraction()
#         postInteraction = interaction
#         if preInteraction != None:
#             self.addOrGetCompositeInteraction(preInteraction, postInteraction)
#
#     def addOrGetCompositeInteraction(self, preInteraction, postInteraction):
#         valence = preInteraction.getValence() + postInteraction.getValence()
#         interaction = self.addOrGetInteraction(preInteraction.getLabel() + postInteraction.getLabel())
#         interaction.setPreInteraction(preInteraction)
#         interaction.setPostInteraction(postInteraction)
#         interaction.setValence(valence)
#         print "learn " + interaction.getLabel()
#         return interaction
#
#     def createInteraction(self, label):
#         return Interaction03(label)
#
#     def anticipate(self):
#         anticipations=[]
#         if self.getEnactedInteraction() != None:
#             for activatedInteraction in self.getActivatedInteractions():
#                 proposedInteraction = activatedInteraction.getPostInteraction()
#                 anticipations.append(Anticipation03(proposedInteraction))
#                 print "afforded " + proposedInteraction.__repr__()
#         return anticipations
#
#     def selectInteraction(self, anticipations):
#         if (len(anticipations) > 0):
#             anticipations.sort(key = lambda x: x.compareTo())
#             affordedInteraction = anticipations[0].getInteraction()
#             if affordedInteraction.getValence() >= 0:
#                 intendedInteraction = affordedInteraction
#             else:
#                 intendedInteraction = self.getOtherInteraction(affordedInteraction)
#
#         else :
#             intendedInteraction = self.getOtherInteraction(None)
#         return intendedInteraction
#
#     def getActivatedInteractions(self) :
#         activatedInteractions = []
#         if self.getEnactedInteraction() != None:
#             for activatedInteraction in self.INTERACTIONS:
#                 if activatedInteraction.getPreInteraction() == self.getEnactedInteraction():
#                     activatedInteractions.append(activatedInteraction)
#         return activatedInteractions
#
#     def getInteraction(self, label):
#         try:
#             ll=[a.getLabel() for a in self.INTERACTIONS]
#         except:
#             ll=[]
#         return  self.INTERACTIONS[ll.index(label)]
#
#     def getOtherInteraction(self, interaction):
#         otherInteraction = self.INTERACTIONS[0]
#         if interaction != None:
#             for e in self.INTERACTIONS:
#                 if e.getExperience() != None and e.getExperience() != interaction.getExperience():
#                     otherInteraction =  e
#                     break
#         return otherInteraction
#
#     def setEnactedInteraction(self, enactedInteraction):
#         self.enactedInteraction = enactedInteraction
#
#     def getEnactedInteraction(self):
#         return self.enactedInteraction
#
#     def returnResult030(self, experience):
#         result = None
#         if self.getPreviousExperience() == experience:
#             result =  self.createOrGetResult(self.LABEL_R1)
#         else:
#             result =  self.createOrGetResult(self.LABEL_R2)
#         self.setPreviousExperience(experience)
#         return result
#
#     ##
#
#     def addOrGetPrimitiveInteraction(self, experience, result, valence=None):
#         label = experience.getLabel() + result.getLabel()
#         try:
#             ll=[a.getLabel() for a in self.INTERACTIONS]
#         except:
#             ll=[]
#         if not (label in ll):
#             inter03 = Interaction03(label)
#             inter03.setExperience(experience)
#             inter03.setResult(result)
#             inter03.setValence(valence)
#             self.INTERACTIONS.append(inter03)
#
#         return inter03
#
#     def addOrGetInteraction(self, label):
#         i3=None
#         try:
#             ll=[a.getLabel() for a in self.INTERACTIONS]
#         except:
#             ll=[]
#         if not (label in ll):
#             i3 = Interaction03(label)
#             self.INTERACTIONS.append(i3)
#         else:
#             i3 = self.INTERACTIONS[ll.index(label)]
#         return i3
#
#     def getPreviousExperience(self):
#         return self.previousExperience
#
#     def setPreviousExperience(self, previousExperience):
#         self.previousExperience = previousExperience
#
#
# class Existence031(Existence03):
#     INTERACTIONS=list()
#     T1=8
#     T2=15
#     clock=0
#     def __init__(self):
#         Existence03.__init__(self)
#
#     def step(self):
#
#         anticipations = self.anticipate()
#         experience = self.selectExperience(anticipations)
#         #result = self.returnResult030(experience)
#         result = self.returnResult031(experience)
#
#         enactedInteraction = self.getInteraction(experience.getLabel() + result.getLabel())
#         print "Enacted "+ enactedInteraction.__repr__()
#         if enactedInteraction.getValence() >= 0:
#             self.mood = 'PLEASED'
#         else:
#             self.mood = 'PAINED'
#
#         self.learnCompositeInteraction(enactedInteraction)
#
#         self.setEnactedInteraction(enactedInteraction)
#
#         return self.mood
#
#     def learnCompositeInteraction(self, enactedInteraction):
#         preInteraction = self.getEnactedInteraction()
#         postInteraction = enactedInteraction
#         if preInteraction != None:
#             interaction = self.addOrGetCompositeInteraction(preInteraction, postInteraction)
#             interaction.incrementWeight()
#
#     def createInteraction(self, label):
#         return Interaction031(label)
#
#     def anticipate(self):
#         anticipations=self.getDefaultAnticipations()
#         if self.getEnactedInteraction() != None:
#             for activatedInteraction in self.getActivatedInteractions():
#                 proposition = Anticipation031(activatedInteraction.getPostInteraction().getExperience(),activatedInteraction.getWeight()*activatedInteraction.getPostInteraction().getValence())
#                 idx = [ a.getExperience().getLabel()==proposition.getExperience().getLabel() for a in anticipations]
#                 try:
#                     index = idx.index(True)
#                     anticipations[index].addProclivity(activatedInteraction.getWeight()*activatedInteraction.getPostInteraction().getValence())
#                 except:
#                     anticipations.append(proposition)
#         return anticipations
#
#     def getDefaultAnticipations(self):
#         anticipations = []
#         for k, experience in self.EXPERIENCES.iteritems():
#             anticipation = Anticipation031(experience, 0)
#             anticipations.append(anticipation)
#         return anticipations
#
#
#     def selectExperience(self, anticipations):
#         if (len(anticipations) > 0):
#             anticipations.sort(key = lambda x: x.compareTo(), reverse=True)
#             for anticipation in anticipations:
#                 print "propose "+anticipation.__repr__()
#         selectedAnticipation = anticipations[0]
#         return selectedAnticipation.getExperience()
#
#     def getInteraction(self, label):
#         try:
#             ll=[a.getLabel() for a in self.INTERACTIONS]
#             r = self.INTERACTIONS[ll.index(label)]
#         except:
#             ll=[]
#             r = None
#         return  r
#
#     #Environment031
#
#     def getClock(self):
#         return self.clock
#
#     def incClock(self):
#         self.clock+=1
#
#     def returnResult031(self,experience):
#
#         self.incClock()
#         if self.getClock() <= self.T1 or self.getClock() > self.T2:
#             if experience == self.addOrGetExperience(self.LABEL_E1):
#                 result =  self.createOrGetResult(self.LABEL_R1)
#             else:
#                 result = self.createOrGetResult(self.LABEL_R2)
#
#         else :
#             if experience == self.addOrGetExperience(self.LABEL_E1):
#                 result = self.createOrGetResult(self.LABEL_R2)
#             else:
#                 result = self.createOrGetResult(self.LABEL_R1)
#
#         return result
#     ##
#
#     def addOrGetPrimitiveInteraction(self, experience, result, valence=None):
#         label = experience.getLabel() + result.getLabel()
#         try:
#             ll=[a.getLabel() for a in self.INTERACTIONS]
#         except:
#             ll=[]
#         if not (label in ll):
#             inter03 = Interaction031(label)
#             inter03.setExperience(experience)
#             inter03.setResult(result)
#             inter03.setValence(valence)
#             self.INTERACTIONS.append(inter03)
#
#         return inter03
#
#     def addOrGetInteraction(self, label):
#         i3=None
#         try:
#             ll=[a.getLabel() for a in self.INTERACTIONS]
#         except:
#             ll=[]
#         if not (label in ll):
#             i3 = Interaction031(label)
#             self.INTERACTIONS.append(i3)
#         else:
#             i3 = self.INTERACTIONS[ll.index(label)]
#         return i3
