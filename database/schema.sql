DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS partner;
DROP TABLE IF EXISTS position;
DROP TABLE IF EXISTS shift;
DROP TABLE IF EXISTS employeeOnShift;

CREATE TABLE user
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT        NOT NULL,
    lastName  TEXT        NOT NULL,
    birthdate TIMESTAMP   NOT NULL,
    userRole  TEXT        NOT NULL,
    mobile    INTEGER     NOT NULL,
    street    TEXT        NOT NULL,
    city      TEXT        NOT NULL,
    country   TEXT        NOT NULL,
    username  TEXT UNIQUE NOT NULL,
    password  TEXT        NOT NULL,
    active    INTEGER     NOT NULL
);

CREATE TABLE partner
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    userId      INTEGER   NOT NULL,
    companyName TEXT      NOT NULL,
    sector      TEXT      NOT NULL,
    created     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES user (id)
);

CREATE TABLE position
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    partnerId   INTEGER   NOT NULL,
    name        TEXT      NOT NULL,
    description TEXT      NOT NULL,
    created     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (partnerId) REFERENCES partner (id)
);

CREATE TABLE shift
(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    positionId   INTEGER   NOT NULL,
    startTime    TIMESTAMP NOT NULL,
    endTime      TIMESTAMP NOT NULL,
    hourlyWage   INTEGER   NOT NULL,
    currencyCode TEXT      NOT NULL,
    created      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (positionId) REFERENCES position (id)
);

CREATE TABLE employeeOnShift
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    shiftId     INTEGER   NOT NULL,
    userId      INTEGER   NOT NULL,
    shiftPay    INTEGER   NOT NULL,
    workedHours INTEGER   NOT NULL,
    loggedIn    BOOLEAN   NOT NULL,
    created     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shiftId) REFERENCES shift (id),
    FOREIGN KEY (userId) REFERENCES user (id),
    UNIQUE (shiftId, userId)

);