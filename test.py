from copy import deepcopy

array = [[1, 2], [3, 4]]
array_copy = array.copy()
array_deepcopy = deepcopy(array_copy)

array[0].pop(0)

a = 1
a = a + 2
