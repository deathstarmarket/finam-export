#!/usr/bin/env python
import logging
from tqdm import tqdm
import pandas as pd
import numpy as np
import datetime
from finam import Exporter, Market, LookupComparator

"""
Full-on example displaying up-to-date values of some important indicators
"""


def main():
    exporter = Exporter()
    #print('*** Current Russian ruble exchange rates ***')
    #rub = exporter.lookup(name='USDRUB_TOD', market=Market.CURRENCIES)
    #assert len(rub) == 1
    #data = exporter.download(rub.index[0], market=Market.CURRENCIES)
    #print(data.tail(1))

    #print('*** MVID ***')
    #data = exporter.lookup(code='MVID', market=Market.SHARES,
                       #   code_comparator=LookupComparator.EQUALS)
    #assert len(oil) == 1
    #data = exporter.download(data.index[0], market=Market.SHARES)
    #tail=pd.DataFrame(data.tail(1))
    #print(data.tail(1))
    #k=tail.loc[:]["<CLOSE>"]
    #print(int(k))

    codes=pd.read_csv("codes.csv", delimiter = "\t", index_col="id")
    #print(codes)
    codes=pd.DataFrame(codes.tail(255))

    averages=[]
    drop_list=[]
    prices=[]

    for code in codes["code"]:
        try:
            data=pd.read_csv(f"{code}"+".csv", sep="\t", encoding="utf-8")
            data=pd.DataFrame(data.tail(255))

            yearly_average=round(np.average(data["<CLOSE>"], weights=data["<VOL>"]),2)
            averages.append(yearly_average)

            tail=pd.DataFrame(data.tail(1))
            price=int(tail.loc[:]["<CLOSE>"])
            prices.append(price)

            drop=round(price/yearly_average-1,2)
            drop_list.append(drop)

            print(code, "Yearly_average", yearly_average, "Price", price, "Drop", drop)

            #print(data)

            """downloading script
            print("Downloading", code)
            data = exporter.lookup(code=code, market=Market.SHARES,code_comparator=LookupComparator.EQUALS)

            #assert len(data) == 1 #hz, zachem eta hren', but it blocked BSPBP for example
            data = exporter.download(data.index[0], market=Market.SHARES, start_date=datetime.date(2020, 10, 5))
            data.to_csv(f"{code}"+".csv", sep="\t", encoding="utf-8")

            yearly_average=round(np.average(data["<CLOSE>"], weights=data["<VOL>"]),2)
            averages.append(yearly_average)
            print ("Downloading complete")

            tail=pd.DataFrame(data.tail(1))
            price=int(tail.loc[:]["<CLOSE>"])
            drop=round(price/yearly_average-1,2)
            drop_list.append(drop)
            print(code, "Yearly_average", yearly_average, "Price", price, "Drop", drop)
            """


        except ZeroDivisionError:
            print("ZeroDivisionError")
            yearly_average=0
            drop=0
            price=0
            prices.append(price)
            drop_list.append(drop)
            averages.append(yearly_average)


    codes["VWAP255"]=averages
    codes["PRICE"]=prices
    codes["DROP"]=drop_list
    print (codes)
    watch_list=codes[codes["DROP"] < -0.1]
    watch_list=watch_list[watch_list["DROP"] > -1]
    watch_list=watch_list.sort_values(by="DROP")
    watch_list.to_csv("watch_list.csv")
    codes.to_csv("codes_results.csv")



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
