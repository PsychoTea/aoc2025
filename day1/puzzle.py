
# ignore 
with open('input.txt', 'r') as f:
    l = f.read().split('\n')

# Solution for part 1 - 65 bytes  
c=50
z=0
for x in l:z+=(c:=(c+(x[0]=='R'or-1)*int(x[1:]))%100)==0

print(f"answer: {z}")

# Solution for part 2 - 74 bytes 
c=50
z=0
for x in l:
 c=(c%100)+int(x[1:])*(x[0]=='R'or-1)
 z+=abs(c//100)

# ignore
print(f"answer: {z}")

# part 1 answer = 1154
# part 2answer = 6819
