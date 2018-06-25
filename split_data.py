#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


column_list = ["매출액","영업이익","매출원가","판관비","비영업손익","금융손익","세전순익","법인세","순익(단순)","영활현흐","재무현흐","유동자산","부채총계","자본총계","총자산","시총"]



def main():
    df = pd.read_csv('stock_data_2009_2017.csv')
    print(df.shape)
    for i in tqdm(range(len(df)), ncols=100):
        code, name = df.iloc[i,:2]
        idx = 2
        data = {"20%02d-12-01"%int(x):[] for x in range(9,18)}
        for col in range(len(column_list)):
            for year in range(9,18):
                dic_y = "20%02d-12-01"%int(year)
                data[dic_y].append(df.iloc[i,idx])
                idx += 1
        pd.DataFrame.from_dict(data, orient='index', columns=column_list).to_csv('data_past/%s.csv'%code)


    #print(df.head())


def test():
    print()


if __name__ == '__main__':
    main()
