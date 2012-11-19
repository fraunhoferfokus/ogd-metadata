import json, urllib2

class Util:

    def translate(self, categories, sourceportal):
        url = "https://github.com/fraunhoferfokus/ogd-metadata/raw/master/kategorien/" + sourceportal + "2deutschland.json"
        map = json.loads( urllib2.urlopen(url).read())
        out = []
        for cat in categories:
            if cat in map.keys():
                out = out + map[cat]
        return out


import unittest
class TestMapping(unittest.TestCase):

    
    def test_b2d(self):
        u = Util()
        translated = u.translate(['verkehr','wahl'], 'berlin')
        print translated
        self.assertEqual(translated, ['transport_verkehr','politik_wahlen'])

    def test_missing(self):
        u = Util()
        translated = u.translate(['verkehr','xyz','wahl'], 'berlin')
        print translated
        self.assertEqual(translated, ['transport_verkehr','politik_wahlen'])


if __name__ == '__main__':
    unittest.main()
    
