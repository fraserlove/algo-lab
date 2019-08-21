#Kata URL: https://www.codewars.com/kata/514a024011ea4fb54200004b/solutions/python/all/newest

def domain_name(url):
    url = url.strip("https://www.")
    if "/" in url:
        url = url.split("/")
        url = url[0]
    if "." in url:
        url = url.split(".")
        url = url[0]
    return url
