st = input().split()
i = len(st)
stg = ""
while i > 0:
    i = i - 1
    stg = stg + st[i] + " "
stg = stg.strip()  
print(stg)
