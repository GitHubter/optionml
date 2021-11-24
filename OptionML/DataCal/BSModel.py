import numpy as np
from scipy.stats import norm
from scipy.optimize import fsolve

class BSModel:

    def __init__(self, S, K, sigma, T, r):
        self._d1 = self.Cald1( S, K, sigma, T, r)
        self._d2 = self._d1 - sigma * T **0.5
        self._call = self.GetOptionPriceNorm(S, K, sigma, T, r, 'call')
        self._put = self.GetOptionPriceNorm(S, K, sigma, T, r, 'put')

    @staticmethod
    def Cald1(S, K, sigma, T, r):

        d1_num = np.log(S / K) + (r + sigma ** 2 / 2) * T
        d1_den = sigma * T ** 0.5
        d1 = d1_num / d1_den
        return d1

    @staticmethod
    def Cald2(S, K, sigma, T, r):

        d2_num = np.log(S / K) + (r - sigma ** 2 / 2) * T
        d2_den = sigma * T ** 0.5
        d2 = d2_num / d2_den
        return d2

    @staticmethod
    def GetCallnPrice(S, K, sigma, T, r):

        d1 = BSModel.Cald1(S, K, sigma, T, r)
        d2 = BSModel.Cald2(S, K, sigma, T, r)
        Call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return Call

    @staticmethod
    def GetPutPrice(S, K, sigma, T, r):

        d1 = BSModel.Cald1(S, K, sigma, T, r)
        d2 = BSModel.Cald2(S, K, sigma, T, r)
        Put = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return Put

    @staticmethod
    def GetImpliedVolatility(S, K, Price, T, r, option_class):
        if option_class == 'call':
            def callfun(sigma):
                return BSModel.GetCallnPrice(S, K, sigma, T, r)
            iv = fsolve(callfun, [Price])

        elif option_class == 'put':
            def putfun(sigma):
                return BSModel.GetPutPrice(S, K, sigma, T, r)
            iv = fsolve(putfun, [Price])
        else:
            print('期权类型错误')

        return iv[0]

    # @staticmethod
    # def GetImpliedVolatilityLst(S_lst, K_lst, P_lst, T_lst, r_lst, lst, option_class):
    #     if option_class == 'call':
    #         def callfun(sigma):
    #             return BSModel.GetCallnPrice(S, K, sigma, T, r)
    #     elif option_class == 'put':
    #         def putfun(sigma):
    #             return BSModel.GetPutPrice(S, K, sigma, T, r)
    #     else:
    #         print('期权类型错误')














