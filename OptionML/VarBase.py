import os
os_type = 'mac'
if os_type == 'win':
    option_dir = r'F:\option'
if os_type == 'mac':
    option_dir = '/Volumes/My Passport/option'

option_info_file = os.path.join(option_dir, 'jQ/sh50/sh50option_info.csv')
data_dir = os.path.join(option_dir, 'jQ/sh50/sh50etf_option_min')
underlying_price_data_file = os.path.join(data_dir, '510050XSHG.csv')
underlying_symbol = 'SSE.510050'
