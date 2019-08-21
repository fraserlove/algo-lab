#Kata URL: https://www.codewars.com/kata/caesar-cipher-helper/python

class CaesarCipher(object):
    def __init__(self, shift):
        self.shift = shift
        self.alpha = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    def encode(self, str):
        encode = []
        for i in str:
            i = i.upper()
            if i not in self.alpha:
                encode.append(i)
            else:
                for j in range(0,self.shift):
                    if self.alpha.index(i) < 25:
                        i = self.alpha[self.alpha.index(i)+1]
                    else:   
                        i = self.alpha[0]
                encode.append(i)
        return("".join(encode))
        
    def decode(self, str):
        decode = []
        for i in str:
            i = i.upper()
            if i not in self.alpha:
                decode.append(i)
            else:
                for j in range(0,self.shift):
                    if self.alpha.index(i) > 0:
                        i = self.alpha[self.alpha.index(i)-1]
                    else:   
                        i = self.alpha[25]
                decode.append(i)
        return("".join(decode))
