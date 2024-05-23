import pandas as pd
# pip install lxml

class CodeReaderKOSPI:
    def __init__(self):
        self.stock_codes=[]
        self.stock_names=[]
        
    def read_kospi200_xls(self):
        kospi_list=pd.read_html("경로\\rltrader\data\상장법인목록_KOSPI200.xls")
        kospi_list[0].종목코드=kospi_list[0].종목코드.map("{:06d}".format)
        
        df=kospi_list[0].sort_values(by='종목코드')
        
        self.stock_codes=[code for code in df.종목코드]
        self.stock_names=[name for name in df.회사명]
        
        return self.stock_codes, self.stock_names

