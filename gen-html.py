#!/usr/bin/python
# -*- coding: utf8 -*-
import sys,json,collections,string
reload(sys)
sys.setdefaultencoding('utf-8')
schema=open('OGPD_JSON_Schema.json', 'r')
data=json.loads( schema.read(), object_pairs_hook=collections.OrderedDict)
schema.close()

def cell(content='', rowspan=1):
	return '<td rowspan="{1}">{0}</td>'.format(content, rowspan)

def renderType(property):
	literal = property['type']
	if 'array' == literal:
		return 'Liste von ' + string.capwords(property['items']['type'])
	else:
		return string.capwords(literal)

def required(property):
	if 'required' in property.keys():
		return property['required']
	return False

def splitDescription(d):
	if ": " in d:
		return  d.split(": ")
	else:
		return [d, d]

def getPattern(prop):
	if 'array' == prop['type']:
		prop = prop['items']
	if 'pattern' in prop.keys():
		return prop['pattern']
	if 'format' in prop.keys():
		if 'uri' == prop['format']:
			return 'URI'
		return prop['format']
	if 'string' == prop['type'] and 'enum' in prop.keys():
		return 'Enum aus: ' + ', '.join(prop['enum'])
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
		out.append("<tr>")
		out.append(cell(fieldName))
		out.append(cell(propKey,subrows+1))
		for i in range (3-level):
			out.append(cell(''))
		out.append(cell('X' if required(prop) else ''))
		out.append(cell(renderType(prop)))
		out.append(cell(getPattern(prop)))
		out.append(cell(description))
		out.append('</tr>\n')
		out.append(subobjects)
	return [''.join(out), rows]


def tableStart():
	print """
<html><head>
<meta http-equiv=Content-Type content="text/html; charset=UTF-8">
<style type="text/css">
<!--
td {vertical-align:top;}
-->
</style>
</head><body>
<table border=1 cellpadding=0 cellspacing=0  style="empty-cells:show;vertical-align:top">
 <col > <col  span=3><col ><col ><col ><col >
 <tr>
  <th rowspan=2 >Metadaten Eintrag</th>
  <th colspan=3 >JSON Bezeichner</th>
  <th rowspan=2 >Pflichtfeld</th>
  <th rowspan=2 >Datentyp</th>
  <th rowspan=2 >Format / Pattern</th>
  <th rowspan=2 >Beschreibung</th>
 </tr>
 <tr>
  <th >1.
  Ebene (CKAN nativ)</th>
  <th >2. Ebene</th>
  <th >3. Ebene</th>
 </tr>
"""

def tableEnd():
	print "</table></body></html>"

	
tableStart()
[tableBody, rows] = renderProperties(data, 1)
print tableBody
tableEnd()


def listTable(name, content):
	print """
<p><table border=1 cellpadding=0 cellspacing=0
 style='border-collapse:collapse;table-layout:fixed'>
 <col>
<tr><th colspan='2'>{0}</th></tr> 
<tr><th>ID</th><th>Titel</th></tr> 
{1}
</table>
""".format(name, content)

def listBody(list):
	out = []
	for id, title in list.iteritems():
		out.append('<tr><td>{0}</td><td>{1}</td></tr>\n'.format(id,title))
	return ''.join(out)

def listLicenseTable(list):
	out = ["""
<p><table border=1 cellpadding=0 cellspacing=0
 style='border-collapse:collapse;table-layout:fixed'>
 <col>
<tr><th colspan='4'>Lizenzen</th></tr> 
<tr><th>ID</th><th>Titel</th><th>URL</th><th>Klassifizierung</th><th>Für Daten/Inhalte</th><th>Für Apps</th></tr>
"""]
	for license in list:
		is_open         = 'offen' if license['is_osi_compliant'] or license['is_okd_compliant'] else 'eingeschränkt'
		domain_data     = 'X' if license['domain_content'] or license['domain_data'] else ''
		domain_software = 'X' if license['domain_software'] else ''
		out.append('<tr><td>{0}</td><td>{1}</td><td><a href="{2}">{2}</a></td><td>{3}</td><td>{4}</td><td>{5}</td></tr>\n'.format(license['id'],license['title'],license['url'],is_open,domain_data,domain_software))
	out.append('</table>')
	return ''.join(out)

f=open('kategorien/deutschland.json', 'r')
kat=json.loads( f.read(), object_pairs_hook=collections.OrderedDict)
f.close()
listTable('Kategorien', listBody(kat))

f=open('lizenzen/deutschland.json', 'r')
licences=json.loads( f.read(), object_pairs_hook=collections.OrderedDict)
f.close()
print listLicenseTable(licences)

