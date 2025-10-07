import gzip
import re


#TODO class input dir_name



def _read():

    with gzip.open(r'data\nginx-access-ui.log-20170630.gz', 'rt', encoding='utf-8') as f:
        for line in f:
            yield line.strip()

        # content = f.readlines(-1)
        # return content

