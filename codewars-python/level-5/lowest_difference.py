#Kata URL: https://www.codewars.com/kata/58b38256e51f1c2af0000081

def best_match(goals1, goals2):
  best = -999999
  for i in range(0,len(goals1)):
      diff = goals2[i] - goals1[i]
      if diff > best or (diff == best and goals2[i] > most_goals):
          best = diff
          out = i
          most_goals = goals2[i]
  return out
