# # Save Model Using Pickle
# import csv
# import time
# import pickle
# import logging
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import iqoptionapi.constants as api_constants
# import matplotlib.dates as mdates
# import matplotlib.ticker as mticker

# from matplotlib.finance import candlestick_ohlc
# from pandas import read_csv
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.linear_model import ElasticNet
# from sklearn.linear_model import SGDClassifier
# from sklearn.kernel_approximation import RBFSampler

# from sklearn.svm import LinearSVC
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.ensemble import RandomForestClassifier, VotingClassifier

# from iqoptionapi.api import IQOptionAPI
# from config import parse_config


# class Learner(object):
#     """Class for ML."""

#     def __init__(self, api, active):
#         self.api = api
#         self.active = api_constants.ACTIVES[active]


#     def fetch_candles(self):
#         """Methond to fetch candles form IQOptions Websocket api"""
#         while not (self.active in self.api.activeCandles):
#             self.api.getcandles(self.active, 60, 60 * 12)
#             time.sleep(3)

#         if self.active in self.api.activeCandles:
#             return self.api.activeCandles[self.active]
#         else:
#             return False

#     def rsi(self, candles, period=14):
#         """Method to get RSI on fetched candels."""
#         if hasattr(candles, 'candles_array'):
#             candel_array = candles.candles_array
#             prices = pd.Series([candle.candle_close for candle in candel_array])
#             delta = prices.diff()

#             d_up, d_down = delta.copy(), delta.copy()
#             d_up[d_up < 0] = 0
#             d_down[d_down > 0] = 0

#             rol_up = d_up.rolling(window=period).mean()
#             rol_down = d_down.rolling(window=period).mean().abs()

#             relativestrength = rol_up / rol_down
#             rsi = 100.0 - (100.0 / (1.0 + relativestrength))

#             return rsi

#     def bolinger_bands(self, candles, period=14, num_of_std=2):
#         """Method to get BB on fetched candels."""
#         if hasattr(candles, 'candles_array'):
#             candel_array = candles.candles_array
#             prices = pd.Series([candle.candle_close for candle in candel_array])

#             rolling_mean = prices.rolling(window=period).mean()
#             rolling_std = prices.rolling(window=period).std()
#             upper_band = rolling_mean + (rolling_std*num_of_std)
#             lower_band = rolling_mean - (rolling_std*num_of_std)
#             height = upper_band - lower_band

#             return upper_band, lower_band, height

#     def stoc_occilator(self, candles, period=13):
#         """Method to get Stocastic occilator on fetched candels."""
#         if hasattr(candles, 'candles_array'):
#             candel_array = candles.candles_array
#             close = pd.Series([candle.candle_close for candle in candel_array])
#             low = pd.Series([candle.candle_low for candle in candel_array])
#             high = pd.Series([candle.candle_high for candle in candel_array])

#             l_period = low.rolling(window=period).min()
#             h_period = high.rolling(window=period).max()

#             K = 100*((close - l_period) / (h_period - l_period) )
#             D = K.rolling(window=3).mean()

#             return K, D

#     def aroon(self, candles, period=25):
#         """Method to get aroon occilator on fetched candels."""
#         if hasattr(candles, 'candles_array'):
#             candel_array = candles.candles_array
#             aroon_up = []
#             aroon_down = []
#             candle_data = []
#             time_data = []

#             for index, candle in enumerate(candel_array):
#                 ar_up = 0.0
#                 ar_down = 0.0
#                 time_data.append(candle.candle_time)

#                 if(candle.candle_close > 0):
#                     append_me = candle.candle_time, candle.candle_open, candle.candle_high, candle.candle_low, candle.candle_close
#                     candle_data.append(append_me)

#                 if index > period:
#                     low = [candle.candle_low for candle in candel_array[index-period:index]]
#                     high = [candle.candle_high for candle in candel_array[index-period:index]]

#                     l_period = min(low)
#                     h_period = max(high)

#                     ind_of_high = high.index(h_period)
#                     ind_of_low = low.index(l_period)
                    
#                     days_since_high = period - ind_of_high - 1
#                     days_since_low = period - ind_of_low - 1
                    
#                     ar_up = float(((period - days_since_high)/float(period)) * 100)
#                     ar_down = float(((period - days_since_low)/float(period)) * 100)


#                 aroon_up.append(ar_up)
#                 aroon_down.append(ar_down)

#             f, axarr = plt.subplots(2, sharex=True)
#             axarr[0].set_title('price')
#             # axarr[0].plot(close)
#             candlestick_ohlc(axarr[0], candle_data, width=0.4, colorup='#77d879', colordown='#db3f3f')
#             axarr[1].set_title('aroon')
#             axarr[1].plot(time_data, aroon_up, color='green')
#             axarr[1].plot(time_data, aroon_down, color='red')
#             plt.show()

            
#             return aroon_up, aroon_down

#     def create_csv(self):
#         """Method to create csv based on fetched candels."""
#         url = "traningData.csv"
#         candles = self.fetch_candles()

#         if hasattr(candles, 'first_candle'):
#             up, lw, height = self.bolinger_bands(candles=candles)
#             rsi14 = self.rsi(candles=candles)
#             K, D = self.stoc_occilator(candles=candles)
#             aroon_up, aroon_down = self.aroon(candles=candles)

#             candles_array = candles.candles_array
#             ofile = open(url, "wb+")
#             writer = csv.writer(ofile, quoting=csv.QUOTE_NONE, escapechar='\n')
#             for index, candle in enumerate(candles_array):
#                 if index > 28 and candle.candle_close > 0 and candle.candle_height > 0:
#                     if candles_array[index - 2].candle_close < lw[index - 3]:
#                         if candles_array[index - 2].candle_type == "red" and candles_array[index - 1].candle_type == "green":
#                             if candles_array[index - 1].candle_height >= (candles_array[index - 2].candle_height / 2):
#                                 category = 1.0 if candle.candle_type == "green" else 0.0
#                                 writer.writerow([up[index - 3] - candles_array[index - 2].candle_close, lw[index - 3] - candles_array[index - 2].candle_close, candles_array[index - 2].candle_height - candles_array[index - 1].candle_height, rsi14[index - 1], K[index - 1], D[index - 1], aroon_up[index - 1], aroon_down[index - 1], category])
#                     elif candles_array[index - 2].candle_close > up[index - 3]:
#                         if candles_array[index - 2].candle_type == "green" and candles_array[index - 1].candle_type == "red":
#                             if candles_array[index - 1].candle_height >= (candles_array[index - 2].candle_height / 2):
#                                 category = -1.0 if candle.candle_type == "red" else 0.0
#                                 writer.writerow([up[index - 3] - candles_array[index - 2].candle_close, lw[index - 3] - candles_array[index - 2].candle_close, candles_array[index - 2].candle_height - candles_array[index - 1].candle_height, rsi14[index - 1], K[index - 1], D[index - 1], aroon_up[index - 1], aroon_down[index - 1], category])
#                     else:
#                         writer.writerow([up[index - 3] - candles_array[index - 2].candle_close, lw[index - 3] - candles_array[index - 2].candle_close, candles_array[index - 2].candle_height - candles_array[index - 1].candle_height, rsi14[index - 1], K[index - 1], D[index - 1], aroon_up[index - 1], aroon_down[index - 1], 0.0])
#             ofile.close()

#     def save_model(self):
#         """Method to save liner regression model."""
#         url = "traningData.csv"
#         dataframe = read_csv(url)
#         array = dataframe.values
#         X = array[:, 0:8]
#         Y = array[:, 8]

#         model = RandomForestClassifier(random_state=1)
#         # model = ElasticNet(random_state=0)
#         # model = LinearSVC(random_state=0)
#         model.fit(X, Y)

#         # save the model to disk
#         filename = 'finalized_model.sav'
#         pickle.dump(model, open(filename, 'wb'))

#         return


# def create_learner(api, active):
#     """Method for create learner.

#     :param api: The IQ Option API.
#     :param active: The trader active.
#     """
#     logger = logging.getLogger(__name__)
#     logger.info("Create learner for active '%s'.", active)
#     return Learner(api, active)


# # url = "traningData.csv"
# # dataframe = read_csv(url)
# # array = dataframe.values
# # X = array[:, 0:8]
# # Y = array[:, 8]

# # test_size = 0.33
# # seed = 8
# # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

# # # Fit the model on 33%
# # # model = VotingClassifier([('lsvc', LinearSVC(random_state=0)), ('knn', KNeighborsClassifier()), ('rfor', RandomForestClassifier(random_state=1))])
# # model = RandomForestClassifier(random_state=1)
# # model.fit(X_train, Y_train)
# # # save the model to disk

# # filename ='finalized_model_test.sav'
# # pickle.dump(model, open(filename,'wb'))

# # # some time later...

# # # load the model from disk
# # loaded_model = pickle.load(open(filename,'rb'))
# # result = loaded_model.score(X_test, Y_test)

# # f, axarr = plt.subplots(2, sharex=True)
# # axarr[0].plot(loaded_model.predict(X_test), 'o')
# # axarr[0].set_title('Predicted')
# # axarr[1].set_title('Orignal')
# # axarr[1].plot(Y_test, 'o')

# # plt.show()
# # print(result)