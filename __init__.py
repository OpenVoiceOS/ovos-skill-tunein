from os.path import join, dirname

from ovos_workshop.backwards_compat import MediaType, PlaybackType, Playlist, MediaEntry
from ovos_workshop.decorators import ocp_search, ocp_featured_media
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill
from tunein import TuneIn


class TuneInSkill(OVOSCommonPlaybackSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(supported_media=[MediaType.RADIO],
                         skill_icon=join(dirname(__file__), "tunein.png"),
                         *args, **kwargs)

    @ocp_featured_media()
    def featured_media(self):
        pl = Playlist(media_type=MediaType.RADIO,
                      title="TuneIn (Featured Stations)",
                      playback=PlaybackType.AUDIO,
                      skill_id=self.skill_id,
                      artist="TuneIn",
                      match_confidence=100,
                      skill_icon=self.skill_icon)
        pl += [MediaEntry(media_type=MediaType.RADIO,
                          uri=ch.direct_stream,
                          title=ch.title,
                          playback=PlaybackType.AUDIO,
                          image=ch.image,
                          skill_id=self.skill_id,
                          artist=ch.artist,
                          match_confidence=90,
                          length=-1,  # live stream
                          skill_icon=self.skill_icon)
               for ch in TuneIn.featured()]
        return pl

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
            yield MediaEntry(media_type=MediaType.RADIO,
                             uri=ch.stream,
                             title=ch.title,
                             playback=PlaybackType.AUDIO,
                             image=ch.image,
                             skill_id=self.skill_id,
                             artist=ch.artist,
                             match_confidence=min(100, score),
                             length=-1,  # live stream
                             skill_icon=self.skill_icon)


if __name__ == "__main__":
    from ovos_utils.messagebus import FakeBus
    from ovos_utils.log import LOG

    LOG.set_level("DEBUG")

    s = TuneInSkill(bus=FakeBus(), skill_id="t.fake")
    for r in s.search_tunein("secret agent", MediaType.RADIO):
        print(r)
        # MediaEntry(uri='http://ice6.somafm.com/secretagent-128-mp3', title='SomaFM: Secret Agent', artist='SomaFM: Secret Agent', match_confidence=100, skill_id='t.fake', playback=<PlaybackType.AUDIO: 2>, status=<TrackState.DISAMBIGUATION: 1>, media_type=<MediaType.RADIO: 7>, length=-1, image='http://cdn-profiles.tunein.com/s2593/images/logoq.jpg', skill_icon='/home/miro/PycharmProjects/OCPSkills/skill-ovos-tunein/res/tunein.png', javascript='')
