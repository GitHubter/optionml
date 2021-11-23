import os
os_type = 'win'
option_dir = r''
if os_type == 'win':
    option_dir = r'F:\option'

underlying_price_data_file = os.path.join(option_dir, r'jQ\sh50\sh50etf_option_min', '510050XSHG.csv')
underlying_symbol = 'SSE.510050'