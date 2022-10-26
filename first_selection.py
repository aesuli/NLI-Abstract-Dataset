import os
import pickle
import sys
import tarfile
import zlib
from json import JSONDecoder

from tqdm.auto import tqdm


def get_records(filename):
    json_decoder = JSONDecoder()

    with tarfile.open(filename) as tar_file:
        for tarred_file_info in tar_file:
            with tar_file.extractfile(tarred_file_info) as tarred_file:
                gzip_data = tarred_file.read()
            json_data = zlib.decompress(gzip_data, zlib.MAX_WBITS | 16).decode('utf-8')
            pos = 0
            while True:
                if pos == len(json_data):
                    break
                while json_data[pos].isspace():
                    pos += 1
                    if pos == len(json_data):
                        break
                if pos == len(json_data):
                    break
                record, pos = json_decoder.raw_decode(json_data, pos)
                yield record


if __name__ == '__main__':
    data_dir = sys.argv[1]

    output_filename = 'first_selection.pkl'

    overwrite = False

    if os.path.exists(output_filename) and not overwrite:
        raise Exception(f'File {output_filename} already exists.')

    with open(output_filename, mode='wb') as output_file:
        filecount = 10
        selected = 0
        for i in range(filecount):
            filename = data_dir + f'/publication_{i + 1}.tar'
            print(filename)
            for record in tqdm(get_records(filename)):
                try:
                    author = record['author']
                    if len(author) != 1:
                        continue
                    author = author[0]

                    description = record['description']
                    if not 0<len(description)<3:
                        continue

                    publication_types = set(instance['type'] for instance in record['instance'])
                    if len(publication_types) != 1:
                        continue
                    (publication_type,) = publication_types

                    language_dict = record['language']
                    language_code = language_dict['code'].lower()
                    language_label = language_dict['label'].lower()
                    if language_code == 'und' or language_label == 'undetermined':
                        continue

                    country = [country['code'].lower() for country in record['country']]

                    pickle.dump((author, publication_type, language_label, language_code, country, description),
                                output_file)
                    selected += 1
                except KeyError:
                    continue
        print(f'{selected} records passed the first selection')
