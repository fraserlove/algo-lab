#Kata URL: https://www.codewars.com/kata/56747fd5cb988479af000028

def get_middle(s):
    lst = list(s)
    if len(lst)%2 == 1:
        side = (len(lst)-1)/2
        del lst[len(lst) - side:]
        del lst[:side - len(lst)]
    else:
        side = (len(lst)-2)/2
        del lst[len(lst) - side:]
        del lst[:side - len(lst)]
    return ''.join(lst)
