import re
from collections import Counter

with open('input.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# re es un módulo que proporciona operaciones de coincidencia de expresiones regulares similares
# findall() return all non-overlapping matches of pattern in string, as a list of strings or tuples.
dic = re.findall(r'[a-z]+', text.lower())

# Una clase Counter es una subclase dict para contar objetos hashables.
c = Counter(dic)
n = 1

print('Word --- Frequency')
print('-------------------')

# most_common() Retorna una lista de los n elementos mas comunes y sus conteos, del mas común al menos común.
for word, frec in c.most_common(10):
    print(f'{n}) {word} --- {frec}')
    n += 1