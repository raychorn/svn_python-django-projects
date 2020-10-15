get_sum_of_digits = lambda nn:sum([int(n) for n in '%d' % (nn)])

def solution(nn):
    sum_of_digits = get_sum_of_digits(nn)
    for i in xrange(nn+1,50001):
        sum_of_digits_in_i = get_sum_of_digits(i)
        if (sum_of_digits == sum_of_digits_in_i):
            return i


print solution(28)

print solution(734)

print solution(1990)

print solution(1000)
