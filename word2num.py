from num_dict import nums, rank, ordinal


def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


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

        elif word in nums:
            if (local_level is not None) and (local_level < nums[word][1]):
                raise ValueError('local_level < {}'.format(nums[word][1]))
            local_level = nums[word][1]
            local_num += nums[word][0]
            last_global_level = False

        elif word in ordinal:
            if (local_level is not None) and (local_level < ordinal[word][1]):
                raise ValueError('local_level < {}'.format(nums[word][1]))
            local_level = ordinal[word][1]
            local_num += ordinal[word][0]
            last_global_level = False

    global_num += local_num

    if global_num == 0:
        return None

    return int(global_num)


def get_numb(lemma):
    local_num = 0
    global_num = 0
    global_level = 1
    for word in lemma:
        if word in rank:
            if (global_level is not None) and (global_level < rank[word][1]):
                raise ValueError('global_level < {}'.format(rank[word][1]))
            global_level = rank[word][1]
            global_num += local_num * rank[word][0]
            local_num = 0

        elif is_digit(word):
            local_num *= global_level
            local_num += float(word)
            global_level *= 1000

    return int(global_num + local_num)


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
