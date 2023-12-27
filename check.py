def check_key(key: str):
    for i, k in enumerate(key.split('-')):
        number = int(k, 16)

        if i == 0: 
            if int(str(number)[3]) != 3:
                return False
        if i == 1: 
            if (int(str(number)[1]) * int(str(number)[0])) % 6 != 0:
                return False
        if i == 2:
            if (int(str(number)[1]) * int(str(number)[3])) % 9 != 0:
                return False        
    return True  
