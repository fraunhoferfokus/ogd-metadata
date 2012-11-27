#!/usr/bin/python
import sys,json,collections,string
reload(sys)
sys.setdefaultencoding('utf-8')
schema=open('../OGPD_JSON_Schema.json', 'r')
data=json.loads( schema.read(), object_pairs_hook=collections.OrderedDict)
schema.close()


def splitDescription(d):
	if ": " in d:
		return  d.split(": ")
	else:
		return [d, d]

def getPattern(prop):
	if 'array' == prop['type']:
		prop = prop['items']
	if 'pattern' in prop.keys():
		return '(%s)' % prop['pattern']
	if 'format' in prop.keys():
		if 'uri' == prop['format']:
			return '(%s)' % 'URI'
		return '(%s)' % prop['format']
	if 'string' == prop['type'] and 'enum' in prop.keys():
		return '(Enum aus: %s)' % ', '.join(prop['enum'])
	return ''

# return the html string and the amount of table rows that were generated
def renderProperties(object, level):
	out = []
	rows = 0
	for propKey, prop in object["properties"].iteritems():
		subobjects = ''
		subrows = 0
		if 'object' == prop['type']:
			[subobjects, subrows ] = renderProperties(prop, level+1)
		if 'array' == prop['type'] and 'object' == prop['items']['type']:
			[subobjects, subrows ] = renderProperties(prop['items'], level+1)
		rows = rows + 1 + subrows
		[fieldName, description] = splitDescription(prop["description"])
		out.append("od.%s.name = %s\n" % (propKey, fieldName))
		out.append("od.%s.description = %s %s\n\n" % (propKey, description, getPattern(prop)))
		out.append(subobjects)
	return [''.join(out), rows]


	
[tableBody, rows] = renderProperties(data, 1)
print tableBody


