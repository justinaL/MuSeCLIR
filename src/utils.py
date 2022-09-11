import pickle

def unpickle(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def save_pickle(file, var):
    print('SAVING PICKLE, ', file)
    with open(file, 'wb') as f:
        pickle.dump(var, f)