DROP TABLE zapsal;
DROP TABLE student;
DROP TABLE predmet;
DROP VIEW NOVY_ZIACI;


CREATE TABLE predmet
(
    zkratkaP    VARCHAR(255) PRIMARY KEY NOT NULL,
    nazev       VARCHAR(255) NOT NULL,
    kredity     INT NOT NULL
);

CREATE TABLE student
(
    cisloS      INT PRIMARY KEY NOT NULL,
    jmeno       VARCHAR(255) NOT NULL,
    mesto       VARCHAR(255) NOT NULL
);

CREATE TABLE zapsal
(
    cisloS  REFERENCES student,
    zkratkaP REFERENCES predmet,
    ak_rok INT,
    body INT NOT NULL,
    CONSTRAINT zapsal_pk PRIMARY KEY(cisloS, zkratkaP, ak_rok)
);

INSERT INTO student VALUES (1, 'Pavel', 'Brno');
INSERT INTO student VALUES (2, 'Pavel', 'Bratislava');
INSERT INTO student VALUES (3, 'Peter', 'Bratislava');
INSERT INTO student VALUES (4, 'Adam Novy', 'Praha');


INSERT INTO predmet VALUES ('IMA', 'Matematika', 50);
INSERT INTO predmet VALUES ('ISS', 'Signaly', 30);
INSERT INTO predmet VALUES ('IOS', 'OS', 4);

INSERT INTO zapsal VALUES (1, 'IMA', 2021, 95);
INSERT INTO zapsal VALUES (1, 'ISS', 2021, 95);
INSERT INTO zapsal VALUES (2, 'IOS', 2021, 55);
INSERT INTO zapsal VALUES (2, 'IMA', 2021, 55);
INSERT INTO zapsal VALUES (3, 'IMA', 2021, 50);
INSERT INTO zapsal VALUES (3, 'ISS', 2021, 34);


COMMIT;
