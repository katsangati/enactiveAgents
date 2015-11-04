from existence import Existence

__author__ = 'katja'


if __name__ == '__main__':
    ex = Existence()

    for i in range(0, 15):
        stepTrace = ex.step()
        print (i, stepTrace)
