DROP TABLE IF EXISTS plantInfo;
DROP TABLE IF EXISTS plantToState;
DROP TABLE IF EXISTS airQuality;
DROP TABLE IF EXISTS stateCodeToName;
DROP TABLE IF EXISTS plantIDToCounty;
DROP TABLE IF EXISTS countyToState;

CREATE TABLE plantInfo
(
    plantID INTEGER PRIMARY KEY NOT NULL,
    noxRate FLOAT DEFAULT 0.00,
    pmRate  FLOAT DEFAULT 0.00,
    totalCost FLOAT DEFAULT 0.00,
    totalFuelConsumed FLOAT DEFAULT 0.00,
    totalGenerated FLOAT DEFAULT 0.00    
);

CREATE TABLE plantToState
(
    plantID INTEGER PRIMARY KEY NOT NULL,
    stateCode CHAR(2),
    plantName VARCHAR(255)
);

CREATE TABLE airQuality
(   countyName VARCHAR(255),
    stateName VARCHAR(125),
    averageGooddays INTEGER DEFAULT 0,
    maxNO2days INTEGER DEFAULT 0,
    maxPMdays INTEGER DEFAULT 0,
    PRIMARY KEY (countyName, stateName)
);

CREATE TABLE stateCodeToName
(
    statecode CHAR(2) PRIMARY KEY,
    stateName VARCHAR(126),
    stateabbr VARCHAR(10)
);
 
CREATE TABLE plantIDToCounty
(
    plantID INTEGER PRIMARY KEY,
    countyName VARCHAR(255)
);
 
CREATE TABLE countyToState
(   
    countyName VARCHAR(255),
    stateName VARCHAR(255),
    PRIMARY KEY(countyName, stateName)
);