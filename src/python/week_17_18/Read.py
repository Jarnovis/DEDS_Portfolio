import csv
import sys

sys.setrecursionlimit(20000000)

from LinkedList import LinkedListEmpty

kentekens = LinkedListEmpty()

with open(sys.argv[1]) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        print(row)
        kentekens.add(row[0])

order = kentekens.sortMerge()
order.toString()

print(f"Unieke kentekens: {order.unique()}")