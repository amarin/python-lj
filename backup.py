# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import pickle
import html
from datetime import datetime
from jinja2 import Template
from zipfile import ZipFile, ZIP_DEFLATED



class LjRecord(object):

    def __init__(self, imported_dict):
        self.data = imported_dict

    @staticmethod
    def decode_string(data_name, data):
        if isinstance(data, str):
            return bytes(data, 'utf-8').decode('utf-8')

        elif isinstance(data, bytes):
            return data.decode('utf-8')

        else:
            raise RuntimeError(
                "Unexpected type %s in %s" % (
                    type(data).__name__,
                    data_name
                )
            )

    @property
    def content(self):
        content = ''
        try:
            content = html.unescape(self.data['event'].data.decode('utf-8'))
        except:
            content = html.unescape(self.data['event'])

        content = content.replace('<lj-cut>', '')
        return content

    @property
    def subject(self):
        if 'subject' in self.data:
            return self.decode_string('subject', self.data['subject'].data)
        else:
            return ''

    @property
    def tags(self):
        if 'taglist' in self.data['props']:
            return self.decode_string(
                'taglist', self.data['props']['taglist'].data
            )
        else:
            return ''

    @property
    def posting_datetime_string(self):
        if isinstance(self.data['eventtime'], str):
            evt_datetime = datetime.strptime(
                self.data['eventtime'],
                '%Y-%m-%d %H:%M:%S'
            )
            return evt_datetime
        else:
            raise RuntimeError(
                "Unexpected eventtime %s" % type(
                    self.data['eventtime']
                ).__name__
            )

    @property
    def url(self):
        return self.data['url']


with open('/Users/amarin/dev/python-lj/kangaroo_mouse.pkl', 'rb') as pd:
    data = pickle.load(pd)
# print(type(data))

# for k, v in data['entries'][1].items():
#     print("%s %s" % (k, type(v)))

entries = [LjRecord(v) for v in data['entries'].values()]
entries_with_tags = [x for x in entries if '<' in x.content]

v = entries_with_tags[1]
# print("\nДата/время: ", v.posting_datetime_string)
# print("URL: ", v.url)
# print("Заголовок: ", v.subject)
# print(v.content)
# print("\nТэги: ", v.tags)
# print("Anum: ", v.data['anum'], '/', v.data['itemid'])
# print(v.data['props'])

print("Loading template")
template_path = os.path.join(
    os.path.dirname(__file__), 'template.html'
)
template_tgt = os.path.join(
    os.path.dirname(__file__), 'document.html'
)

with open(template_path, 'rb') as template_fh:
    template = Template(template_fh.read().decode('utf-8'))

output_text = template.render(posts=entries_with_tags)

with open(template_tgt, 'wb') as output_fh:
    output_fh.write(output_text.encode())





# for k, v in v['props'].items():
#     print("%s %s" % (k, type(v)))
