def reassign(list):
  list = [0, 1]

def append(list):
  list.append(1)

list = [0]
# reassign(list)  # not do what I want
append(list)
print(list)



listA = [0]
listB = listA
listB.append(1)
print (listA)