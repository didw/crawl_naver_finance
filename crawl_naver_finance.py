#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from util import get_date_str
from crawl_naver_finance_more import get_additional_naver_finance

DEBUG = False

def get_code_list():
    df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
    df.종목코드 = df.종목코드.map('{:06d}'.format)
    return df.종목코드

'''
* code: 종목코드
* fin_type = '0': 재무제표 종류 (0: 주재무제표, 1: GAAP개별, 2: GAAP연결, 3: IFRS별도, 4:IFRS연결)
* freq_type = 'Y': 기간 (Y:년, Q:분기)
'''
def get_finstate_naver(code, fin_type='0', freq_type='Y'):
    url_tmpl = 'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?' \
                   'cmp_cd=%s&fin_typ=%s&freq_typ=%s'

    url = url_tmpl % (code, fin_type, freq_type)
    print("url:%s"%url)
    dfs = pd.read_html(url, encoding="utf-8")
    if DEBUG:
        print(dfs)
    df = dfs[0]
    if df.ix[0,0].find('해당 데이터가 존재하지 않습니다') >= 0:
        return None

    df.columns = ['주요재무정보']+[x[1] for x in df.columns[:-1]]
    df.rename(columns={'주요재무정보':'date'}, inplace=True)
    df.set_index('date', inplace=True)
    df = df.iloc[:, [j for j,c in enumerate(df.columns) if '(E)' not in c]]
    df.columns = [get_date_str(x) for x in df.columns]
    dft = df.T
    dft.columns = [x for x in dft.columns]
    dft.index = pd.to_datetime(dft.index)

    # remove if index is NaT
    dft = dft[pd.notnull(dft.index)]
    df_add = get_additional_naver_finance(code, freq_type)
    if DEBUG:
        print(dft)
        print(df_add)
    res_df = pd.concat([dft, df_add], axis=1, join='inner')
    return res_df


def main():
    code_list = get_code_list()
    for freq_typ, directory in zip(['Y', 'Q'], ['fin_year', 'fin_quarter']):
        for code in tqdm(code_list, ncols=80):
            print(code, end='\r')
            df = get_finstate_naver(code, '0', freq_typ)
            df.to_csv('%s/%s.csv'%(directory, code))


def test():
    DEBUG = True
    df = get_finstate_naver('000030', '0', 'Y')
    print(df)


if __name__ == '__main__':
    test()
