a = int(input("first number: "))
b = int(input("second number: "))
c = int(input("third number: "))


def check(a, b, c):

    if a > b and a > c:
        return f"{a} is the biggest!"
    if b > a and b > c:
        return f"{b} is the biggest!"
    else:
        return f"{c} is the biggest"


spr = check(a, b, c)
print(spr)
