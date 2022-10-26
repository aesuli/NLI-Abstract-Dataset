import os
import pickle
from collections import Counter

import py3langid
from tqdm.auto import tqdm


def get_records(input_file):
    try:
        while True:
            yield pickle.load(input_file)
    except EOFError:
        pass


if __name__ == '__main__':
    output_filename = 'eng_native.pkl'

    min_description_len = 300
    max_description_len = 3000
    publication_type_to_keep = {'Article', 'Conference object', 'Preprint', 'Doctoral thesis', 'Master thesis',
                                'Thesis', 'Bachelor thesis'}

    overwrite = False

    if os.path.exists(output_filename) and not overwrite:
        raise Exception(f'File {output_filename} already exists.')

    native_lang_counter = Counter()

    with open('first_selection.pkl', mode='rb') as input_file, \
            open(output_filename, mode='wb') as output_file:
        selected = 0
        for (author, publication_type, language_label, language_code, country, description) in tqdm(
                get_records(input_file)):
            if language_label == 'english' \
                    and len(description) == 1 \
                    and min_description_len <= len(description[0]) <= max_description_len \
                    and len(country) == 1 \
                    and country[0] == 'gb' \
                    and publication_type in publication_type_to_keep:
                description_lang = py3langid.classify(description[0])
                if description_lang[0] == 'en':
                    native_lang_counter.update([('2', publication_type, 'en')])
                    native_lang_counter.update([('L', 'en')])
                    native_lang_counter.update([('P', publication_type)])
                    pickle.dump((author['fullname'], 'en', publication_type, description), output_file)
                    selected += 1

        print(f'{selected} records passed the second selection as native english')
        print(native_lang_counter)
