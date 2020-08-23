# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

categeories = {
    'государство':0,
    'политика и общество':1,
    'социальная сфера':2,
    'ЖКХ':3,
    'благоустройство':4,
    'культура':5,
    'экономика':6,
    'безопасность':7,
    'транспорт и дорожное хозяйство':8,
    'инфраструктура':9,
    'сельское хозяйство':10}


class ClassifierModel:
    def __init__(self, predictor, encoder, labels_to_ids):
        self.predictor = predictor
        self.encoder = encoder
        self.ids_to_labels = {val: key for key, val in labels_to_ids.items()}

    def predict(self, X):
        result = self.predictor.predict(self.encoder.transform([X]))[0]
        return self.ids_to_labels[result]


def train(folder):
    X_corpus = []
    y_corpus = []

    ads = pd.read_csv(folder+'advertisement_v2.csv', encoding='cp1251', sep=';')
    ads = ads.dropna()
    l = [categeories['политика и общество']] * len(ads['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(ads['Описание'])

    apt = pd.read_csv(folder+'apartments_v2.csv', encoding='cp1251', sep=';')
    apt = apt.dropna()
    l = [categeories['ЖКХ']] * len(apt['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(apt['Описание'])

    bst = pd.read_csv(folder+'bus_stops_v2.csv', encoding='cp1251', sep=';')
    bst = bst.dropna()
    l = [categeories['инфраструктура']] * len(bst['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(bst['Описание'])

    ctt = pd.read_csv(folder+'city_territory_v2.csv', encoding='cp1251', sep=';')
    ctt = ctt.dropna()
    l = [categeories['благоустройство']] * len(ctt['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(ctt['Описание'])

    cwk = pd.read_csv(folder+'construction_works_v2.csv', encoding='cp1251', sep=';')
    cwk = cwk.dropna()
    l = [categeories['безопасность']] * len(cwk['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(cwk['Описание'])

    dvr = pd.read_csv(folder+'dvor_v2.csv', encoding='cp1251', sep=';')
    dvr = dvr.dropna()
    l = [categeories['ЖКХ']] * len(dvr['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(dvr['Описание'])

    med = pd.read_csv(folder+'medical_v2.csv', encoding='cp1251', sep=';')
    med = med.dropna()
    l = [categeories['социальная сфера']] * len(med['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(med['Описание'])

    prk = pd.read_csv(folder+'parks_v2.csv', encoding='cp1251', sep=';')
    prk = prk.dropna()
    l = [categeories['благоустройство']] * len(prk['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(prk['Описание'])

    rad = pd.read_csv(folder+'road_v2.csv', encoding='cp1251', sep=';')
    rad = rad.dropna()
    l = [categeories['транспорт и дорожное хозяйство']] * len(rad['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(rad['Описание'])

    crs = pd.read_csv(folder+'street_crossings_v2.csv', encoding='cp1251', sep=';')
    crs = crs.dropna()
    l = [categeories['безопасность']] * len(crs['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(crs['Описание'])

    trs = pd.read_csv(folder+'public_transport_v2.csv', encoding='cp1251', sep=';')
    trs = trs.dropna()
    l = [categeories['транспорт и дорожное хозяйство']] * len(trs['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(trs['Описание'])

    mto = pd.read_csv(folder+'moving_trading_objects_v2.csv', encoding='cp1251', sep=';')
    mto = mto.dropna()
    l = [categeories['экономика']] * len(mto['Описание'])
    y_corpus.extend(l)
    X_corpus.extend(mto['Описание'])

    print(len(X_corpus), len(y_corpus))
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X_corpus)
    print(len(vectorizer.get_feature_names()))

    vect = pd.DataFrame(columns=['Слова'])
    vect['Слова'] = vectorizer.get_feature_names()

    X_train, X_test, y_train, y_test = train_test_split(X, y_corpus, test_size=0.05)

    clf = MLPClassifier(hidden_layer_sizes=(20, 20, 20), max_iter=25, verbose=1)
    clf = clf.fit(X_train, y_train)

    print(clf.score(X_test, y_test))
    return ClassifierModel(clf, vectorizer, categeories)
