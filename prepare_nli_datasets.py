import os
import pickle
from collections import defaultdict

import numpy as np
from tqdm.auto import tqdm


def get_records(input_file):
    try:
        while True:
            yield pickle.load(input_file)
    except EOFError:
        pass


if __name__ == '__main__':
    input_filename_native = 'eng_native.pkl'
    output_filename_native = 'openaire_en_native.pkl'
    input_filename_nonnative = 'eng_nonnative.pkl'
    output_filename_nonnative = 'openaire_en_nonnative.pkl'

    MAX_COUNT = 10000

    languages_to_keep = {'en', 'tr', 'de', 'es', 'lv', 'it', 'fr', 'pt', 'ru', 'nl', 'ja', 'pl', 'fi', 'da'}

    overwrite = True

    if os.path.exists(output_filename_native) and not overwrite:
        raise Exception(f'File {output_filename_native} already exists.')

    if os.path.exists(output_filename_nonnative) and not overwrite:
        raise Exception(f'File {output_filename_nonnative} already exists.')

    with open(input_filename_native, mode='rb') as input_file, \
            open(output_filename_native, mode='wb') as output_file:
        X = list()
        for (author, native_lang, publication_type, description) in tqdm(
                get_records(input_file)):
            if native_lang != 'en':
                raise ValueError(f'Unexpected language {native_lang}')
            X.append(description[0])
        selection = np.random.choice(len(X),MAX_COUNT,False)
        X = [X[id] for id in selection]
        print(len(X))
        pickle.dump(X, output_file)
        pickle.dump(['en']*len(X), output_file)

    with open(input_filename_nonnative, mode='rb') as input_file, \
            open(output_filename_nonnative, mode='wb') as output_file:
        Xs = defaultdict(list)
        for (author, native_lang, publication_type, eng_description, native_description) in tqdm(
                get_records(input_file)):
            if native_lang in languages_to_keep:
                Xs[native_lang].append(eng_description)
        X = list()
        y = list()
        for native_lang in Xs:
            selection = np.random.choice(len(Xs[native_lang]),min(len(Xs[native_lang]),MAX_COUNT),False)
            print(native_lang,len(selection))
            X.extend([Xs[native_lang][id] for id in selection])
            y.extend([native_lang]*len(selection))
        print(len(X))
        pickle.dump(X, output_file)
        pickle.dump(y, output_file)
