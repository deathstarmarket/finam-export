#!/usr/bin/env python
# coding: utf-8
import logging
import pandas as pd
from finam import Exporter, Market, LookupComparator
import re

"""
This sample script shows off lookup capabilities
"""


def main():
    exporter = Exporter()
    print('*** Looking up all RTS futures codes ***')
    res = exporter.lookup(
        market=[Market.FUTURES_ARCHIVE, Market.FUTURES],
        name='RTS-',
        name_comparator=LookupComparator.STARTSWITH)
    print(','.join(res['code']))

    print('*** Looking up Russian Ministry of Finance\'s bonds ***')
    print(exporter.lookup(market=Market.BONDS, name=u'ОФЗ',
                          name_comparator=LookupComparator.STARTSWITH))

    print('*** Looking up Microsoft ***')
    print(exporter.lookup(market=Market.USA, name='Microsoft',
                          name_comparator=LookupComparator.CONTAINS))

    print('*** Looking up LSRG ***')
    print(exporter.lookup(market=Market.USA, name='Microsoft',
                          name_comparator=LookupComparator.CONTAINS))


    print('*** Looking up Shares ***')
    #codes = exporter.lookup(market=Market.SHARES, name=u'\w',
    #                      name_comparator=LookupComparator.CONTAINS)

    codes = exporter.lookup(market=Market.SHARES, code=u'[^\-]',
                          code_comparator=LookupComparator.CONTAINS)

    def searcher (text):
        if text:
            result = re.search(r'RM', text)
            if result:
                return True
        else:
            return False
        return result

    print(codes)
    codes = pd.DataFrame(codes)

    codes=codes[codes.index < 999999]

    codes.to_csv("codes.csv", sep="\t", encoding="utf-8")
    print(codes)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
