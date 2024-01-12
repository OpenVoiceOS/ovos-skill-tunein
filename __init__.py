from os.path import join, dirname

from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    MediaType, PlaybackType, ocp_search, ocp_featured_media
from tunein import TuneIn


class TuneInSkill(OVOSCommonPlaybackSkill):
    def __init__(self, *args, **kwargs):
        self.supported_media = [MediaType.RADIO]
        self.skill_icon = join(dirname(__file__), "res", "tunein.png")
        super().__init__(*args, **kwargs)
    
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
