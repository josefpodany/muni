''' simplex calculation '''


'''
header  x1  x2  x3  ... xn  01  02  03  ... 0n  result
row_1   r11 r12 r13 ... r1n 1   0   0   ... 0   restriction_1
row_2   r21 r22 r23 ... r2n 0   1   0   ... 0   restricion_2
row_n   rn1 rn2 rn3 ... rnn 0   0   0   ... 1   restriction_n
'''


def simplex_method(func, restr):
    '''
    Calculates optimal result with regards to restrictions
    :param func: list of variables of maximaliazation function
    :param restr: 2D list of restrictions of variables without slack 
    variables
    :return: tuple with solved coefficients and optimal maximum value of 
    function

    example:
    func: [3, 1, 2, 2]
    restrictions: [[1, 2, 0, 0, 300], [2, 3, 1, 1, 500]]
    '''
    if all([len(i) == len(func) + 1 for i in restr]):
        function = [-i for i in func]
        restrictions = [row[:] for row in restr]
        # Create slack variables in header
        function += (len(restrictions) + 1) * [0]
        # Create slack variables in the restrictions
        for i in range(len(restrictions)):
            total = restrictions[i].pop()
            for j in range(len(restrictions[i])):
                restrictions[i] += [1] if j == i else [0]
            restrictions[i].append(total)
    else:
        raise ValueError("Restrictions of simplex method do not have larger\
 amount of variables than maximaliazation function by one")


if __name__ == "__main__":
    simplex_method([1, 2], [[1, 2, 3], [1, 2, 3]])
