from LinkedList import LinkedListPopulated, LinkedListEmpty

def test_toString():
    print("----------------test_toString-----------------")
    empty = LinkedListEmpty()
    print("Lege ll:", empty.toString())

    ll1 = LinkedListPopulated([22])
    print("ll met 1 element:", ll1.toString())

    ll2 = LinkedListPopulated([22, 23])
    print("ll met 2 elementen:", ll2.toString())

def test_addFirst():
    print("----------------test_addFirst---------------------")
    ll = LinkedListPopulated([4, 7])
    new_ll = ll.addFirstNewList(5)

    print("ll voor addFirst:", ll.toString())
    print("ll na gebruik addFirst:", new_ll.toString())

def test_remove():
    print("-------------------test_remove-----------------------")
    ll = LinkedListPopulated([5, 4, 7, 4])
    new_ll = ll.remove(4)

    print("ll voor remove:", ll.toString())
    print("ll na remove:", new_ll.toString())

    new_ll_2 = new_ll.remove(4)
    print("ll na 2de keer remove:", new_ll_2.toString())

def test_smallest():
    print("----------------test_smallest-------------------")
    ll = LinkedListPopulated([5, 4, 7])

    print("ll:", ll.toString())
    print("Kleinste in ll:", ll.smallest())

def test_sortSimple():
    print("-----------test_sortSimple--------------")
    ll = LinkedListPopulated([5, 4, 7, 4])
    print("ll zonder sortering:", ll.toString())
    print("ll met sortering:", ll.order().toString())

    ll2 = LinkedListPopulated([10, 4, 7, 2, 8, 3])
    print("ll zonder sortering:", ll2.toString())
    print("ll met sortering:", ll2.order().toString())

def test_uniq():
    print("--------------------------test_uniq----------------")
    ll = LinkedListPopulated([1, 2, 2, 2, 3, 3, 3, 4, 5, 5, 6, 7, 8, 8, 8, 8])
    print("ll:", ll.toString())
    print("Aantal unieke in de ll:", ll.unique())
    
def test_sublist():
    print("---------------- test_subList ----------------")
    ll = LinkedListPopulated([5, 4, 7, 4])
    print("Originele lijst:", ll.toString())

    sub = ll.subList(1, 3)
    print("subList(1, 3):", sub.toString())

def test_merge():
    print("---------------- test_merge ----------------")
    ll1 = LinkedListPopulated([4, 4, 5, 7])
    ll2 = LinkedListPopulated([2, 6, 7])
    
    print("ll1 voor merge:", ll1.toString())
    print("ll2 voor merge:", ll2.toString())

    merged = ll1.merge(ll2)
    print("Gecombineerde en gesorteerde lijst:", merged.toString())

def test_sort_merge():
    print("---------------- test_sort_merge ----------------")
    ll = LinkedListPopulated([5, 4, 7, 4])
    print("Lijst voor sortMerge:", ll.toString())

    sorted_ll = ll.sortMerge()
    print("Lijst na sortMerge:", sorted_ll.toString())