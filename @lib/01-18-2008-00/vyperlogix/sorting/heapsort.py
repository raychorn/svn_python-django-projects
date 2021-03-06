import sys 

def heapsort(n, ra) : 
    ir = n 
    l = (n >> 1) + 1 

    while True : 
        if l > 1 : 
            l -= 1 
            rra = ra[l] 
        else : 
            rra = ra[ir] 
            ra[ir] = ra[1] 
            ir -= 1 
            if ir == 1 : 
                ra[1] = rra 
                return 

        i = l 
        j = l << 1 
        while j <= ir : 
            if (j < ir) and (ra[j] < ra[j + 1]) : 
                j += 1 

            if rra < ra[j] : 
                ra[i] = ra[j] 
                i = j 
                j += j 
            else : 
                j = ir + 1; 
        ra[i] = rra; 

if (__name__ == '__main__'):
    IM = 139968 
    IA =   3877 
    IC =  29573 
    
    LAST = 42 
    def gen_random(max) : 
        global LAST 
        LAST = (LAST * IA + IC) % IM 
        return( (max * LAST) / IM ) 
    
    def main() : 
        if len(sys.argv) == 2 : 
            N = int(sys.argv[1]) 
        else : 
            N = 100
    
        ary = [None]*(N + 1) 
        for i in xrange(1, N + 1) : 
            ary[i] = gen_random(1.0) 
    
        heapsort(N, ary) 
    
        print "%.10f" % ary[N] 
        print str(ary)
    
    main() 
