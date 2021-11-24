from OptionML.DataQry.DataGet import DataGet
from OptionML.DataCal.BSModel import BSModel
from datetime import *
import numpy as np
import pandas as pd

dt = datetime(2020, 5, 25, 14, 15, 0)
sample_size = 2000
sample_freq = 60

#获得sample_size个数据点，其中采样频率为sample_freq分钟，最后记录时间为dt
close = DataGet.get_underlying_price_ls(dt, sample_size, sample_freq)
#蒙特卡洛方法从正态分布中抽样
rand_norm = np.random.normal(0, 1, sample_size)
sim_df = pd.DataFrame(close)

trading_date_ls = [datetime.strptime(trading_date, '%Y-%m-%d %H:%M:%S') for trading_date in sim_df.index.values]
#从历史数据中计算股票的年化收益，年化波动作为漂移率和方差率
sim_df['return'] = (sim_df['close'] - sim_df['close'].shift(1)) / sim_df['close'].shift(1)
sim_df['drift'] = DataGet.get_annualized_return_ls(trading_date_ls)
sim_df['variance'] = DataGet.get_annualized_var_ls(trading_date_ls)

#计算未来一周的股价变化
dt = 5 / 250
close_chg = sim_df['drift'] * sim_df['close'] * dt + sim_df['variance'] * sim_df['close'] * rand_norm * dt ** 0.5
sim_df['sim_close'] = sim_df['close'] + close_chg

#模拟lnS未来一周的走势
sim_df['lnS'] = np.log(sim_df['close'])
T = 5 / 250
sim_df['sim_lnS'] = np.zeros(sample_size)
for i in range(sample_size):
    lnS_0 = sim_df['lnS'].iloc[i]
    drift = sim_df['drift'].iloc[i]
    var = sim_df['variance'].iloc[i] ** 2
    u = lnS_0 + (drift - (var * 0.5)) * T
    sigma = var * T ** 0.5
    sim_df['sim_lnS'].iloc[i] = np.random.normal(u, sigma, 1)[0]

#期权BS定价模型

##取得期权价格历史数据
end_dt = datetime(2018, 6, 26, 14, 30)
option_id = '10001167'
count = 500
close_df = DataGet.get_option_history_price_by_count(option_id, end_dt=end_dt, count=count)
last_time = DataGet.get_option_last_time(option_id, end_dt=end_dt, count=count)
S = DataGet.get_underlying_price_ls(end_dt=end_dt, count=count)
iv = BSModel.GetImpliedVolatility(3, 3, 0.06, 0.05, 0.03, 'call')
for S, Price, T in zip()


