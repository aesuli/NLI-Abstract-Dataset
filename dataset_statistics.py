import sys
import tarfile
import zlib
from collections import Counter, defaultdict
from json import JSONDecoder


def get_records(filename):
    json_decoder = JSONDecoder()

    with tarfile.open(filename) as tar_file:
        for tarred_file_info in tar_file:
            with tar_file.extractfile(tarred_file_info) as tarred_file:
                gzip_data = tarred_file.read()
            json_data = zlib.decompress(gzip_data, zlib.MAX_WBITS | 16).decode()
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

    filecount = 10
    keys_counter = Counter()
    value_counters = defaultdict(Counter)
    for i in range(filecount):
        filename = data_dir + f'/publication_{i + 1}.tar'
        print(filename)
        for record in get_records(filename):
            keys = list(record.keys())
            keys_counter.update(keys)
            for key in keys:
                value = record[key]
                if key == 'bestaccessright':
                    pass
                elif key == 'language':
                    value_counters[key+'_code'].update([value['code'].lower()])
                    value_counters[key+'_label'].update([value['label'].lower()])
                elif key == 'author':
                    value_counters[key].update([len(value)])
                elif key == 'container':
                    pass
                elif key == 'contributor':
                    pass
                elif key == 'country':
                    for country in value:
                        value_counters[key].update([country['code'].lower()])
                elif key == 'coverage':
                    pass
                elif key == 'dateofcollection':
                    pass
                elif key == 'description':
                    for piece in value:
                        value_counters[key].update([len(piece)])
                elif key == 'embargoenddate':
                    pass
                elif key == 'format':
                    pass
                elif key == 'id':
                    pass
                elif key == 'instance':
                    for instance in value:
                        value_counters[key].update([instance['type'].lower()])
                elif key == 'lastupdatetimestamp':
                    pass
                elif key == 'maintitle':
                    value_counters[key].update([len(value)])
                elif key == 'originalId':
                    pass
                elif key == 'pid':
                    pass
                elif key == 'publicationdate':
                    pass
                elif key == 'publisher':
                    pass
                elif key == 'source':
                    pass
                elif key == 'subjects':
                    pass
                elif key == 'subtitle':
                    pass
                elif key == 'type':
                    pass
                else:
                    raise Exception(key)

    print(keys_counter)

    print()
    print('*' * 10)
    print()

    for key in value_counters:
        print(key, len(value_counters[key]))

    print()
    print('*' * 10)
    print()

    for key in value_counters:
        print(key, value_counters[key])
        print()
        print('#' * 10)
        print()
