# -*- encoding=utf8 -*-
list1 = ["0:0", "0:1", "0:2", "0:3"]
list2 = ["0:0", "0:1", "0:5", "0:6"]
for item in list2:
    if item in list1:
        list1.remove(item)
print(list1)
