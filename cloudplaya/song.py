class Song(object):
    COLUMNS = [
        'albumArtistName', 'albumName', 'artistName', 'assetType',
        'duration', 'objectId', 'sortAlbumArtistName', 'sortAlbumName',
        'sortArtistName', 'title', 'status', 'trackStatus', 'extension',
        'asin', 'trackNum', 'discNum', 'albumReleaseDate',
    ]

    def __init__(self, client, payload):
        self.client = client

        metadata = payload['metadata']
        self.id = metadata['objectId']
        self.asset_type = metadata['assetType']
        self.title = metadata['title']
        self.asin = metadata.get('asin', None)
        self.status = metadata['status']
        self.duration = metadata['duration']
        self.extension = metadata['extension']
        self.album_name = metadata['albumName']
        self.album_release_date = metadata.get('albumReleaseDate', None)
        self.artist_name = metadata['artistName']
        self.album_artist_name = metadata['albumArtistName']
        self.track_num = int(metadata.get('trackNum', 0))
        self.disc_num = int(metadata.get('discNum', 0))
        self.sort_album_artist_name = metadata['sortAlbumArtistName']
        self.sort_album_name = metadata['sortAlbumName']

        self._metadata = None

    def get_stream_url(self):
        return self.client.get_song_stream_urls([self.id])[0]

    def populate_metadata(self):
        """Fetches the reference metadata as a dictionary."""
        md_list = self.client.get_song_track_metadata([self.asin])
        if md_list:
            self._metadata = md_list[0]

    def update_metadata(self):
        if not self._metadata:
            self.populate_metadata()
        metadata = self._metadata
        self.client.update_song_metadata(self.id, metadata)

    def __repr__(self):
        return '<Song "%s">' % self.title

    def __str__(self):
        return self.title
