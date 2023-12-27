import random


def generator():
    key = [10000, 21400, 32450]

    while int(str(key[0])[3]) != 3:
        key[0] = random.randint(15000, 20000)

    while (int(str(key[1])[1]) * int(str(key[1])[0])) % 6 != 0:
        key[1] = random.randint(1000, 9000)

    while (int(str(key[2])[1]) * int(str(key[2])[3])) % 9 != 0:
        key[2] = random.randint(50000, 100000)
    
    print(key) 
    res = ''
    for i in key:
        res += str(hex(i))[2:] + '-'
    return res[0:-1]    
