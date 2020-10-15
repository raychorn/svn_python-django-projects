def solution(A):
    d = {}
    for i in A:
        if (not d.has_key(i)):
            d[i] = 1
        else:
            d[i] += 1
    for k,v in d.iteritems():
        if (v % 2):
            return False
    return True


print solution([1,2,2,1])

print solution([7,7,7])

print solution([1,2,2,3])

