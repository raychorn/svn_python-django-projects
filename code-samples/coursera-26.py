import re
def convert_phone_number(phone):
    result = phone
    print(phone)
    results = re.search(r'(\d{3}[-| ]\d{3}[-| ]\d{4}|[+]?\d{1,3}[-| ]?\d{3}[-| ]\d{3}[-| ]\d{4}|\d{10,11})', phone)
    if (results):
        print(results.groups())
        toks = re.split(r'[ -]', results.groups()[0])
        #result = phone.replace(results.groups()[0], '({}) {}-{}'.format(toks[0], toks[1], toks[2]) if (len(toks) == 3) else '{} ({}) {}-{}'.format(toks[0], toks[1], toks[2], toks[3]))
        result = phone.replace(results.groups()[0], '({}) {}-{}'.format(toks[0], toks[1], toks[2]) if (len(toks) == 3) else '{} {} {} {}'.format(toks[0], toks[1], toks[2], toks[3]))
        print(result)
        print('-'*30)
    return result

print(convert_phone_number("My number is 212-345-9999.")) # My number is (212) 345-9999.
print(convert_phone_number("Please call 888-555-1234")) # Please call (888) 555-1234
print(convert_phone_number("123-123-12345")) # 123-123-12345
print(convert_phone_number("Phone number of Buckingham Palace is +44 303 123 7300")) # Phone number of Buckingham Palace is +44 303 123 7300