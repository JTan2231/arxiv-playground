with open('response.txt', 'r') as f:
    contents = f.read()

lines = [l for l in contents.split('\n') if len(l) > 0]

titles = [t[2:] for t in lines if t[0] != ' ']
abstracts = [a[4:] for a in lines if a[0] == ' ']

assert(len(titles) == len(abstracts))
for t, a in zip(titles, abstracts):
    pass
