# -*- coding: utf-8 -*-

def compare(a, b):
    return True if a > b else False

f = compare
print f(1,2)


def partition(low, high, l):
    temp = l[low]
    i = low
    j = high
    while (i < j):
        while (j > low and l[j] >= temp):
            j -= 1
        if i < j:    
            l[i] = l[j]
            i += 1
        while (i < high and l[i] <= temp):
            i += 1
        if i < j:
            l[j] = l[i]
            j -= 1
    l[i] = temp
    return i

def quck_sort(comparator, low, high, l):
    # 一定要加此限定
    if low < high:
        temp = l[low]
        i = low
        j = high
        while (i < j):
            while (j > low and l[j] >= temp):
                j -= 1
            if i < j:    
                l[i] = l[j]
                i += 1
            while (i < high and l[i] <= temp):
                i += 1
            if i < j:
                l[j] = l[i]
                j -= 1
        l[i] = temp

        print i, l[i]
        quck_sort(comparator, low, i-1, l)
        quck_sort(comparator, i+1, high, l)
    
    return l

l = [9,4,6,3,5,7]

print quck_sort(compare, 0, 5, l)