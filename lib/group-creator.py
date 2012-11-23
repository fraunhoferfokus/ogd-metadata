#!/usr/bin/python
# -*- coding: utf8 -*-
import traceback,pprint,sys
import ckanclient #developed with ckanclient 0.10
reload(sys)
sys.setdefaultencoding('utf-8')

import ckanclient
import json
import argparse
import groupmap

pp=pprint.PrettyPrinter(indent=4)
parser = argparse.ArgumentParser(description='Create group/subgroup structur.')
parser.add_argument('--ckanurl', help='ckan url', required=True)
parser.add_argument('--apikey', help='ckan api key, eg localhost:5000/api')
parser.add_argument('--domain', help='ID for a group of domains like "iso" or "berlin".', required=True)
args = parser.parse_args()


# Instantiate the CKAN client.
ckan = ckanclient.CkanClient(base_location=args.ckanurl, api_key=args.apikey)
pp=pprint.PrettyPrinter(indent=4)

filename = "../kategorien/" + args.domain + ".json"
groups = json.loads( open(filename, 'r').read())
transl = groupmap.Translator(args.domain)

for gid in groups.iterkeys():
	group_entity = {
	    'name': gid,
	    'title': groups[gid]
	}
	if not 'deutschland' == args.domain:
		group_entity['type'] = 'subgroup'

# 	try:
# 		ckan.group_register_post(group_entity)
# 	except:
# 		traceback.print_exc()

	if not 'deutschland' == args.domain:
		for supergroupname in transl.translate(gid):
			print supergroupname
			supergroup =  ckan.group_entity_get(supergroupname)
			supergroup['groups'] = [{'name':gid}] + supergroup['groups']
			try:
				ckan.group_register_post(supergroup)
			except:
				traceback.print_exc()
