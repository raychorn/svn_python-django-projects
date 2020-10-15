def solution(A):
    v = []
    if (len(A) < 2) :
        return False
    for i in A:
        __is__ = 0
        n = i + 1
        if (n in A):
            if (not any([n in vv for vv in v])):
                v.append(tuple([i,n]))
            __is__ += 1
        n = i - 1
        if (n in A):
            if (not any([n in vv for vv in v])):
                v.append(tuple([i,n]))
            __is__ += 1
        return len(v) > 0

print solution([7])

print solution([4,3])

print solution([11,1,8,12,14])

print solution([4,10,8,5,9])

print solution([5,5,5,5,5])
