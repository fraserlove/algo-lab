#Kata URL: https://www.codewars.com/kata/563f037412e5ada593000114

def calculate_years(principal, interest, tax, desired):
    i = 0
    total = 0
    sub_total = 0
    last_no = principal
    if principal == desired:
        return 0
    while total < desired:
        sub_total = last_no * (interest + 1)
        print(sub_total)
        taxable = sub_total - last_no
        dividends = taxable * (1 - tax)
        total = last_no + dividends
        last_no = total
        print(total)
        i += 1
    return i
