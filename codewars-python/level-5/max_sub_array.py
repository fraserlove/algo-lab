#Kata URL: https://www.codewars.com/kata/54521e9ec8e60bc4de000d6c

def maxSequence(arr):
  best = 0
  for i in range(0,len(arr)-3):
    c = sum = 0
    while sum + arr[i] + arr[i+1] > sum and i+c < len(arr):
      sum += arr[i+c]
      c += 1
      if sum > best: best = sum
  return best
