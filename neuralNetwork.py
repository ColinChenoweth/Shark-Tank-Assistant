from sklearn.neural_network import MLPClassifier
from util import get_data

def main():
    x_train, y_train, x_test, y_test = get_data()
    clf = MLPClassifier(hidden_layer_sizes=int(2* len(x_train.columns) / 3), random_state=42, activation='logistic')
    clf = clf.fit(x_train, y_train)
    y_preds = clf.predict(x_test)
    acc = sum(y_preds == y_test) / len(y_test)
    print(acc)

if __name__ == "__main__":
    main()