from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import json
from util import get_date_str
import copy

"""

매출액: 매출액(수익)
영업이익: 영업이익
매출원가: 매출원가
판관비: 판매비와관리비
비영업손익: 
금융손익: 
세전순익: 법인세비용차감전계속사업이익
법인세: 법인세비용
순익(단순): 당기순이익
영활현흐: 영업활동현금흐름
재무현흐: 재무활동현금흐름
유동자산
부채총계: 부채총계
자본총계: 자본총계
총자산: 자산총계
시총
"""
DEBUG = False

def get_additional_naver_finance(code, freq_type='Y'):
    frqTyp = '0' if freq_type == 'Y' else '1'
    url_tmpl = "http://companyinfo.stock.naver.com/v1/company/cF3002.aspx?cmp_cd={}&frq=0&rpt=0&finGubun=MAIN&frqTyp={}&cn="
    url = url_tmpl.format(code, frqTyp)
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
     
    #string to json object
    jsonObject = json.loads(str(bsObj))
    dates = jsonObject['YYMM']

    result = {}
    if DEBUG:
        print(dates)
    dates = [get_date_str(x) for x in dates[:5]]
    del_idx = []
    for i,date in enumerate(dates):
        if date == '':
            dates[i] = 'to_remove'
            date = 'to_remove'
        result[date] = []
    if DEBUG:
        print(dates)
    data = jsonObject['DATA']
    
    no_data = True
    for item in data:
        if item['ACC_NM'] != "매출원가":
            continue
        for i, date in enumerate(dates):
            result[date].append(item['DATA%d'%(i+1)])
            no_data = False
    
    url_tmpl = "http://companyinfo.stock.naver.com/v1/company/cF3002.aspx?cmp_cd={}&frq=0&rpt=1&finGubun=MAIN&frqTyp={}&cn="
    url = url_tmpl.format(code, frqTyp)
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
     
    #string to json object
    jsonObject = json.loads(str(bsObj))

    data = jsonObject['DATA']
    
    for item in data:
        if item['ACC_NM'] != "유동자산":
            continue
        for i, date in enumerate(dates):
            result[date].append(item['DATA%d'%(i+1)])
            no_data = False

    cpy_result = copy.copy(result)
    for k,v in result.items():
        if k == 'to_remove':
            del cpy_result[k]
    result = cpy_result
    if no_data:
        return pd.DataFrame([],columns=['매출원가','유동자산'])
    df = pd.DataFrame.from_dict(result, orient='index', columns=['매출원가','유동자산'])
    df.index = pd.to_datetime(df.index)
    return df.sort_index()

def main():
    DEBUG = True
    df = get_additional_naver_finance("267250")
    print(df)

if __name__ == '__main__':
    main()