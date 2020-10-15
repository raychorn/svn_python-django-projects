cases = []
if (1):
    cases.append(tuple(["([)]", False]))
    cases.append(tuple(["()", True]))
    cases.append(tuple(["(", False]))
    cases.append(tuple([")", False]))
    
    cases.append(tuple(["[]", True]))
    cases.append(tuple(["[", False]))
    cases.append(tuple(["]", False]))
    
    cases.append(tuple(["{}", True]))
    cases.append(tuple(["{", False]))
    cases.append(tuple(["}", False]))
    
    cases.append(tuple(["[()]", True]))
    cases.append(tuple(["[(]", False]))
    cases.append(tuple(["[()", False]))
    cases.append(tuple(["[)]", False]))
    cases.append(tuple(["[()", False]))
    cases.append(tuple(["()]", False]))
    cases.append(tuple(["[(", False]))
    cases.append(tuple([")]", False]))
    
    cases.append(tuple(["[({})]", True]))
    cases.append(tuple(["[({", False]))
    cases.append(tuple(["})]", False]))
    
    cases.append(tuple(["[({})({})({})({})]", True]))
    
    cases.append(tuple(["[({}{}{}{})({})({})({})]()", True]))
cases.append(tuple(["[({}{}{}{})({})({})({})(])", False]))

__rules__ = {
    '(' : ')',
    '[' : ']',
    '{' : '}'
}

def invert_dict(d):
    new_d = {}
    for k,v in d.items():
        new_d[v] = k
    return new_d

class Balancer():
    def __count_it__(self, c,d, is_o=False, is_c=False, toks1=[], toks2=[]):
        count_one = lambda c,d : 1 if (not (c in d.keys())) else d[c]+1
        d[c]=count_one(c,d)
        if (is_o):
            toks1.append(c)
        elif (is_c):
            toks2.append(c)
        return c
    
    def __analysis__(self):
        self.tokens = []
        self.tokens2 = []
        for c in self.s:
            is_opener = (c in self.rules.keys())
            is_closer = (c in self.rules.values())
            self.__count_it__(c,self.d, is_o=is_opener, is_c=is_closer, toks1=self.tokens, toks2=self.tokens2)
    
    def __is_balanced__(self, the_str):
        self.d = {}
        self.s = the_str
        if (self.method == 0):
            # This method has two loops...
            self.tokens = [self.__count_it__(c,self.d) for c in self.s if (c in self.rules.keys())]     # this contains the unbalanced tokens for openers
            self.tokens2 = [self.__count_it__(c,self.d) for c in self.s if (c in self.rules.values())]  # this contains the unbalanced tokens for closers
        else:
            # This method has one loop.
            self.__analysis__()
        self.__count__ = 0
        self.num1 = 0
        for k,v in self.rules.items():
            if (k in self.d.keys()):
                self.num1 += 1
            try:
                if (self.d[k] == self.d[v]):
                    self.__count__ += 1
            except KeyError:
                self.__count__ += 0
        stack = []
        __is__ = False
        __str__ = [ch for ch in the_str if (ch in self.rules.keys()) or (ch in self.rules.values())]
        for c in __str__:
            if (c in self.rules.keys()):
                stack.append(c)
            elif (c in self.rules.values()):
                try:
                    val = stack.pop()
                    if (val in self.rules.keys()):
                        if (self.rules[val] == c):
                            __is__ = True
                        else:
                            __is__ = False
                            break
                except IndexError:
                    pass
        return (self.num1 > 0) and (self.__count__ == self.num1) and (len(self.tokens) == len(self.tokens2)) and (__is__)

    def __init__(self, the_str, the_rules={}, the_method=0):
        self.__unmatched__ = []
        self.rules = the_rules
        self.method = the_method
        self.other_rules = invert_dict(the_rules)
        self._is_balanced = self.__is_balanced__(the_str)
        
    @property
    def is_balanced(self): 
        return self._is_balanced

    @property
    def unmatched(self): 
        for k,v in self.d.items():
            if (k in self.rules.keys()):
                closer = self.rules[k]
                if (closer not in self.d.keys()):
                    self.__unmatched__.append(closer)
            elif (k in self.other_rules.keys()):
                opener = self.other_rules[k]
                if (opener not in self.d.keys()):
                    self.__unmatched__.append(opener)
        return list(set(self.__unmatched__))


print('BEGIN: Method #1')
results1 = []
error_results1 = []
for c in cases:
    o = Balancer(c[0], the_rules=__rules__, the_method=0)
    __is__ = o.is_balanced
    is_b = __is__ == c[-1]
    reasons = []
    the_reason = 'Balanced.'
    if (not __is__):
        if (len(o.unmatched) > 0):
            reasons.append('Unmatched %s' % (o.unmatched))
        the_reason = "%s" % (', '.join(reasons) if (len(reasons) > 0) else '')
    results1.append('is_balanced("%s") --> %s :: %s :: %s :: %s' % (c[0], __is__, is_b, the_reason, '' if (is_b) else "*** ERROR, Will Robinson."))
    if (not is_b):
        error_results1.append(results1[-1])
print('END: Method #1')

print('BEGIN: Method #2')
results2 = []
error_results2 = []
for c in cases:
    o = Balancer(c[0], the_rules=__rules__, the_method=1)
    __is__ = o.is_balanced
    is_b = __is__ == c[-1]
    reasons = []
    the_reason = 'Balanced.'
    if (not __is__):
        if (len(o.unmatched) > 0):
            reasons.append('Unmatched %s' % (o.unmatched))
        the_reason = "%s" % (', '.join(reasons) if (len(reasons) > 0) else '')
    results2.append('is_balanced("%s") --> %s :: %s :: %s :: %s' % (c[0], __is__, is_b, the_reason, '' if (is_b) else "*** ERROR, Will Robinson."))
    if (not is_b):
        error_results2.append(results2[-1])
print('END: Method #2')

print('Perform Comparison of Methods.')
if (len(results1) == len(results2)):
    print('Both methods produced the same number of results.')
else:
    print('WARNING 1: Results differ for both methods.')

warnings = 0
for i in range(len(results1)):
    if (results1[i] != results2[i]):
        print('WARNING 2: Results differ for Line No. %s' % (i))
        warnings += 1
        
print('There were %s warnings.%s' % (warnings, ' So both methods are identical.' if (warnings == 0) else ' Which means both methods are NOT identical.'))
for lineno,r in enumerate(results1):
    print('%s --> %s' % (lineno, r))

print('There were %s issues for Method 1.' % (len(error_results1)))
for lineno,r in enumerate(error_results1):
    print('%s --> %s' % (lineno, r))
print('-'*30)

print('There were %s issues for Method 2.' % (len(error_results2)))
for lineno,r in enumerate(error_results2):
    print('%s --> %s' % (lineno, r))
print('-'*30)

print('Run Analysis Complete.')