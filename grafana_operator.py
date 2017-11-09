#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import urllib2
import base64
import json
import glob

# argparse
parser = argparse.ArgumentParser(description='Grafana Operator')
parser.add_argument('--url', required=True, help='grafana url (example: --url http://127.0.0.1:3000)')
parser.add_argument('--action', required=True, help='grafana action (example: --action enable|export|import)')
parser.add_argument('--app', required=False, help='app id (example: --app your_add_id')
args = parser.parse_args()

# variables
pass_hash = base64.encodestring("admin:admin").replace('\n', '')
url = args.url
action = args.action
if args.app:
    app = args.app
else:
    app = 'your_app_id'


def request(url, method, data=None):
    request = urllib2.Request(url)
    request.add_header('Authorization', 'Basic {0}'.format(pass_hash))
    request.get_method = lambda: method
    if data:
        request.add_header('Content-Type', 'application/json')
        request.add_data(data)
        resp = None
        try:
            resp = urllib2.urlopen(request)
        except Exception as err:
            print("=== request Exception ===")
            print(url)
            print(err)
        return resp


def enable_app(app):
    return request(url='{0}/api/plugins/{1}/settings'.format(url, app),
                   method='POST',
                   data=json.dumps({'enabled': True, 'pinned': True}))


def disable_app(app):
    return request(url='{0}/api/plugins/{1}/settings'.format(url, app),
                   method='POST',
                   data=json.dumps({'enabled': False, 'pinned': False}))


def get_dashboards(app):
    return request(url='{0}/api/plugins/{1}/dashboards'.format(url, app),
                   method='GET')


def delete_dashboard(dashboard):
    return request(url='{0}/api/dashboards/{1}'.format(url, dashboard),
                   method='DELETE')


def export_dashboards():
    dbs = request(url='{0}/api/search'.format(url), method='GET').read()
    try:
        for i in json.loads(dbs):
            with open(i['title'].encode('utf-8') + '.json', 'w') as target:
                resp = request(url='{0}/api/dashboards/{1}'.format(url, i['uri'].encode('utf-8')), method='GET')
                content = json.loads(resp.read())
                content['overwrite'] = True
                content['dashboard']['id'] = 'null'
                target.truncate()
                target.write(json.dumps(content))
                print("Done! --- export dashboard: {0}.json".format(i['title'].encode('utf-8')))
    except Exception as err:
        print("=== export_dashboards Exception ===")
        print(err)


def import_dashboards():
    try:
        for f in glob.glob('*.json'):
            with open(f) as content:
                resp = request(url='{0}/api/dashboards/db'.format(url),
                               method='POST',
                               data=content.read())
                if resp and resp.code == 200:
                    print("Done! --- import dashboard: {0}".format(f))
    except Exception as err:
        print("=== import_dashboards Exception ===")
        print(err)


def main():
    if action == 'enable':
        print('disable app: ' + disable_app(app).read())
        print('enable app: ' + enable_app(app).read())
        if app == 'monitors':
            data = json.load(get_dashboards(app))
            for i in data:
                print('delete dashboard: ' + delete_dashboard(i['importedUri']).read())
        elif action == 'export':
            export_dashboards()
        elif action == 'import':
            import_dashboards()


if __name__ == '__main__':
    main()

