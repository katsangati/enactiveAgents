__author__ = 'katja'

from existence import Existence

if __name__ == '__main__':
    ex = Existence()

    for i in range(0, 15):
        stepTrace = ex.step()
        print (i, stepTrace)
