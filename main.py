import data_retrieval as dr
import file_utils as fu
import numpy as np
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import ADASYN
from imblearn.combine import SMOTETomek
from imblearn.under_sampling import TomekLinks
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from collections import Counter, OrderedDict
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score


def sample_balancer(X, Y, method):
    sm = method
    X_res, Y_res = sm.fit_resample(X, Y)
    return X_res, Y_res


def plot_histogram(Y, tt):
    plt.figure()
    colors = ['blue', 'green', 'gold', 'red', 'orchid']
    sum_occurrances = Counter(Y).most_common()
    plt.bar(list(OrderedDict(sum_occurrances).keys()), [value[1] for value in sum_occurrances], align='center', color=colors)
    plt.xticks(list(OrderedDict(sum_occurrances).keys()), [label_mapping[index] for index in list(OrderedDict(sum_occurrances).keys())])
    plt.grid(True)
    plt.title(tt)


def perform_KMeans(X):
    kmeans = KMeans(n_clusters=len(label_mapping))
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)

    ax = Axes3D(plt.figure())
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y_kmeans, s=20)
    centers = kmeans.cluster_centers_
    ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], c='black', s=100, alpha=0.4)


def main_menu():
    print("Welcome to the program.\nThe system is now checking if there are samples already saved locally...\n")
    dr.check_local_files()
    print("That's all for now!! Thank you")


main_menu()
gene_data, ens_gene_list, y, label_mapping = fu.get_data_from_files()

# apply PCA to the matrix
pca = PCA(n_components=4)
X_t = pca.fit_transform(gene_data)

# ax = Axes3D(plt.figure())
# ax.scatter(X_t[:, 0], X_t[:, 1], X_t[:, 2], c=y)

# plt.figure()
# plt.plot(pca.explained_variance)

kf = KFold(n_splits=5)

classifier_names = ['Decision Tree Classifier', 'Gaussian Naive Bayes']
clfs = [DecisionTreeClassifier(), GaussianNB()]
sample_balancers = ['ADASYN (over)', 'SMOTETomek (over+under)', 'TomekLinks (under)']
blnc = [ADASYN(), SMOTETomek(), TomekLinks()]
split_index = 0

for train_index, test_index in kf.split(X_t):
    X_train, X_test = X_t[train_index], X_t[test_index]
    Y_train = y[min(train_index): max(train_index)]
    Y_test = y[min(test_index): max(test_index)]

    for balancer, balancer_name in zip(blnc, sample_balancers):
        X_train_t, Y_train_t = sample_balancer(X_train, Y_train, balancer)
        for classifier_name, clf in zip(classifier_names, clfs):
            clf.fit(X_train, Y_train)
            Y_predicted = clf.predict(X_test)
            print("MODEL: {}\nBALANCING METHOD: {}\nSPLIT N: {}".format(classifier_name, balancer_name, split_index))
            print(precision_recall_fscore_support(Y_test, Y_predicted))
            print("ACCURACY: {}".format(accuracy_score(Y_test, Y_predicted)))

    split_index += 1

# dealing with classes imbalances: over and under sampling
X_train, X_test, Y_train, Y_test = train_test_split(X_t, y, test_size=0.2)
print("The before oversampling we have a {} matrix".format(len(X_train)))

plt.figure()
# X_train_sm, Y_train_sm = sample_balancer(X_train, Y_train, SMOTE())
# X_train_ros, Y_train_ros = sample_balancer(X_train, Y_train, RandomOverSampler())
X_train_ada, Y_train_ada = sample_balancer(X_train, Y_train, ADASYN())
#
# X_train_tmk, Y_train_tmk = sample_balancer(X_train, Y_train, TomekLinks())
# X_train_smtmk, Y_train_smtmk = sample_balancer(X_train, Y_train, SMOTETomek())

# plot_histogram(Y_train, "Training sample distribution")
# plot_histogram(Y_train_tmk, "Training sample distribution w/ undersampling")
# plot_histogram(Y_train_sm, "Training sample distribution w/ oversampling")
# plot_histogram(Y_train_smtmk, "Training sample distribution w/ over + undersampling")

perform_KMeans(X_train_ada)


print("hello")
print("finish")
# plt.show()