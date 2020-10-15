'''
Write a Python program to remove and print every third number from a list of numbers until the list becomes empty.
'''

def nibble_thirds_method1(l):
    while (len(l) > 0):
        r = []
        for i in range(0, len(l), 3):
            print('l[%d] = %s' % (i, l[i]))
            r.append(i)
        r.reverse()
        for i in r:
            print('delete %d' % (i))
            del l[i]

nibble_thirds_method1([1,2,3,4,5,6,7,8,9])
