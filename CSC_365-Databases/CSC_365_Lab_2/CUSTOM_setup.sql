DROP TABLE albums_and_songs;
DROP TABLE all_songs;
DROP TABLE albums;

CREATE TABLE albums (
    album_name VARCHAR(50) PRIMARY KEY,
    ep VARCHAR(15),
    album_release DATE
);

CREATE TABLE albums_and_songs (
    album_name VARCHAR(50),
    ep VARCHAR(15),
    album_release DATE,
    track_number INTEGER,
    track_name VARCHAR(100),
    artist VARCHAR(50),
    PRIMARY KEY (album_name, track_name, artist),
    FOREIGN KEY (album_name) REFERENCES albums(album_name)
);

CREATE TABLE all_songs (
    album_name VARCHAR(50),
    ep VARCHAR(15),
    album_release DATE,
    track_number INTEGER,
    track_name VARCHAR(100),
    artist VARCHAR(50),
    PRIMARY KEY (album_name, track_name, artist)
);
