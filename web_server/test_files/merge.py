def mergeJoin(invertedIndex, terms):
    if len(terms) == 0:
        return []
    else:
        return mergeJoinHelper(invertedIndex, terms[0], terms[1:])
            
def mergeJoinHelper(invertedIndex, first, rest):
    if len(rest) == 0:
        output = []
        for x in invertedIndex[first]:
            output.append(x[0])
        return output
    else:
        rest_output = mergeJoinHelper(invertedIndex, rest[0], rest[1:])
        # now we join first to rest
        i = 0
        j = 0
        output = list()
        while (i < len(invertedIndex[first]) and j < len(rest_output)):
            print invertedIndex[first][i][0], rest_output[j]
            if invertedIndex[first][i][0] == rest_output[j]:
                output.append(invertedIndex[first][i][0])
                i += 1
                j += 1
            elif invertedIndex[first][i][0] < rest_output[j]:
                i += 1
            else:
                j += 1
        return output
    

if __name__ == '__main__':
    index = dict()
    index['data'] = [(0, 12), (2, 12), (5, 12), (7, 12), (9, 12)]
    index['big']  = [(0, 12), (1, 12), (2, 12), (3, 12), (5, 12)]
    index['vis']  = [(1, 12), (9, 12), (11, 12)]
    index['rdma'] = [(2, 12), (3, 12), (5, 12), (9, 12), (10, 12)]
    index['machine'] = [(6, 12), (8, 12)]
    index['empty'] = []
    
    out = mergeJoin(index, ['data', 'big', 'empty', 'rdma'])
    print out