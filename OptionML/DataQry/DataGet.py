from OptionML.VarBase import *
import pandas as pd
import numpy as np

class DataGet:

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



