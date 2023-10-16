import numpy as np
from util import get_data
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

def nb(x_train, y_train, x_test, y_test):
    nbG = GaussianNB()
    nbG = nbG.fit(x_train, y_train)
    y_preds = nbG.predict(x_test)
    acc = accuracy_score(y_preds, y_test)
    print(acc)


def main():
    x_train, y_train, x_test, y_test = get_data()
    nb(x_train, y_train, x_test, y_test)

if __name__ == "__main__":
    main()