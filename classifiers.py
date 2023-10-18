from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier


def naiveBayes(x_train, y_train, x_test):
    nbG = GaussianNB()
    nbG = nbG.fit(x_train, y_train)
    y_pred = nbG.predict(x_test)
    return y_pred

def logistricRegression(x_train, y_train, x_test):
    logReg = LogisticRegression()
    logReg = logReg.fit(x_train, y_train)
    y_pred = logReg.predict(x_test)
    return y_pred

def decisionTree(x_train, y_train, x_test):
    clf = DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    return y_pred

def randomForest(x_train, y_train, x_test, n):
    clf = RandomForestClassifier(n_estimators=n)
    clf = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    return y_pred

def gradientBoost(x_train, y_train, x_test):
    clf = GradientBoostingClassifier(random_state=42)
    clf = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    return y_pred

def SVM(x_train, y_train, x_test):
    clf=svm.SVC()
    clf.fit(x_train,y_train)
    y_pred = clf.predict(x_test)
    return y_pred

def neuralNetwork(x_train, y_train, x_test):
    clf = MLPClassifier(hidden_layer_sizes=int(2* len(x_train.columns) / 3), random_state=42, activation='logistic')
    clf = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    return y_pred