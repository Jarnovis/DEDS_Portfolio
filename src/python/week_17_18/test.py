from LinkedList import LinkedListPopulated, LinkedListEmpty

def test_toString():
    print("----------------test_toString-----------------")
    empty = LinkedListEmpty()
    print("Lege lijst:", empty.toString())

    lijst1 = LinkedListPopulated([22])
    print("Lijst met 1 element:", lijst1.toString())

    lijst2 = LinkedListPopulated([22, 23])
    print("Lijst met 2 elementen:", lijst2.toString())

def test_addFirst():
    print("----------------test_addFirst---------------------")
    lijst = LinkedListPopulated([4, 7])
    new_lijst = lijst.add_first_new_list(5)

    print("Lijst voor addFirst:", lijst.toString())
    print("Lijst na gebruik addFirst:", new_lijst.toString())

def test_remove():
    print("-------------------test_remove-----------------------")
    lijst = LinkedListPopulated([5, 4, 7, 4])
    new_lijst = lijst.remove(4)

    print("Lijst voor remove:", lijst.toString())
    print("Lijst na remove:", new_lijst.toString())

    new_lijst_2 = new_lijst.remove(4)
    print("Lijst na 2de keer remove:", new_lijst_2.toString())

def test_smallest():
    print("----------------test_smallest-------------------")
    lijst = LinkedListPopulated([5, 4, 7])

    print("Lijst:", lijst.toString())
    print("Kleinste in lijst:", lijst.smallest())

def test_sortSimple():
    print("-----------test_sortSimple--------------")
    lijst = LinkedListPopulated([5, 4, 7, 4])
    print("Lijst zonder sortering:", lijst.toString())
    print("Lijst met sortering:", lijst.order().toString())

    lijst2 = LinkedListPopulated([10, 4, 7, 2, 8, 3])
    print("Lijst zonder sortering:", lijst2.toString())
    print("Lijst met sortering:", lijst2.order().toString())

def test_uniq():
    print("--------------------------test_uniq----------------")
    lijst = LinkedListPopulated([1, 2, 2, 2, 3, 3, 3, 4, 5, 5, 6, 7, 8, 8, 8, 8])
    print("Lijst:", lijst.toString())
    print("Aantal unieke in de lijst:", lijst.unique())