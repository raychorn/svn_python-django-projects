def format_address(address_string):
  toks = address_string.split()
  unit_number = None
  rest_of_the_address = ''
  for i, tok in enumerate(toks):
    if (not unit_number):
      if (str(tok).isdigit()):
        unit_number = tok
        rest_of_the_address = ' '.join(toks[i+1:])
  return "house number {} on street named {}".format(unit_number, rest_of_the_address)

print(format_address("123 Main Street"))
# Should print: "house number 123 on street named Main Street"

print(format_address("1001 1st Ave"))
# Should print: "house number 1001 on street named 1st Ave"

print(format_address("55 North Center Drive"))
# Should print "house number 55 on street named North Center Drive"
