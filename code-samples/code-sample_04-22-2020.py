def compress(str1):
    d = {}
    for ch in str1:
        if (d.has_key(ch)):
            cnt = d[ch] + 1
            d[ch] = cnt
        else:
            d[ch] = 1
    resp = []
    s_keys = d.keys()
    s_keys.sort()
    for k in s_keys:
        v = d[k]
        i = []
        n = len('%d' % v)
        t = 0
        vv = v
        while (vv > 0):
            m = 9 if (vv > 9) else vv
            i.append(tuple([k,m]))
            vv -= m
            t += m
        assert t == v, 'Check your logic.'
        for item in i:
            resp.append('%s%d' % (item[0],item[-1]))
    return ''.join(resp)


def uncompress(str1):
    c = None
    resp = []
    for ch in str1:
        if (c == None):
            c = ch
        elif (str(ch).isdigit()):
            v = int(ch)
            resp.append(''.join([c for i in xrange(v)]))
            c = None
    return ''.join(resp)


def __main__():
    case_num = 1
    vals = ['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbcdef', 'abcdefg', 'aabcdefg']
    for v in vals:
        val0 = v
        val1 = compress(val0)
    
        val2 = uncompress(val1)
    
        if (val0 == val2):
            print 'Case %s works.' % (case_num)
        else:
            print 'Case %s is not working.' % (case_num)
        case_num += 1

if __name__ == "__main__":
    __main__()