# lab 4 part 1
# verifying logic strings are parsable by nltk's fromstring

import nltk

read_expr = nltk.sem.Expression.fromstring

# 8.1.1
# AS = "Angus sings", BS = "Bertie sulks"
read_expr('AS -> -BS')

# 8.1.2
# CR = “Cryil runs” and CB = “Cyril barks”
read_expr('CR & CB')

# 8.1.3
# R = "rain", IWS = "it will snow"
read_expr('-R -> IWS')

# 8.1.4
# IH = “Irene will be happy” and OC = “Olive comes” and TC = “Tofu comes”
read_expr('-((OC | TC) -> IH)')

# 8.1.5
# PC = "Pat coughed", PS = "Pat sneezed"
# Pat didn't cough or Pat didn't sneeze
read_expr('-(PC | PS)')

# 8.1.6
# YDC = “you don’t come” and IC = “I call” and IWC = “I won’t come” and YC = “you call"
read_expr('(IC -> YDC) -> (YC -> IWC)')

# 8.2.1
read_expr('likes(Angus, Cyril) & hates(Irene, Cyril)')

# 8.2.2
read_expr('Taller(Tofu,Bernie)')

# 8.2.3
read_expr('loves(Bruce, Bruce) & loves(Pat, Pat)')
read_expr('loves(Bruce, Bruce) & loves(Pat, Bruce)')

# 8.2.4
read_expr('saw(Cyril, Bertie) & (-saw(Angus, Bertie))')

# 8.2.5
read_expr('fourLeggedFriend(Cyril)')

# 8.2.6
read_expr('near(Tofu, Olive) & near(Olive, Tofu)')

# 8.3.1
read_expr('exists x.(likes(Angus, x) & likes(x, Julia))')

# 8.3.2
read_expr('exists x.og(x) & loves(Angus, x) & love(x, Angus)')

# 8.3.3
read_expr('all x.(-smilesAt(x, Pat))')

# 8.3.4
read_expr('exists x.(coughes(x) & sneezes(x))')

# 8.3.5
read_expr('-(exists x.(coughed(x) | sneezed(x)))')

# 8.3.6
read_expr('exists x.(loves(Bruce, x) & -Same(x, Bruce))')

# 8.3.7
read_expr('all x.(love(x, Pat) -> Same(x, Matthew))')

#8.3.8
read_expr('all x.(Likes(Cyril, Same(x, Irene)))')

#8.3.9
read_expr('exists x.(asleep(x) & (exists y.(asleep(y) -> Same(x, y))))')
