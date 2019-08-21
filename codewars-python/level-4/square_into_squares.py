#Kata URL: https://www.codewars.com/kata/54eb33e5bc1a25440d000891

def decompose(n):
    total = 0
    out = [n]
    while out:
        curr = out.pop()
        total += curr ** 2
        for i in range(curr-1,0,-1):
            if total - i ** 2 >= 0:
                total -= i ** 2
                out.append(i)
                if total == 0:
                    return sorted(out)
