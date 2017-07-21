# -*- coding: utf-8 -*-

"""
@version   : 0.1.0
@Author    : davidfnck
@contact   : davidfnck@gmail.com
@Time      : 2017/7/16 下午9:46
@Purpose   : 走通逻辑，用的是python
@Reference :
@File      : demo_python.py
@Software  : PyCharm
@PY.Version: 2.7

"""

import ast
import sqlite3
import pandas as pd
from pypinyin import pinyin, lazy_pinyin
import pypinyin

# ====== 读取 sougou 词库
def ReadFromTxt(file):
    word_list = []
    with open(file, 'rt') as f:
        for line in f:
            word_list.append(str(line).strip())
    return word_list

# ====== pandas 读取数据
def ReadFromSQLite():
    conn = sqlite3.connect("sougou.db")
    try:
    # 创建一个 df
        df = pd.read_sql_query("select * from sougou limit 5;", conn)

    except BaseException as e:
        print('Reason:',e)

    finally:
        conn.commit()
        print("Records created successfully")
        conn.close()

def DuPinYin(words):
    df = pd.DataFrame(columns=['WORD', 'COUNT', 'PINYIN'])
    x = 0
    while x < len(words):
        word = words[x]
        count = len(word.decode('utf-8'))
        word_pinyin = lazy_pinyin(words[x].decode('utf8'))
        df.loc[x] = {'WORD': word, 'COUNT': count, 'PINYIN':word_pinyin}
        x = x + 1
    return df

def SingleRhyme(df_bank):
    x = 0
    keys = []
    values = []
    while x < len(df_bank.index):
        rhyme = df_bank.iat[x,2][-1]
        keys.append(x)
        values.append(str(rhyme))
        rhyme_bank_single = dict(zip(keys, values))
        x = x + 1
    return rhyme_bank_single

def DoubleRhyme(df_bank):
    x = 0
    keys = []
    values = []
    while x < len(df_bank.index):
        rhyme = df_bank.iat[x,2][-2:]
        keys.append(x)
        values.append(str(rhyme))
        rhyme_bank_double = dict(zip(keys, values))
        x = x + 1
    return rhyme_bank_double

def SelectByInput(rhyme_bank,how_many):
    num = []
    if how_many == '1':
        rhyme = raw_input(">>> Input: ")
        for k,v in rhyme_bank.iteritems():
            if len(rhyme) == 1:
                if rhyme == v[-1]:
                    num.append(k)
            elif len(rhyme) != 1:
                result = v.rfind(rhyme)
                if result != -1:
                    num.append(k)
            # result = v.rfind(rhyme)
            # if result != -1:
            #     num.append(k)
    elif how_many == '2':
        result_1 = ''
        result_2 = ''
        rhyme_1 = raw_input(">>> Input: ")
        rhyme_2 = raw_input(">>> Input: ")
        for k,v in rhyme_bank.iteritems():
            v = ast.literal_eval(v)
            try:
                if len(rhyme_1) == 1:
                    if rhyme_1 == v[0][-1]:
                        result_1 = 0
                    else:
                        result_1 = -1
                else:
                    result_1 = v[0].rfind(rhyme_1)

                if len(rhyme_2) == 1:
                    if rhyme_2 == v[1][-1]:
                        result_2 = 0
                    else:
                        result_1 = -1
                else:
                    result_2 = v[1].rfind(rhyme_2)

            except BaseException as e:
                # 有些是单字的就会报错
                print (e)
            finally:
                if result_1 != -1 and result_2 != -1:
                    num.append(k)
    return num

def main():
    file = 'sougou.txt'
    words = ReadFromTxt(file)
    df_bank = DuPinYin(words)
    # 选择单押，双押，三押……
    how_many = raw_input(">>> Input: ")
    if how_many == '1':
        rhyme_banks = SingleRhyme(df_bank)
    else:
        rhyme_banks = DoubleRhyme(df_bank)
    IDnum = SelectByInput(rhyme_banks,how_many)
    for x in IDnum:
        print (df_bank.iat[x,0])

if __name__ == '__main__':
    main()
