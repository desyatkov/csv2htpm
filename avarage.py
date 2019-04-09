import numpy as np
print(np.average([4, 5, 4, 3, 2], weights=[25, 10, 15, 20, 30]))
print(np.average([4, 5, 4, 3, 2], weights=[20, 20, 20, 20, 20]))
print(np.average([4, 5, 4, 3, 2]))


def round_of_rating(number):
    return round(number * 2) / 2

print(round_of_rating(2.8))
