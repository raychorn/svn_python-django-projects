def skipper(elements, use_odd=False):
    n = 0
    for ele in elements:
        if (((n+1) % 2) == (0 if (not use_odd) else 1)):
            yield ele
        n += 1
        
print([i for i in skipper([1,2,3,4,5,6])])
print([i for i in skipper([1,2,3,4,5,6], use_odd=True)])
