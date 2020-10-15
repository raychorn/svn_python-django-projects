def octal_to_string(octal):
    result = ""
    value_letters = [(4,"r"),(2,"w"),(1,"x")]
    for octet in [int(n) for n in str(octal)]:
        b = format(octet, '03b')
        for n,v in enumerate(b):
            if (int(v) > 0):
                result += value_letters[n][-1]
            else:
                result += '-'
    return result
    
print(octal_to_string(755)) # Should be rwxr-xr-x
print(octal_to_string(644)) # Should be rw-r--r--
print(octal_to_string(750)) # Should be rwxr-x---
print(octal_to_string(600)) # Should be rw-------