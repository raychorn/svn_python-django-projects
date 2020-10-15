def foo(number):
    if number > 11: 
        print(0)
    elif number != 10:
        print(1)
    elif number >= 20 or number < 12:
        print(2)
    else:
        print(3)
        
foo(10)

def sum(x, y):
    return(x+y)
print(sum(sum(1,2), sum(3,4)))