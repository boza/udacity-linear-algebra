from line import Line

line1 = Line([7.204, 3.182], constant_term=8.68)
line2 = Line([8.172, 4.114], constant_term=9.883)

print(line1.isparallel(line2))
print(line1 == line2)
print(line1.intersection(line2))
