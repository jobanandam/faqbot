entries = [1, 2]


def stack_pop(e):
    print("Stack is populated with ")
    for entry in e:
        print(entry)

    if len(e) == 0:
        print("nothing to pop")
    else:
        print("Removing top element", len(e))
        e.pop()


def stack_push(e):
    e.insert(len(e), input("Insert <<"))


def stack_is_empty(e):
    if len(e).__ge__(0):
        print("No")
    else:
        print("Yes")


def stack_top(e):
    print(e.__getitem__(len(e).__sub__(1)))


def stack_list(e):
    for ee in e:
        print(ee)


while True:
    print("Data Structure Implementation using Python")
    print("1.Stack")
    print("X.Exit")
    ip = input("Enter a number to see implementation ->")
    if ip.__eq__("1"):
        while True:
            print("You Chose Stack Implementation")
            print("1.Push")
            print("2.Pop")
            print("3.is Empty?")
            print("4.Top")
            print("5.List")
            print("x.Exit")
            op = input("What do you want to do ? enter no < ")
            if op.__eq__("1"):
                stack_push(entries)
            elif op.__eq__("2"):
                stack_pop(entries)
            elif op.__eq__("3"):
                stack_is_empty(entries)
            elif op.__eq__("4"):
                stack_top(entries)
            elif op.__eq__("5"):
                stack_list(entries)
            elif op.__eq__("x"):
                break

    elif ip.__eq__("x"):
        break
