def _partition(list, start, end):
    pivot = list[end]
    bottom = start-1
    top = end

    done = 0
    while not done:

        while not done:
            bottom = bottom+1

            if bottom == top:
                done = 1
                break

            if pivot < list[bottom]:
                list[top] = list[bottom]
                break

        while not done:
            top = top-1
            
            if top == bottom:
                done = 1
                break

            if list[top] < pivot:
                list[bottom] = list[top]
                break

    list[top] = pivot
    return top


def _quicksort(list, start, end):
    if start < end:
        split = _partition(list, start, end)
        _quicksort(list, start, split-1)
        _quicksort(list, split+1, end)

def quicksort(list):
    if len(list) > 1:
        _quicksort(list, 0, len(list)-1)

# ____________________________________________________________

if (__name__ == '__main__'):
    import random, time, psyco
    l = range(10000)
    random.shuffle(l)
    
    TIMEIT = "psyco.proxy(quicksort)(l)"
    
    print TIMEIT, ':',
    t = time.time()
    exec TIMEIT
    print time.time() - t
    
    assert l == range(10000)

    TIMEIT = "quicksort(l)"
    print TIMEIT, ':',
    t = time.time()
    exec TIMEIT
    print time.time() - t
    
    TIMEIT = "l.sort()"
    print TIMEIT, ':',
    t = time.time()
    exec TIMEIT
    print time.time() - t
    

