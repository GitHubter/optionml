from OptionML.VarBase import *
import pandas as pd
import numpy as np
import re
from datetime import *

class DataGet:

    def __init__(self):
        self._option_info_df = pd.read_csv(option_info_file)

    @staticmethod
    def get_underlying_price_ls(end_dt, count, freq=1):
        underlying_df = pd.read_csv(underlying_price_data_file, index_col=0)
        trading_date_time_string = end_dt.strftime('%Y-%m-%d %H:%M:%S')
        idxs = np.where(underlying_df.index.values <= trading_date_time_string)[0][-count*freq-1::freq]
        ret = underlying_df['close'].iloc[idxs].iloc[1:]
        if len(ret):
            return ret
        else:
            print(f'get underlying price list failed')

    @staticmethod
    def get_annualized_return_ls(end_dt_ls, get_by='week'):
        if get_by == 'week':
            data_size = 60 * 4 * 5

        underlying_df = pd.read_csv(underlying_price_data_file, index_col=0)
        trading_date_time_string_ls = [end_dt.strftime('%Y-%m-%d %H:%M:%S') for end_dt in end_dt_ls]
        end_dt_string = trading_date_time_string_ls[-1]
        days = len(end_dt_ls)
        idxs = np.where(underlying_df.index.values <= end_dt_string)[0][-data_size-days-1:]
        close_series = underlying_df['close'].iloc[idxs]
        ann_ret_ls = np.divide(np.subtract(close_series[-days:].values, close_series[:days].values), close_series[:days].values)
        ann_ret_ls = ann_ret_ls / 5 * 250
        if len(ann_ret_ls):
            return ann_ret_ls

    @staticmethod
    def get_annualized_var_ls(end_dt_ls, get_by='week'):
        var_sample_num = 100
        if get_by == 'week':
            freq = 60 * 4 * 5
            mul = 250 / 5
        data_size = freq * var_sample_num
        underlying_df = pd.read_csv(underlying_price_data_file, index_col=0)
        trading_date_time_string_ls = [end_dt.strftime('%Y-%m-%d %H:%M:%S') for end_dt in end_dt_ls]
        end_dt_string = trading_date_time_string_ls[-1]
        days = len(end_dt_ls)
        idxs = np.where(underlying_df.index.values <= end_dt_string)[0][-data_size-days-2:]
        close_series = underlying_df['close'].iloc[idxs]
        ret_series = (close_series - close_series.shift(freq)) / close_series.shift(freq)
        ann_var_ls = []
        for i in range(days):
            ret_series_qua = ret_series.iloc[i+1:-days+i:freq]
            t_var = ret_series_qua.std() * mul ** 0.5
            ann_var_ls.append(t_var)
        if len(ann_var_ls):
            return ann_var_ls

    @staticmethod
    def get_option_history_price_by_count(option_id, end_dt, count):
        option_filebasename = re.findall(r'\d+', option_id)[0] + 'XSHG.csv'
        option_filepat = os.path.join(data_dir, option_filebasename)
        option_df = pd.read_csv(option_filepat, index_col=0)
        if not isinstance(end_dt, str):
            end_dt = end_dt.strftime('%Y-%m-%d %H:%M:%S')
        idx_end = np.where(option_df.index.values == end_dt)[0]
        if not len(idx_end):
            print('数据不存在')
            return False
        idx_end = idx_end[0]
        if idx_end - count < 0:
            print(f'此时长度不足,为{idx_end}')
            idx_start = 0
        else:
            idx_start = idx_end - count
        option_close = option_df['close'].iloc[idx_start:idx_end+1]
        return option_close

    @staticmethod
    def get_option_last_time(option_id, end_dt, count):
        option_filebasename = re.findall(r'\d+', option_id)[0] + 'XSHG.csv'
        option_filepat = os.path.join(data_dir, option_filebasename)
        option_df = pd.read_csv(option_filepat, index_col=0)
        if not isinstance(end_dt, str):
            end_dt = end_dt.strftime('%Y-%m-%d %H:%M:%S')
        idx_t = np.where(option_df.index.values <= end_dt)[0]
        if not len(idx_t):
            print('数据不存在')
            return False
        idx_t = idx_t[-count:]
        last_time = (len(option_df) - idx_t) / (360 * 4 * 60)
        ret_series = pd.Series(last_time, index=option_df.index.values[idx_t])
        return ret_series


    def get_option_info(self, option_id):
        all_option_df = self._option_info_df
        option_code = re.findall(r'\d+', option_id)[0] + '.XSHG'
        ret_dict = {}
        option_series = all_option_df[all_option_df['code'] == option_code].iloc[0]
        ret_fields = ['exercise_price']

        for field in ret_fields:
            ret_dict[field] = option_series[field]
        ret_dict['option_id'] = option_code
        contract_type_dict = {'CO': 'call', 'PO': 'put'}
        ret_dict['option_class'] = contract_type_dict[option_series['contract_type']]
        return ret_dict






# end_dt = datetime(2018, 6, 26, 14, 30)
# DataGet.get_option_history_price_by_count('10001167sss', end_dt=end_dt, count=500)
# dataget =  DataGet()
# dataget.get_option_info('10001167')

