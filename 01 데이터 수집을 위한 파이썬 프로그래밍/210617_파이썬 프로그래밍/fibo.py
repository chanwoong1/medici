def fibo1(n) :
    a, b = 0, 1
    while b < n : 
        print(b, end = ' ')
        a, b = b, a+b
    print()



def fibo2(n) :
    result = []
    a, b = 0, 1
    while b < n :
        result.append(b)
        a, b = b, a+b
    return result