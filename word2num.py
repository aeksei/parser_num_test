from num_dict import nums, rank


def get_numr(lemma):
    local_num = 0
    global_num = 0
    global_level = None
    local_level = None
    last_global_level = False
    for word in lemma:
        if word in rank:
            if (global_level is not None) and (global_level < rank[word][1]):
                if not last_global_level:
                    raise ValueError('global_level < {}'.format(rank[word][1]))
            global_level = rank[word][1]
            if local_num == 0:
                if last_global_level:
                    global_num *= rank[word][0]
                else:
                    global_num += rank[word][0]
            else:
                global_num += local_num * rank[word][0]
            local_num = 0
            local_level = None
            last_global_level = True

        if word in nums:
            if (local_level is not None) and (local_level < nums[word][1]):
                raise ValueError('local_level < {}'.format(nums[word][1]))
            local_level = nums[word][1]
            local_num += nums[word][0]
            last_global_level = False

    global_num += local_num

    return global_num


def get_numb(lemma):
    num = float(lemma.pop(0))
    for r in rank:
        if r in lemma:
            num *= rank[r][0]
            break
    return int(num)


def test_999():
    with open('numbers_0_999.txt', 'r') as f:
        for line in f:
            word_num = line[:-1].split(',')
            num = get_numr(parser.get_lemma(word_num[1]))
            if int(word_num[0]) != num:
                raise ValueError('{} != {}'.format(num, word_num[1]))


def test_1000_999999():
    with open('numbers_1000_999999.txt', 'r') as f:
        for line in f:
            word_num = line[:-1].split(',')
            num = get_numr(parser.get_lemma(word_num[1]))
            if int(word_num[0]) != num:
                raise ValueError('{} != {}'.format(num, word_num[1]))
            else:
                print('{} = {}'.format(num, word_num[1]))


def test_1000000_999999999():
    with open('numbers_1000000_999999999.txt', 'r') as f:
        for line in f:
            word_num = line[:-1].split(',')
            num = get_numr(parser.get_lemma(word_num[1]))
            if int(word_num[0]) != num:
                raise ValueError('{} != {}'.format(num, word_num[1]))
            else:
                print('{} = {}'.format(num, word_num[1]))


if __name__ == '__main__':
    from parser import NumParser

    parser = NumParser()
    
    test_999()
    test_1000_999999()
    test_1000000_999999999()
