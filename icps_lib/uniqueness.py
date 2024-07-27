from random import randint

alphanumerics = [
        [chr(x) for x in range(ord('a'), ord('z')+1)],
        [chr(x) for x in range(ord('A'), ord('Z')+1)],
        [str(x) for x in range(1,10)]
    ]

alphanums = alphanumerics[0]+alphanumerics[1]+alphanumerics[2]+['0']

def unique_key(length):

    code=""
    for i in range(length):
        x = alphanumerics[randint(0, len(alphanumerics)-1)]
        c = x[randint(0,len(x)-1)]
        code+=c

    return code
