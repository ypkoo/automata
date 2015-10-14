# -*- coding:utf-8 -*-
#!/usr/bin/env python

# Korean automata. baatchim
__author__ = 'koo'

from mealy import *
from hangul import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class HangulAutomata(Mealy):

    def print_output(self, input_string):
        cur_state = self.init_state
        prev_str = ''

        for symbol in input_string:
            if(cur_state.trans(symbol)):
                symbol = symbol.decode('utf-8')
                prev_str = cur_state.output(prev_str, symbol)
                print prev_str
                symbol = symbol.encode('utf-8')
                cur_state = cur_state.trans(symbol)
            else:
                print 'wrong input.'

def construct_hangul_automata():

    vocabulary = [
        # consonants
        'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ',
        'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㄲ', 'ㄸ',
        'ㅃ', 'ㅆ', 'ㅉ',

        # vowels
        'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',
        'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ',

        # delete
        '-',
    ]

    consonants = [
        'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ',
        'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㄲ', 'ㄸ',
        'ㅃ', 'ㅆ', 'ㅉ',
    ]

    vowels = [
        'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',
        'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ',
    ]

    hangul = HangulAutomata('hangul')
    hangul.set_voca(vocabulary)

    # construct states
    init_state = hangul.add_state('initial')
    v = hangul.add_state('v')
    o = hangul.add_state('o')
    u = hangul.add_state('u')
    a = hangul.add_state('a')
    i = hangul.add_state('i')
    k = hangul.add_state('k')
    n = hangul.add_state('n')
    r = hangul.add_state('r')
    l = hangul.add_state('l')

    # set initial state and final states
    hangul.set_init_state(init_state)
    hangul.add_final_state(init_state)
    hangul.add_final_state(o)
    hangul.add_final_state(u)
    hangul.add_final_state(a)
    hangul.add_final_state(i)
    hangul.add_final_state(k)
    hangul.add_final_state(n)
    hangul.add_final_state(r)
    hangul.add_final_state(l)

    ### start setting transition function ###
    # set transition function of initial state
    for c in consonants:
        init_state.set_trans_func(c, v)

    # set transition function of v
    v.set_trans_func('ㅗ', o)
    v.set_trans_func('ㅜ', u)
    for vowel in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅡ']:
        v.set_trans_func(vowel, a)
    for vowel in ['ㅛ', 'ㅠ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ']:
        v.set_trans_func(vowel, i)

    # set transition function of o
    o.set_trans_func('ㄱ', k)
    o.set_trans_func('ㅂ', k)
    o.set_trans_func('ㄴ', n)
    o.set_trans_func('ㄹ', r)
    for c in ['ㄷ', 'ㅁ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㄲ', 'ㅆ']:
        o.set_trans_func(c, l)
    for c in ['ㄸ', 'ㅃ', 'ㅉ']:
        o.set_trans_func(c, v)

    o.set_trans_func('ㅏ', a)
    o.set_trans_func('ㅐ', a)
    o.set_trans_func('ㅣ', i)

    # set transition function of u
    u.set_trans_func('ㄱ', k)
    u.set_trans_func('ㅂ', k)
    u.set_trans_func('ㄴ', n)
    u.set_trans_func('ㄹ', r)
    for c in ['ㄷ', 'ㅁ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㄲ', 'ㅆ']:
        u.set_trans_func(c, l)
    for c in ['ㄸ', 'ㅃ', 'ㅉ']:
        u.set_trans_func(c, v)

    u.set_trans_func('ㅓ', a)
    u.set_trans_func('ㅔ', a)
    u.set_trans_func('ㅣ', i)

    # set transition function of a
    a.set_trans_func('ㄱ', k)
    a.set_trans_func('ㅂ', k)
    a.set_trans_func('ㄴ', n)
    a.set_trans_func('ㄹ', r)
    for c in ['ㄷ', 'ㅁ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㄲ', 'ㅆ']:
        a.set_trans_func(c, l)
    for c in ['ㄸ', 'ㅃ', 'ㅉ']:
        a.set_trans_func(c, v)

    a.set_trans_func('ㅣ', i)

    # set transition function of i
    i.set_trans_func('ㄱ', k)
    i.set_trans_func('ㅂ', k)
    i.set_trans_func('ㄴ', n)
    i.set_trans_func('ㄹ', r)
    for c in ['ㄷ', 'ㅁ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㄲ', 'ㅆ']:
        i.set_trans_func(c, l)
    for c in ['ㄸ', 'ㅃ', 'ㅉ']:
        i.set_trans_func(c, v)

    # set transition function of k, n, r, l for vowel input
    for state in [k, n, r, l]:
        state.set_trans_func('ㅗ', o)
        state.set_trans_func('ㅜ', u)
        for vowel in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅡ']:
            state.set_trans_func(vowel, a)
        for vowel in ['ㅛ', 'ㅠ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ']:
            state.set_trans_func(vowel, i)

    # set transition function of k
    k.set_trans_func('ㅅ', l)
    for c in list(set(consonants) - {'ㅅ'}):
        k.set_trans_func(c, v)

    # set transition function of n
    n.set_trans_func('ㅈ', l)
    n.set_trans_func('ㅎ', l)
    for c in list(set(consonants) - {'ㅈ', 'ㅎ'}):
        n.set_trans_func(c, v)

    # set transition function of r
    for c in ['ㄱ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅌ', 'ㅍ', 'ㅎ']:
        r.set_trans_func(c, l)
    for c in list(set(consonants) - {'ㄱ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅌ', 'ㅍ', 'ㅎ'}):
        r.set_trans_func(c, v)

    # set transition function of l
    for c in consonants:
        l.set_trans_func(c, v)

    # set transition function of input '-'
    for state in hangul.get_all_states():
        state.set_trans_func('-', init_state)
    ### setting transition function over ###


    ### start setting output function ###
    # set output function of initial state
    def output_init_state(prev_str, input):
        if input == '-':
            if len(prev_str) == 0:
                return ''
            elif len(prev_str) > 0:
                return prev_str[0:-1]
        else:
            return prev_str + input

    init_state.output = output_init_state

    # set output function of state v
    def output_v(prev_str, input):
        if input == '-':
            return prev_str[0:-1]

        if len(prev_str) is 1:
            last_char = prev_str
        elif len(prev_str) > 1:
            last_char = prev_str[-1]

        if last_char in consonants: # last character is a consonant (initial input)
            return prev_str[0:-1] + make_char(last_char, input)
        else: # last character is a letter (cho + jung + jong)
            cho, jung, jong = get_allsung(last_char)

            if jong in DOUBLE_JONG_LIST:
                first, second = split_jong(jong)
                return prev_str[0:-1] + make_char(cho, jung, first) + make_char(second, input)


    v.output = output_v

    # set output function of state o
    def output_o(prev_str, input):
        if input == '-':
            return prev_str[0:-1]

        last_char = prev_str[-1]
        cho, jung, jong = get_allsung(last_char)

        if input in list(set(consonants) - {'ㄸ', 'ㅃ', 'ㅉ'}):
            return prev_str[0:-1] + make_char(cho, jung, input)
        elif input in ['ㄸ', 'ㅃ', 'ㅉ']:
            return prev_str + input
        elif input == 'ㅣ':
            return prev_str[0:-1] + make_char(cho, 'ㅚ')
        elif input == 'ㅏ':
            return prev_str[0:-1] + make_char(cho, 'ㅘ')
        elif input == 'ㅐ':
            return prev_str[0:-1] + make_char(cho, 'ㅙ')

    o.output = output_o

    # set output function of state u
    def output_u(prev_str, input):
        if input == '-':
            return prev_str[0:-1]

        last_char = prev_str[-1]
        cho, jung, jong = get_allsung(last_char)

        if input in list(set(consonants) - {'ㄸ', 'ㅃ', 'ㅉ'}):
            return prev_str[0:-1] + make_char(cho, jung, input)
        elif input in ['ㄸ', 'ㅃ', 'ㅉ']:
            return prev_str + input
        elif input == 'ㅣ':
            return prev_str[0:-1] + make_char(cho, 'ㅟ')
        elif input == 'ㅓ':
            return prev_str[0:-1] + make_char(cho, 'ㅝ')
        elif input == 'ㅔ':
            return prev_str[0:-1] + make_char(cho, 'ㅞ')

    u.output = output_u

    # set output function of a
    def output_a(prev_str, input):
        if input == '-':
            return prev_str[0:-1]

        last_char = prev_str[-1]
        cho, jung, jong = get_allsung(last_char)

        if input in list(set(consonants) - {'ㄸ', 'ㅃ', 'ㅉ'}):
            return prev_str[0:-1] + make_char(cho, jung, input)
        elif input in ['ㄸ', 'ㅃ', 'ㅉ']:
            return prev_str + input
        elif input == 'ㅣ':
            if jung == 'ㅏ':
                return prev_str[0:-1] + make_char(cho, 'ㅐ')
            elif jung == 'ㅑ':
                return prev_str[0:-1] + make_char(cho, 'ㅒ')
            elif jung == 'ㅓ':
                return prev_str[0:-1] + make_char(cho, 'ㅔ')
            elif jung == 'ㅕ':
                return prev_str[0:-1] + make_char(cho, 'ㅖ')
            elif jung == 'ㅡ':
                return prev_str[0:-1] + make_char(cho, 'ㅢ')
            elif jung == 'ㅘ':
                return prev_str[0:-1] + make_char(cho, 'ㅙ')
            elif jung == 'ㅝ':
                return prev_str[0:-1] + make_char(cho, 'ㅞ')

    a.output = output_a

    # set output function of i
    def output_i(prev_str, input):
        if input == '-':
            return prev_str[0:-1]

        last_char = prev_str[-1]
        cho, jung, jong = get_allsung(last_char)

        if input in list(set(consonants) - {'ㄸ', 'ㅃ', 'ㅉ'}):
            return prev_str[0:-1] + make_char(cho, jung, input)
        elif input in ['ㄸ', 'ㅃ', 'ㅉ']:
            return prev_str + input

    i.output = output_i

    # set output function of k
    def output_k(prev_str, input):
        if input == '-':
            return prev_str[0:-1]

        last_char = prev_str[-1]
        cho, jung, jong = get_allsung(last_char)

        if input in vowels:
            return prev_str[0:-1] + make_char(cho, jung) + make_char(jong, input)
        elif input in list(set(consonants) - {'ㅅ'}):
            return prev_str + input
        elif input == 'ㅅ':
            jong = merge_jong(jong, input)
            return prev_str[0:-1] + make_char(cho, jung, jong)

    k.output = output_k

    # set output function of n
    def output_n(prev_str, input):
        if input == '-':
            return prev_str[0:-1]

        last_char = prev_str[-1]
        cho, jung, jong = get_allsung(last_char)

        if input in vowels:
            return prev_str[0:-1] + make_char(cho, jung) + make_char(jong, input)
        elif input in list(set(consonants) - {'ㅈ', 'ㅎ'}):
            return prev_str + input
        elif input in ['ㅈ', 'ㅎ']:
            jong = merge_jong(jong, input)
            return prev_str[0:-1] + make_char(cho, jung, jong)

    n.output = output_n

    # set output function of r
    def output_r(prev_str, input):
        if input == '-':
            return prev_str[0:-1]

        last_char = prev_str[-1]
        cho, jung, jong = get_allsung(last_char)

        if input in vowels:
            return prev_str[0:-1] + make_char(cho, jung) + make_char(jong, input)
        elif input in list(set(consonants) - {'ㄱ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅌ', 'ㅍ', 'ㅎ'}):
            return prev_str + input
        elif input in ['ㄱ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅌ', 'ㅍ', 'ㅎ']:
            jong = merge_jong(jong, input)
            return prev_str[0:-1] + make_char(cho, jung, jong)

    r.output = output_r

    # set output function of l
    def output_l(prev_str, input):
        if input == '-':
            return prev_str[0:-1]

        last_char = prev_str[-1]
        cho, jung, jong = get_allsung(last_char)

        if input in consonants:
            return prev_str + input
        elif input in vowels:
            if jong in DOUBLE_JONG_LIST:
                first, second = split_jong(jong)
                return prev_str[0:-1] + make_char(cho, jung, first) + make_char(second, input)
            else:
                return prev_str[:-1] + make_char(cho, jung) + make_char(jong, input)

    l.output = output_l
    ### setting output function if over ###

    return hangul


if __name__ == "__main__":
    hangul = construct_hangul_automata()

    while True:
        input_string = raw_input('Enter input string. (seperated by space)')
        input_string = input_string.split()
        if(hangul.is_acceptable(input_string)):
            hangul.print_output(input_string)
        else:
            print 'Input string is not hangul. Please try again.'







