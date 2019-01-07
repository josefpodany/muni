''' simplex calculation '''


'''
header  x1  x2  x3  ... xn  01  02  03  ... 0n  result
row_1   r11 r12 r13 ... r1n 1   0   0   ... 0   restriction_1
row_2   r21 r22 r23 ... r2n 0   1   0   ... 0   restricion_2
row_n   rn1 rn2 rn3 ... rnn 0   0   0   ... 1   restriction_n
'''


def simplex(func, restricitons):
    '''
    Calculates optimal result with regards to restrictions
    :param func: list of variables of maximaliazation function
    :param restrictions: list of restrictions of variables without slack variables
    :return: tuple with solved coefficients and optimal maximum value of function
    '''
    pass
