from existence import RecursiveExistence, ConstructiveExistence
__author__ = 'katja'


if __name__ == '__main__':

    primitive_interactions = {"a": ("e1", "r1", -1), "b": ("e1", "r2", 1),
                              "c": ("e2", "r1", -1), "d": ("e2", "r2", 1)}

    primitive_interactions_world = {"move forward": ("e1", "r1", 5), "bump": ("e1", "r2", -10),
                              "turn left": ("e2", "r3", -1), "turn right": ("e3", "r4", -1),
                              "touch empty": ("e4", "r5", -1), "touch wall": ("e4", "r6", -2)}

    # ex = Existence()
    ex = RecursiveExistence(primitive_interactions)
    # ex = ConstructiveExistence(primitive_interactions)

    for i in range(0, 50):
        stepTrace = ex.step()
        print (i, stepTrace)
        print "\n"
