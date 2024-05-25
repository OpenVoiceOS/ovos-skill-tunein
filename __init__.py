from os.path import join, dirname


from ovos_utils.ocp import MediaType, PlaybackType
from ovos_utils.log import LOG
from ovos_workshop.decorators import ocp_search, ocp_featured_media
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill
from tunein import TuneIn
from pyradios import RadioBrowser


class TuneInSkill(OVOSCommonPlaybackSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(supported_media = [MediaType.RADIO],
                         skill_icon=join(dirname(__file__), "res", "tunein.png"),
                         *args, **kwargs)
    
    @ocp_featured_media()
    def featured_media(self):
        return [{
            "match_confidence": 90,
            "media_type": MediaType.RADIO,
            "uri": ch.stream,
            "playback": PlaybackType.AUDIO,
            "image": ch.image,
            "bg_image": ch.image,
            "skill_icon": self.skill_icon,
            "title": ch.title,
            "artist": ch.artist,
            "author": "TuneIn",
            "length": 0
        } for ch in TuneIn.featured()]

    @ocp_search()
    def search_tunein(self, phrase, media_type):
        base_score = 0

        if media_type == MediaType.RADIO or self.voc_match(phrase, "radio"):
            base_score += 30
        else:
            base_score -= 30

        if self.voc_match(phrase, "tunein"):
            base_score += 50  # explicit request
            phrase = self.remove_voc(phrase, "tunein")

        # Try quick search with PyRadios
        LOG.debug(f"Searching PyRadios for '{phrase}'...")
        for item in self.search_pyradios(phrase, media_type):
           yield item

        LOG.debug(f"Searching TuneIn for '{phrase}'...")
        for ch in TuneIn.search(phrase):
            score = base_score + ch.match(phrase)
            if self.voc_match(ch.title, "radio"):
                score += 5
            yield {
                "match_confidence": min(100, score),
                "media_type": MediaType.RADIO,
                "uri": ch.stream,
                "playback": PlaybackType.AUDIO,
                "image": ch.image,
                "bg_image": ch.image,
                "skill_icon": self.skill_icon,
                "title": ch.title,
                "artist": ch.artist,
                "author": "TuneIn",
                "length": 0
            }

    def search_pyradios(self, phrase, media_type):
       """Search radio with PyRadios."""
       base_score = 0
       radio_browser = RadioBrowser()
       
       if media_type == MediaType.RADIO or self.voc_match(phrase, "radio"):
           base_score += 30
       else:
           base_score -= 30

       if self.voc_match(phrase, "tunein"):
           base_score += 50  # explicit request
           phrase = self.remove_voc(phrase, "tunein")

       for ch in radio_browser.search(name=phrase.replace('radio', '').strip()):
           score = base_score + int(ch["name"] in phrase) * 80
           yield {
               "match_confidence": min(100, score),
               "media_type": MediaType.RADIO,
               "uri": ch["url_resolved"],
               "playback": PlaybackType.AUDIO,
               "image": ch["favicon"],
               "bg_image": "",  # TODO: which image to add here?
               "skill_icon": self.skill_icon,
               "title": ch["name"],
               "artist": ch["name"],
               "author": "PyRadios",
               "length": 0
           }
