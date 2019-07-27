from num_dict import nums, rank
from parser import NumParser

parser = NumParser()


def get_num(word_num):
    local_num = 0
    global_num = 0
    global_level = None
    local_level = None
    for word in word_num:
        if word in rank:
            if (global_level is not None) and (global_level < nums[word][1]):
                raise ValueError('global_level < {}'.format(nums[word][1]))
            global_level = rank[word][1]
            if local_num == 0:
                global_num += rank[word][0]
            else:
                global_num += local_num * rank[word][0]
            local_num = 0
            local_level = None

        if word in nums:
            if (local_level is not None) and (local_level < nums[word][1]):
                raise ValueError('local_level < {}'.format(nums[word][1]))
            local_level = nums[word][1]
            local_num += nums[word][0]

    global_num += local_num
    return global_num


def test_999():
    with open('numbers_0_999.txt', 'r') as f:
        for line in f:
            word_num = line[:-1].split(',')
            num = get_num(parser.get_lemma(word_num[1]))
            if int(word_num[0]) != num:
                raise ValueError('{} != {}'.format(num, word_num[1]))


def test_1000_999999():
    with open('numbers_1000_999999.txt', 'r') as f:
        for line in f:
            word_num = line[:-1].split(',')
            num = get_num(parser.get_lemma(word_num[1]))
            if int(word_num[0]) != num:
                raise ValueError('{} != {}'.format(num, word_num[1]))
            else:
                print('{} = {}'.format(num, word_num[1]))


if __name__ == '__main__':
    # test_999()
    test_1000_999999()
