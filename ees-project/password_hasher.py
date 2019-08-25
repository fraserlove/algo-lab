from passlib.hash import pbkdf2_sha256

string = input("What do you want to hash: ")
hash = pbkdf2_sha256.hash(string)
print(hash)
