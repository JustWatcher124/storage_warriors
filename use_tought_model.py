import pandas as pd
import sklearn
import pickle
import argparse
import os

def main(model_pkl_file_loc: str = './tought_models/DecisionTree_data_wanted_data.csv.pkl'):
    if os.path.isfile(model_pkl_file_loc):
        model = pickle.loads(model_pkl_file_loc)
    else:
        model = None

    return model


if __name__ == '__main__':
    main()
