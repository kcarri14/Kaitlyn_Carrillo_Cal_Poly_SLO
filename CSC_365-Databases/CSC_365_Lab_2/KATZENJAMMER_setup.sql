DROP TABLE Tracklists;
DROP TABLE Instruments;
DROP TABLE Performance;
DROP TABLE Vocals;
DROP TABLE Albums;
DROP TABLE Bands;
DROP TABLE Songs;


CREATE TABLE Albums(
    AId INTEGER PRIMARY KEY,
    Title VARCHAR(40),
    Year INTEGER,
    Label VARCHAR(30),
    Type VARCHAR(30)
);

CREATE TABLE Band(
    Id INTEGER PRIMARY KEY,
    Lastname VARCHAR(15),
    Firstname VARCHAR(15)
);

CREATE TABLE Songs(
    SongId INTEGER PRIMARY KEY,
    Title VARCHAR(40)
);


CREATE TABLE Instruments(
    SongId INTEGER, 
    BandmateId INTEGER, 
    Instrument VARCHAR(15),
    PRIMARY KEY (SongId, BandmateId, Instrument),
    FOREIGN KEY (SongId) REFERENCES Songs(SongId),
    FOREIGN KEY (BandmateId) REFERENCES Band(Id)
);

CREATE TABLE Performance(
    SongId INTEGER, 
    Bandmate INTEGER, 
    StagePosition VARCHAR(15),
    PRIMARY KEY (SongId, Bandmate),
    FOREIGN KEY (SongId) REFERENCES Songs(SongId),
    FOREIGN KEY (Bandmate) REFERENCES Band(Id)
);



CREATE TABLE Tracklists(
    AlbumId INTEGER, 
    Position INTEGER,
    SongId INTEGER, 
    PRIMARY KEY (AlbumId, SongId),
    FOREIGN KEY (SongId) REFERENCES Songs(SongId),
    FOREIGN KEY (AlbumId) REFERENCES Albums(AId)
);

CREATE TABLE Vocals(
    SongId INTEGER, 
    Bandmate INTEGER, 
    Type VARCHAR(15),
    PRIMARY KEY (SongId, Bandmate),
    FOREIGN KEY (SongId) REFERENCES Songs(SongId),
    FOREIGN KEY (Bandmate) REFERENCES Band(Id)
);