# -*- coding:utf-8 -*-

__author__ = 'koo'

BASE = 44032
CHOSUNG = 588
JUNGSUNG = 28

CHOSUNG_LIST = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
        'ㅅ', 'ㅆ', 'ㅇ' , 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

JUNGSUNG_LIST = [
        'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ',
        'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ',
        'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ',
        'ㅡ', 'ㅢ', 'ㅣ'
]

JONGSUNG_LIST = [
        ' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ',
        'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
        'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ',
        'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

DOUBLE_JONG_LIST = [
     'ㄳ', 'ㄵ', 'ㄶ',  'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
     'ㄿ', 'ㅀ', 'ㅄ'
]

def get_chosung(input):
    #input = input.decode('utf-8')
    index = (ord(input) - BASE) / CHOSUNG
    return CHOSUNG_LIST[index]

def get_jungsung(input):
    #input = input.decode('utf-8')
    index = ((ord(input) - BASE) % CHOSUNG) / JUNGSUNG
    return JUNGSUNG_LIST[index]

def get_jongsung(input):
    #input = input.decode('utf-8')
    index = ((ord(input) - BASE) % CHOSUNG) % JUNGSUNG
    return JONGSUNG_LIST[index]

def get_allsung(input):
    return get_chosung(input), get_jungsung(input), get_jongsung(input)

def get_cho_index(input):
    return CHOSUNG_LIST.index(input)

def get_jung_index(input):
    return JUNGSUNG_LIST.index(input)

def get_jong_index(input):
    return JONGSUNG_LIST.index(input)

# input: index of each list. output: unicode character assigned to inputs
def make_char(cho, jung, jong=' '):
    cho_index = get_cho_index(cho)
    jung_index = get_jung_index(jung)
    jong_index = get_jong_index(jong)

    return unichr(BASE + CHOSUNG*cho_index + JUNGSUNG*jung_index + jong_index)

def split_jong(jong):
    if jong == 'ㄳ':
        return 'ㄱ', 'ㅅ'
    elif jong == 'ㄵ':
        return 'ㄴ', 'ㅈ'
    elif jong == 'ㄶ':
        return 'ㄴ', 'ㅎ'
    elif jong == 'ㄺ':
        return 'ㄹ', 'ㄱ'
    elif jong == 'ㄻ':
        return 'ㄹ', 'ㅁ'
    elif jong == 'ㄼ':
        return 'ㄹ', 'ㅂ'
    elif jong == 'ㄽ':
        return 'ㄹ', 'ㅅ'
    elif jong == 'ㄾ':
        return 'ㄹ', 'ㅌ'
    elif jong == 'ㄿ':
        return 'ㄹ', 'ㅍ'
    elif jong == 'ㅀ':
        return 'ㄹ', 'ㅎ'
    elif jong == 'ㅄ':
        return 'ㅂ', 'ㅅ'

def merge_jong(f, s):
    if f == 'ㄱ' and s == 'ㅅ':
        return 'ㄳ'
    elif f == 'ㄴ' and s == 'ㅈ':
        return 'ㄵ'
    elif f == 'ㄴ' and s == 'ㅎ':
        return 'ㄶ'
    elif f == 'ㄹ' and s == 'ㄱ':
        return 'ㄺ'
    elif f == 'ㄹ' and s == 'ㅁ':
        return 'ㄻ'
    elif f == 'ㄹ' and s == 'ㅂ':
        return 'ㄼ'
    elif f == 'ㄹ' and s == 'ㅅ':
        return 'ㄽ'
    elif f == 'ㄹ' and s == 'ㅌ':
        return 'ㄾ'
    elif f == 'ㄹ' and s == 'ㅍ':
        return 'ㄿ'
    elif f == 'ㄹ' and s == 'ㅎ':
        return 'ㅀ'
    elif f == 'ㅂ' and s == 'ㅅ':
        return 'ㅄ'
    else:
        return '-1'