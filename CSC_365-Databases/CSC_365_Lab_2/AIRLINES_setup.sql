DROP TABLE flights;
DROP TABLE airlines;
DROP TABLE airports;

CREATE TABLE airlines(
    Id INTEGER,
    Airline VARCHAR(25),
    Abbreviation VARCHAR(25) UNIQUE,
    Country CHAR(10),
    PRIMARY KEY (Id, Airline)
);

CREATE TABLE airports(
    City VARCHAR(15),
    AirportCode VARCHAR(10) UNIQUE,
    AirportName VARCHAR(50),
    Country VARCHAR(15),
    CountryAbbrev CHAR(10)
);

CREATE TABLE flights(
    Airline INTEGER,
    FlightNo INTEGER,
    SourceAirport VARCHAR(10),
    DestAirport VARCHAR(10) NOT NULL,
    PRIMARY KEY (Airline, FlightNo),
    FOREIGN KEY (SourceAirport) REFERENCES airports(AirportCode),
    FOREIGN KEY (DestAirport) REFERENCES airports(AirportCode),
    FOREIGN KEY (Airline) REFERENCES airlines(Id)
);