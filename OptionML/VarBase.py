import os
os_type = 'win'
option_dir = r''
if os_type == 'win':
    option_dir = r'F:\option'

data_dir = os.path.join(option_dir, r'jQ\sh50\sh50etf_option_min')
underlying_price_data_file = os.path.join(data_dir, '510050XSHG.csv')
underlying_symbol = 'SSE.510050'