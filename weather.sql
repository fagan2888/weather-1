CREATE TABLE observation(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clothingLayers INTEGER,
    humidity INTEGER,
    pressure INTEGER,
    rainfall REAL,
    temperature REAL,
    time TEXT,
    windChill INTEGER,
    windDirection INTEGER,
    windGustSpeed INTEGER,
    windSpeed INTEGER
);

-- wind speed is in km/h
-- all temperatures are measured in celsius
-- time is formatted as YYYY-MM-DD HH:MM
-- humidity is a percentage [0-100]
-- pressure is in hPa (1hPa = 100 Pa)
-- rainfall is in mm e.g. 1.2mm

CREATE TABLE forecast(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    currentDate TEXT,
    forecastDate TEXT,
    descriptionID TEXT,
    maxTemperature REAL,
    minTemperature REAL,
    FOREIGN KEY(descriptionID) REFERENCES description(id)
);

CREATE TABLE description(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    shortDescription TEXT
);
