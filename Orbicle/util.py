#!/usr/local/bin/python3.7

from math import fabs

from params import *

def adjacent_pairs(lst):
    list2 = list(lst)
    list2.append(list2.pop(0))
    return zip(lst, list2)

def eps(x):
    return 0.0 if (fabs(x) < epsilon_threshold) else x

def main():
    print('Hello, world!')
    lst = [1,2,3,4,5]
    aps = adjacent_pairs(lst)
    for ap in aps:
        print(ap)

if __name__ == '__main__':
    main()
