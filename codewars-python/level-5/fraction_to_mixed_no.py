#Kata URL: https://www.codewars.com/kata/556b85b433fb5e899200003f

def mixed_fraction(s):
    num = int(s.split("/")[0])
    den = int(s.split("/")[-1])
    whole = int(float(num)/float(den))
    if num < 0 and den < 0:
        num = abs(num)
        den = abs(den)
    if den < 0 and num > 0:
        den = abs(den)
        num = -num
    if num%den == 0:
        return(str(num/den))
    frac = num - whole * den
    common_factor = 1
    for i in xrange(min(abs(num), abs(den)), 1, -1):
        if num % i == 0 and den % i == 0:
             common_factor = i
             break
    if whole == 0:
        print(str(num/common_factor) + "/" + str(den/common_factor))
        return(str(num/common_factor) + "/" + str(den/common_factor))
    if whole < 0 and num < 0:
        num = abs(num)
        print(str(whole) + " " + str(-frac/common_factor) + "/" + str(den/common_factor))
        return(str(whole) + " " + str(-frac/common_factor) + "/" + str(den/common_factor))
    if num/den < 1 and num/den >= 0:
        print(str(num/common_factor) + "/" + str(den/common_factor))
        return(str(num/common_factor) + "/" + str(den/common_factor))
    else:
        print(str(whole) + " " + str(frac/common_factor) + "/" + str(den/common_factor))
        return(str(whole) + " " + str(frac/common_factor) + "/" + str(den/common_factor))

fraction = input(str("Type in the fraction you want to convert: "))
mixed_fraction(fraction)
