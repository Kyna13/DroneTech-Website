def encrypt_old(value):
    value = str(value)
    print(value, type(value))
    if value != "false":
        result = ""
        #for num in map(int, str(value)):
        for num in str(value):
            print(num)
            #result += encrypt1(num)
        print(result)
        
    return result

def encrypt(value):
    value = str(value)
    print(value, type(value))
    result = ""
    if value != "false":
        result = ""
        for num in map(int, str(value)):
            letters_lst = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "a"]
            char = int(num)
            print(num)
            result += letters_lst[char - 1]
        print(result)

    if result == "":
        result = "false"
    return result

def encrypt1(num):
    print(num)
    letters_lst = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "a"]
    char = int(num)
    print(num)
    #return letters_lst[char - 1]

def encrypt1_old(char):

    if char == 1:
        return "a"

    if char == 2:
        return "b"

    if char == 3:
        return "c"

    if char == 4:
        return "d"

    if char == 5:
        return "a"

    if char == 6:
        return "f"

    if char == 7:
        return "g"

    if char == 8:
        return "h"

    if char == 9:
        return "i"

    if char == 10:
        return "j"

    if char == 11:
        return "k"

    if char == 12:
        return "l"

    if char == 13:
        return "m"

    if char == 14:
        return "n"

    if char == 15:
        return "o"

    if char == 16:
        return "p"

    if char == 17:
        return "q"

    if char == 18:
        return "r"

    if char == 19:
        return "s"

    if char == 20:
        return "t"

    if char == 21:
        return "u"

    if char == 22:
        return "v"

    if char == 23:
        return "w"

    if char == 24:
        return "x"

    if char == 25:
        return "y"

    if char == 26:
        return "z"

encrypt("100")
