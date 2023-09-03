import unittest
from typing import Generator

from ovos_skill_tunein import TuneInSkill

MEDIA_KEYS = ["match_confidence", "media_type", "uri", "playback", "image",
              "bg_image", "skill_icon", "title", "artist", "author", "length"]


class TestSkill(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.skill = TuneInSkill()
    
    def test_featured_media(self):
        fm = self.skill.featured_media()
        self.assertTrue(isinstance(fm, list))
        self.assertTrue(len(fm) > 0)
        self.assertTrue(isinstance(fm[0], dict))
        self.assertTrue(all([k in fm[0] for k in MEDIA_KEYS]))
        self.assertTrue(fm[0]["media_type"].name == "RADIO")
        self.assertTrue(fm[0]["playback"].name == "AUDIO")
    
    def test_search(self):
        stations = self.skill.search_tunein("radio NPR", None)
        self.assertTrue(isinstance(stations, Generator))
        station = next(stations)
        self.assertTrue(all([k in station for k in MEDIA_KEYS]))
        self.assertTrue(station["media_type"].name == "RADIO")
        self.assertTrue(station["playback"].name == "AUDIO")


if __name__ == "__main__":
    unittest.main()
