__author__ = 'peter'

the_world_is_flat = True
if the_world_is_flat:
    print("Be Careful you don't fall off")

squares = [1,4,9,16,25]

print(squares[1])
print(squares[-3])

squares.append(50)
print(squares[5])

a, b = 0, 1
while b < 10:
    print(b)
    a, b = b, a+b


words = ['cat','window','defense']
for i in words:
    print(i, len(i))

for x in words[:]:
    if len(x) > 5:
        words.insert(0, x)

for i in range(5):
    print(i)


a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])

print(list(a))

for n in range(2, 10):
    for x in range(2,n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        print(n, 'is a prime number')



