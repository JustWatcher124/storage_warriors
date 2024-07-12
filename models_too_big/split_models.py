from itertools import chain, islice


def chunks(iterable, n):
    "chunks(ABCDE,2) => AB CD E"
    iterable = iter(iterable)
    while True:
        yield chain([next(iterable)], islice(iterable, n-1))


l = ...
file_large = './134ada83d8a5174517af03a187ce205521d58157ce78bd94b5ab4a4d9c9a779b.pkl'
with open(file_large, 'rb') as bigfile:
    for i, lines in enumerate(chunks(bigfile, l)):
        file_split = '{}.{}'.format(file_large, i)
        with open(file_split, 'wb') as f:
            f.write(lines)
