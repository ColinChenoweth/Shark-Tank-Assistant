import numpy as np
from util import get_data
from sklearn.naive_bayes import GaussianNB

def nb(x_train, y_train, x_test, y_test):
    nb = GaussianNB()
    nb.fit(x_train, y_train)
    y_preds = nb.predict(x_test)
    acc = np.sum(y_preds == y_test) / len(y_test)
    print(acc)

def main():
    x_train, y_train, x_test, y_test = get_data()
    nb(x_train, y_train, x_test, y_test)

if __name__ == "__main__":
    main()