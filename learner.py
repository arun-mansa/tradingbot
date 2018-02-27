# Save Model Using Pickle
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
url = "traningData.csv"
names = ['time', 'open', 'rsi', 'high', 'low', 'height', 'close']
dataframe = read_csv(url, names=names)
dataframe = dataframe.drop(columns=['time'])

array = dataframe.values
X = array[:,0:5]
Y = array[:,5]
test_size = 0.50
seed = 5

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
# Fit the model on 33%
model = LogisticRegression()
model.fit(X_train, Y_train)
# save the model to disk
filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

# some time later...

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
loaded_model.predict(X_test).plot()
print(Y_test)
print(result)