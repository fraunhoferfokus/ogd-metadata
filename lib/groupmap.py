import json, urllib2

class Translator:
	map = {}
	
	def __init__(self, sourceportal):
		filename = "../kategorien/" + sourceportal + "2deutschland.json"
		self.map = json.loads( open(filename, 'r').read())
	
	def translate(self, categories=[]):
		if not isinstance(categories, list):
			categories = [categories]
		out = []
		if not categories:
			return out 
		for cat in categories:
			if cat in self.map.keys():
				out = out + self.map[cat]
		return out



import unittest
class TestMapping(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.u = Translator('berlin')
	
	def test_b2d(self):
		translated = self.u.translate(['verkehr','wahl'])
		print translated
		self.assertEqual(translated, ['transport_verkehr','politik_wahlen'])

	def test_atom(self):
		translated = self.u.translate('verkehr')
		print translated
		self.assertEqual(translated, ['transport_verkehr'])

	def test_missing(self):
		translated = self.u.translate(['verkehr','xyz','wahl'])
		print translated
		self.assertEqual(translated, ['transport_verkehr','politik_wahlen'])

	def test_empty(self):
		translated = self.u.translate()
		print translated
		self.assertEqual(translated, [])

	def test_none(self):
		translated = self.u.translate(None)
		print translated
		self.assertEqual(translated, [])

if __name__ == '__main__':
	unittest.main()
	
