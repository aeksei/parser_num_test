from num_dict import nums


def get_num(word_num):
    common_num = 0
    rank = 1

    local_num = 0
    for word in word_num:
        local_num += nums[word]

    local_num *= rank

    common_num += local_num

    return common_num


def test_999():
    with open('numbers_0_999.txt', 'r') as f:
        for line in f:
            word_num = line[:-1].split(',')
            num = get_num(word_num[1].split(' '))
            if int(word_num[0]) != num:
                raise ValueError('{} != {}'.format(num, word_num[1]))


if __name__ == '__main__':
    test_999()