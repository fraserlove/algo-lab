# Developed by Fraser Love on 09/05/20
# Solution to the coding challange at https://docs.google.com/document/d/1CQUj82NiB3l0KDiDV1fuTKWs2A7YNvAsHkacM-EjLBA/edit
# The main functions of this script is to create a string polynomial from coefficients passed in Poly() and to reconstruct a string
# polynomial from the polynomils roots PolyRoot(). The PolyRoot() function can accept all rational numbers and has methods for
# accepting strings to represent fractions 'a/b' and decimals with recurring digits 'a.b(c)' where the number c in parenthesis is
# the recurring digits. The program converts all of these string values into tuples (num, denom) to represent a fraction, where
# the numerator and denominator have no common factors.

from itertools import combinations
from functools import reduce

def Poly(terms):
    expr = ''
    orders = []
    pad = ''

    for i, term in enumerate(terms):
        sign = '-'
        if term > 0:
            sign = '+'
            if i == 0:
                sign = ''
        term = abs(term)

        order = ''
        exp = len(terms) - i - 1
        if exp > 0:
            order += 'x'
            if exp > 1:
                order += '^{}'.format(exp)
        orders.append(order)

        if term > 0:
            # If the current term is not the last term (constant) dont display the coefficient if it is 1.
            if i < len(terms) - 1 and term == 1:
                expr += '{}{}{}{}'.format(pad, sign, pad, orders[i])
            else:
                expr += '{}{}{}{}{}'.format(pad, sign, pad, term, orders[i])
        pad = ' '
    return expr + ' = 0'

def PolyRoot(roots):
    roots = RootsToTuples(roots)
    multiplier = 1
    for num, denom in roots:
        multiplier *= denom
    roots = MultiplyRoots(roots, multiplier)
    
    coefficients = [1 * multiplier]
    for i in range(1, len(roots) + 1):
        # Add up the products of all combinations of the terms to a speficifc order
        # i - speficifes the length of the combinations
        terms = list(combinations(roots, i))
        total = 0
        for term in terms:
            total += reduce(lambda x, y: x*y, term)
        if i % 2 != 0:
            total = -total
        coefficients.append(int(total / multiplier ** (i - 1)))
    return Poly(coefficients)

def GCD(num, denom):
    while denom:
        num, denom = denom, num % denom
    return num

def DecToFrac(decimal):
    if '.' not in decimal:
        return '{}/{}'.format(int(decimal), 1)
    before_pnt, after_pnt = decimal.split('.')
    is_recurr = False

    for i, char in enumerate(after_pnt):
        if char == '(':
            is_recurr = True
            no_recurr, recurr = after_pnt[:i], after_pnt[i+1:-1]
            decimal = float('0.{}{}'.format(no_recurr, recurr))
 
            mul_1 = decimal * 10 ** len(recurr + no_recurr)
            mul_2 = decimal * 10 ** len(no_recurr)
            for j in range(len(recurr + no_recurr)):
                mul_1 += float(recurr[j % len(recurr)]) * 10 ** -(j + 1)
            for j in range(len(recurr), len(recurr + no_recurr)):
                mul_2 += float(recurr[j % len(recurr)]) * 10 ** -(j + 1)
            num, denom = mul_1 - mul_2, 10 ** len(no_recurr) * (10 ** len(recurr) - 1)

            if before_pnt[0] == '-':
                num = -num
            num += int(before_pnt) * denom

    if not is_recurr:
        num = int(''.join([before_pnt, after_pnt]))
        denom = 10 ** len(after_pnt)

    return '{}/{}'.format(int(num), int(denom))

def FracToTuple(frac):
    num, denom = [int(n) for n in frac.split('/')]
    gcd = GCD(num, denom)
    return int(num / gcd), int(denom / gcd)

def MultiplyRoots(roots, multiplier):
    new_roots = []
    for num, denom in roots:
        if denom == multiplier:
            new_roots.append(num)
        else:
            new_roots.append(num / denom * multiplier)
    return new_roots

def RootsToTuples(roots):
    tuples = []
    for root in roots:
        if '/' in root:
            tuples.append(FracToTuple(root))
        else:
            tuples.append(FracToTuple(DecToFrac(root)))
    return tuples

# Examples
print(PolyRoot(['-3/2', '0']))
print(PolyRoot(['1.0(54)', '3/1']))
print(PolyRoot(['0.(8)', '-0.75', '-3/6', '-5', '4/2']))
print(PolyRoot(['-5.(9)', '114/19', '4.0', '-131/95', '0', '25/200', '-391/23']))