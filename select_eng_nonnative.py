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
    output_filename = 'eng_nonnative.pkl'

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
            if len(description) == 2 \
                    and min_description_len <= len(description[0]) <= max_description_len \
                    and publication_type in publication_type_to_keep:
                description_0_lang = py3langid.classify(description[0])[0]
                description_1_lang = py3langid.classify(description[1])[0]
                if description_0_lang == description_1_lang:
                    continue
                if description_0_lang == 'en' or description_1_lang == 'en':
                    if description_0_lang == 'en':
                        native_lang = description_1_lang
                        eng_description = description[0]
                        native_description = description[1]
                    if description_1_lang == 'en':
                        native_lang = description_0_lang
                        eng_description = description[1]
                        native_description = description[0]
                    native_lang_counter.update([('2', publication_type, native_lang)])
                    native_lang_counter.update([('L', native_lang)])
                    native_lang_counter.update([('P', publication_type)])
                    pickle.dump(
                        (author['fullname'], native_lang, publication_type, eng_description, native_description),
                        output_file)
                    selected += 1

        print(f'{selected} records passed the second selection as nonnative english')
        print(sorted(native_lang_counter.items(),
                     key=lambda x: (x[0][0], '_', x[1]) if len(x[0]) == 2 else (x[0][0], x[0][2], x[1]),
                     reverse=True))
