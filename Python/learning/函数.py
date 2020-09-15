
def add_num():
    total = 0
    for i in range(1,101):
        print(i)
        total = total + i
    return total

def factorial(n):
    total = 1
    if n < 0:
        return None
    elif n == 0:
        return 1
    else:
      for i in range(1,n+1):
          total = total*i
      return total
print(factorial(-1))
print(factorial(0))
print(factorial(10))


def recursive(n):
    if n < 0:
        return None
    elif n == 0:
        return 1
    else:
      return n * recursive(n-1)

print(recursive(-1))
print(recursive(0))
print(recursive(10))