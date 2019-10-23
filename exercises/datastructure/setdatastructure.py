def printsetele(x):
    print("Printing the elements in Set")
    for item in x:
        print(item)


def checkifexists(x, ele):
    if (ele in x):
        print("Element exists in set")
    else:
        print("Element doesn't exists in set")


def checkifexists(x, ele):
    if (ele in x):
        print("Element exists in set")
    else:
        print("Element doesn't exists in set")


def unionset(x1, x2):
    if isinstance(x1, set):
        print("Union of two sets", x1 | x2)
    else:
        # if the input is not a type of set, it is converted and then union is performed
        print("Convert and union of two sets", x1.union(x2))

def intersectionset(x1, x2):
    if isinstance(x1, set):
        print("Intersection of two sets", x1 & x2)
    else:
        # if the input is not a type of set, it is converted and then intersection is performed
        print("Convert and Intersection of two sets", x1.intersection(x2))



def addtoset(x, valuetoadd):
    print("Set before adding", x)
    x |= valuetoadd
    print("Set after adding", x)


def gettypeofset(x1, x2):
    if x1 == x2:
        print("the two sets are equal")
    if x1 <= x2:
        print("First Set is a subset of Second Set, Second set is Super set")
    if x1 >= x2:
        print("Second Set is a subset of First Set, First set is Super set")
    else:
        print("Two sets are neither equal, nor one or the other is a subset")


x1 = {1, 2, 3, 4, 5}
x2 = {1, 20, 30, 4, 50}

printsetele(x1)
checkifexists(x2, 20)
unionset(x1, x2)
unionset(set({1, 3, 4}), x2)
intersectionset(x1,x2)
intersectionset(set({1, 22, 43}), x2)
addtoset(x1, {1, 33, 55})
gettypeofset(x1, x2)
