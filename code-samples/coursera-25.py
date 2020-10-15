import re
def transform_comments(line_of_code):
    result = line_of_code
    results = re.search(r'([#]+.*)', line_of_code)
    if (results):
        print(results.groups())
        result = line_of_code.replace(results.groups()[0], '// '+' '.join(results.groups()[0].split()[1:]))
    return result

print(transform_comments("### Start of program")) 
# Should be "// Start of program"
print(transform_comments("  number = 0   ## Initialize the variable")) 
# Should be "  number = 0   // Initialize the variable"
print(transform_comments("  number += 1   # Increment the variable")) 
# Should be "  number += 1   // Increment the variable"
print(transform_comments("  return(number)")) 
# Should be "  return(number)"