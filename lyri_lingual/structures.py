"""Data structures for various purposes."""

from dataclasses import dataclass


@dataclass
class TrackData:
    """
    Dataclass to hold relevant track data.

    :ivar id: Track ID (for Musixmatch API).
    :ivar title: Track title.
    :ivar artist: Track Artist(s).
    :ivar album: Track album.
    :ivar genre: Track genre.
    """

    id: int
    title: str
    artist: str
    album: str
    genre: str  # TODO: may define as an enum later

    @property
    def lyrics(self) -> str:
        """Getter for track lyrics.

        :return: Track lyrics.
        """
        from lyri_lingual.api import get_lyrics_from_id

        return get_lyrics_from_id(self.id)
