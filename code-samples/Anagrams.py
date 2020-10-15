"""
Anagram Finder. For a given string, find anagrams of the word that are valid words in a dictionary.  An anagram is reordering of the letters in a given string.  Example, if the input is “lame” and the dictionary is {“meal”, “male”, “female”, “camel”}, the output should be {“meal”, “male”}.
"""
l = ['meal', 'male', 'female', 'camel', 'mmeee']

tests = [tuple(['meal', 'male', True]), tuple(['lame', 'male', True])]

def freq_anal(a_word):
    d = {}
    for c in a_word:
        if (d.has_key(c)):
            d[c] += 1
        else:
            d[c] = 1
    return d


def freq_match(d1, d2):
    cnt = 0
    for k,v in d1.iteritems():
        if (d2.has_key(k)) and (d2[k] == v):
            cnt += 1
    return (cnt == len(d1.keys())) and (cnt == len(d2.keys())) and (len(d1.keys()) == len(d2.keys()))


def is_anagram(word1, word2):
    d1 = freq_anal(word1)
    d2 = freq_anal(word2)
    print '%s --> %s' % (word1, d1)
    print '%s --> %s' % (word2, d2)
    __is__ = freq_match(d1, d2)
    print '%s' % (__is__)
    return __is__

given_word = 'lame'

for  i in xrange(0, len(l)):
    word = l[i]
    print word
    difference = is_anagram(word, given_word)
    if (difference):
        print '%s and %s --> %s' % (word, given_word, difference)
        print 'ANAGRAM !!!'
    print '='*5
    print '-'*30
