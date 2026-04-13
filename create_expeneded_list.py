with open('usernames.txt','r') as l:
    username = l.read().splitlines()

with open('expended_list.txt', 'w') as l:
    for name in username:
        for _ in range(5):
            l.write(name + '\n')

print(l)
        