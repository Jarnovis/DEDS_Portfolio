import csv
import sys

sys.setrecursionlimit(20000000)

from LinkedList import LinkedListPopulated 

kentekens = LinkedListPopulated()

with open(sys.argv[1], encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if row:
            kentekens.add(row[0])

ordered_kentekens = kentekens.order()

print("Gesorteerde kentekens:")
ordered_kentekens.toString()

print(f"Aantal unieke kentekens: {ordered_kentekens.unique()}")
