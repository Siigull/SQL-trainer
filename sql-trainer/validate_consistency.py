#!/usr/bin/env python3
"""
Consistency and semantic validation for SQL Trainer datasets.
Checks FK integrity, expected cardinalities, and that assignments match reality.
"""
import sqlite3
import sys

DATASETS = {
    "banka": """
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS transakce;
DROP TABLE IF EXISTS ucet;
DROP TABLE IF EXISTS pobocka;
DROP TABLE IF EXISTS klient;
CREATE TABLE klient (r_cislo TEXT PRIMARY KEY, jmeno TEXT NOT NULL, ulice TEXT, mesto TEXT);
CREATE TABLE pobocka (nazev TEXT PRIMARY KEY, jmeni INTEGER);
CREATE TABLE ucet (c_uctu INTEGER PRIMARY KEY, stav REAL, r_cislo TEXT NOT NULL REFERENCES klient ON DELETE CASCADE, pobocka TEXT REFERENCES pobocka);
CREATE TABLE transakce (c_uctu INTEGER, c_transakce INTEGER, datum TEXT, castka REAL, PRIMARY KEY (c_uctu, c_transakce), FOREIGN KEY (c_uctu) REFERENCES ucet ON DELETE CASCADE);
INSERT INTO klient VALUES('440726/0672','Jan Novak','Cejl 8','Brno');
INSERT INTO klient VALUES('530610/4532','Petr Vesely','Podzimni 28','Brno');
INSERT INTO klient VALUES('601001/2218','Ivan Zeman','Cejl 8','Brno');
INSERT INTO klient VALUES('510230/0048','Pavel Tomek','Tomkova 34','Brno');
INSERT INTO klient VALUES('580807/9638','Josef Moudry','Svatoplukova 15','Brno');
INSERT INTO klient VALUES('625622/6249','Jana Mala','Brnenska 56','Vyskov');
INSERT INTO klient VALUES('491120/0423','Jiri Novak',NULL,'Brno');
INSERT INTO pobocka VALUES('Janska',10000000);
INSERT INTO pobocka VALUES('Palackeho',5000000);
INSERT INTO ucet VALUES(4320286,52000,'440726/0672','Janska');
INSERT INTO ucet VALUES(2348531,10000,'530610/4532','Janska');
INSERT INTO ucet VALUES(1182648,10853,'530610/4532','Palackeho');
INSERT INTO ucet VALUES(2075752,26350,'440726/0672','Palackeho');
INSERT INTO ucet VALUES(1182649,40000,'530610/4532','Janska');
INSERT INTO ucet VALUES(4520111,40000,'580807/9638','Janska');
INSERT INTO ucet VALUES(4520112,40000,'580807/9638','Janska');
INSERT INTO ucet VALUES(9999999,90000,'625622/6249','Palackeho');
INSERT INTO transakce VALUES(4320286,1,'1998-10-10',3000);
INSERT INTO transakce VALUES(4320286,2,'1998-10-12',-5000);
INSERT INTO transakce VALUES(2075752,1,'1998-10-14',-2000);
INSERT INTO transakce VALUES(2075752,2,'1998-10-14',10000);
INSERT INTO transakce VALUES(2348531,1,'1998-10-15',5000);
INSERT INTO transakce VALUES(1182648,1,'1998-10-16',-1000);
INSERT INTO transakce VALUES(1182648,2,'1998-11-01',20000);
""",
    "obchod": """
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS koupil;
DROP TABLE IF EXISTS zbozi;
DROP TABLE IF EXISTS zakaznik;
CREATE TABLE zakaznik (cisloZ INTEGER PRIMARY KEY, jmeno TEXT, dat_nar TEXT, mesto TEXT);
CREATE TABLE zbozi (kodZb INTEGER PRIMARY KEY, nazev TEXT, kategorie TEXT, vyrobce TEXT);
CREATE TABLE koupil (cisloZ INTEGER REFERENCES zakaznik, kodZb INTEGER REFERENCES zbozi, datum TEXT, cena INTEGER, PRIMARY KEY (cisloZ, kodZb));
INSERT INTO zakaznik VALUES(1,'Samuel','1999-02-02','Brno');
INSERT INTO zakaznik VALUES(2,'Emanuel','1999-01-03','Brno');
INSERT INTO zakaznik VALUES(3,'Richard','2002-12-12','Brno');
INSERT INTO zakaznik VALUES(4,'Eva','2001-01-01','Praha');
INSERT INTO zakaznik VALUES(5,'Anna','1985-06-15','Praha');
INSERT INTO zakaznik VALUES(6,'Martin','1995-03-20','Ostrava');
INSERT INTO zakaznik VALUES(7,'Tereza','2000-01-01','Plzen');
INSERT INTO zbozi VALUES(1,'Samsung A20','mobily','Samsung');
INSERT INTO zbozi VALUES(2,'Benq 1000mq','monitory','Benq');
INSERT INTO zbozi VALUES(3,'iPhone X','mobily','Apple');
INSERT INTO zbozi VALUES(4,'MacBook Pro','notebooky','Apple');
INSERT INTO zbozi VALUES(5,'Dell UltraSharp','monitory','Dell');
INSERT INTO zbozi VALUES(6,'Sony WH-1000','sluchatka','Sony');
INSERT INTO zbozi VALUES(7,'iPad Air','tablety','Apple');
INSERT INTO zbozi VALUES(8,'Logitech MX','prislusenstvi','Logitech');
INSERT INTO zbozi VALUES(9,'Samsung S21','mobily','Samsung');
INSERT INTO zbozi VALUES(10,'LG 4K','monitory','LG');
INSERT INTO koupil VALUES(1,1,'2020-05-05',1200);
INSERT INTO koupil VALUES(2,1,'2020-05-05',800);
INSERT INTO koupil VALUES(3,1,'2020-05-05',1000);
INSERT INTO koupil VALUES(4,3,'2020-05-05',800);
INSERT INTO koupil VALUES(3,3,'2020-05-05',1000);
INSERT INTO koupil VALUES(2,2,'2019-05-05',1200);
INSERT INTO koupil VALUES(1,2,'2019-06-05',1000);
INSERT INTO koupil VALUES(4,2,'2019-06-07',800);
INSERT INTO koupil VALUES(5,4,'2020-01-10',45000);
INSERT INTO koupil VALUES(6,5,'2020-02-15',8000);
INSERT INTO koupil VALUES(1,9,'2020-03-10',25000);
INSERT INTO koupil VALUES(2,9,'2020-03-11',24500);
INSERT INTO koupil VALUES(3,6,'2020-04-01',5000);
INSERT INTO koupil VALUES(4,7,'2020-04-02',12000);
INSERT INTO koupil VALUES(5,8,'2020-04-03',2000);
INSERT INTO koupil VALUES(6,10,'2019-07-20',15000);
INSERT INTO koupil VALUES(1,4,'2019-08-10',42000);
INSERT INTO koupil VALUES(3,5,'2019-09-05',7500);
""",
    "univerzita": """
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS zapsal;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS predmet;
CREATE TABLE predmet (zkratkaP TEXT PRIMARY KEY, nazev TEXT NOT NULL, kredity INTEGER NOT NULL);
CREATE TABLE student (cisloS INTEGER PRIMARY KEY, jmeno TEXT NOT NULL, mesto TEXT NOT NULL);
CREATE TABLE zapsal (cisloS INTEGER REFERENCES student, zkratkaP TEXT REFERENCES predmet, ak_rok INTEGER, body INTEGER NOT NULL, PRIMARY KEY (cisloS, zkratkaP, ak_rok));
INSERT INTO predmet VALUES('IMA','Matematika',50);
INSERT INTO predmet VALUES('ISS','Signaly',30);
INSERT INTO predmet VALUES('IOS','Operacni systemy',4);
INSERT INTO predmet VALUES('IDB','Databaze',60);
INSERT INTO predmet VALUES('IPK','Pocitacove komunikace',40);
INSERT INTO predmet VALUES('IEL','Elektronika',30);
INSERT INTO predmet VALUES('FYZ','Fyzika',40);
INSERT INTO student VALUES(1,'Pavel','Brno');
INSERT INTO student VALUES(2,'Pavel','Bratislava');
INSERT INTO student VALUES(3,'Peter','Bratislava');
INSERT INTO student VALUES(4,'Adam Novy','Praha');
INSERT INTO student VALUES(5,'Marie','Brno');
INSERT INTO student VALUES(6,'Jana','Praha');
INSERT INTO student VALUES(7,'Karel','Ostrava');
INSERT INTO student VALUES(8,'Eva','Brno');
INSERT INTO zapsal VALUES(1,'IMA',2021,95);
INSERT INTO zapsal VALUES(1,'ISS',2021,95);
INSERT INTO zapsal VALUES(1,'IOS',2021,85);
INSERT INTO zapsal VALUES(2,'IOS',2021,55);
INSERT INTO zapsal VALUES(2,'IMA',2021,55);
INSERT INTO zapsal VALUES(2,'IPK',2021,70);
INSERT INTO zapsal VALUES(3,'IMA',2021,50);
INSERT INTO zapsal VALUES(3,'ISS',2021,34);
INSERT INTO zapsal VALUES(3,'IDB',2021,88);
INSERT INTO zapsal VALUES(4,'IEL',2021,92);
INSERT INTO zapsal VALUES(4,'IDB',2021,75);
INSERT INTO zapsal VALUES(5,'IMA',2021,80);
INSERT INTO zapsal VALUES(5,'ISS',2021,65);
INSERT INTO zapsal VALUES(5,'IOS',2021,90);
INSERT INTO zapsal VALUES(5,'IEL',2021,78);
INSERT INTO zapsal VALUES(6,'IDB',2021,60);
INSERT INTO zapsal VALUES(6,'IPK',2021,45);
INSERT INTO zapsal VALUES(7,'IOS',2021,30);
""",
    "firma": """
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS zamestnanec;
DROP TABLE IF EXISTS oddeleni;
CREATE TABLE oddeleni (nazov TEXT PRIMARY KEY, popis TEXT);
CREATE TABLE zamestnanec (id INTEGER PRIMARY KEY AUTOINCREMENT, mzda INTEGER NOT NULL CHECK(mzda >= 0), meno TEXT NOT NULL, oddelenie TEXT NOT NULL REFERENCES oddeleni(nazov) ON DELETE CASCADE, vedeneOddelenie TEXT NULL REFERENCES oddeleni(nazov));
INSERT INTO oddeleni VALUES('Ekonomicke','Vyplaty a dane');
INSERT INTO oddeleni VALUES('Personalne','Najimanie ludi');
INSERT INTO oddeleni VALUES('Marketingove','Komunikacia so zakaznikmi a reklamou');
INSERT INTO oddeleni VALUES('Analyticke','Zber a spracovanie dat');
INSERT INTO oddeleni VALUES('IT','Podpora systemov a vyvoj');
INSERT INTO zamestnanec VALUES(NULL,3000,'Monika','Ekonomicke','Ekonomicke');
INSERT INTO zamestnanec VALUES(NULL,1800,'Emma','Ekonomicke',NULL);
INSERT INTO zamestnanec VALUES(NULL,3200,'Lucia','Personalne','Personalne');
INSERT INTO zamestnanec VALUES(NULL,2800,'Michal','Personalne',NULL);
INSERT INTO zamestnanec VALUES(NULL,3000,'Samuel','Marketingove','Marketingove');
INSERT INTO zamestnanec VALUES(NULL,1200,'Ella','Marketingove',NULL);
INSERT INTO zamestnanec VALUES(NULL,2500,'Jan','Analyticke',NULL);
INSERT INTO zamestnanec VALUES(NULL,3500,'Igor','Analyticke','Analyticke');
INSERT INTO zamestnanec VALUES(NULL,4500,'Dana','IT','IT');
INSERT INTO zamestnanec VALUES(NULL,2200,'Tomas','IT',NULL);
INSERT INTO zamestnanec VALUES(NULL,5000,'Petra','Ekonomicke',NULL);
INSERT INTO zamestnanec VALUES(NULL,4000,'Lukas','IT',NULL);
""",
    "servis": """
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS oprava;
DROP TABLE IF EXISTS auto;
DROP TABLE IF EXISTS mechanik;
CREATE TABLE mechanik (cisloM INTEGER PRIMARY KEY, meno TEXT NOT NULL);
CREATE TABLE auto (spz INTEGER PRIMARY KEY, znacka TEXT NOT NULL, r_vyroby INTEGER NOT NULL);
CREATE TABLE oprava (cisloO INTEGER PRIMARY KEY AUTOINCREMENT, cisloM INTEGER REFERENCES mechanik, spz INTEGER REFERENCES auto NOT NULL, datum TEXT NOT NULL, cena INTEGER NOT NULL, typ TEXT NOT NULL);
INSERT INTO mechanik VALUES(69,'Adam');
INSERT INTO mechanik VALUES(42,'Betka');
INSERT INTO mechanik VALUES(33,'Cyril');
INSERT INTO mechanik VALUES(77,'Dana');
INSERT INTO mechanik VALUES(55,'Erik');
INSERT INTO auto VALUES(123,'Ford',2005);
INSERT INTO auto VALUES(999,'Volvo',2000);
INSERT INTO auto VALUES(555,'Skoda',2015);
INSERT INTO auto VALUES(777,'BMW',2018);
INSERT INTO auto VALUES(888,'Audi',2020);
INSERT INTO auto VALUES(444,'Ford',2010);
INSERT INTO auto VALUES(333,'Volvo',2012);
INSERT INTO auto VALUES(222,'Skoda',2008);
INSERT INTO oprava VALUES(NULL,69,123,'2022-03-28',100000,'vymena');
INSERT INTO oprava VALUES(NULL,42,999,'2022-03-28',25000,'brzdy');
INSERT INTO oprava VALUES(NULL,42,999,'2022-03-29',50001,'vymena');
INSERT INTO oprava VALUES(NULL,42,999,'2022-03-30',58000,'vymena');
INSERT INTO oprava VALUES(NULL,33,555,'2022-04-01',15000,'oprava');
INSERT INTO oprava VALUES(NULL,33,777,'2022-04-02',22000,'brzdy');
INSERT INTO oprava VALUES(NULL,77,888,'2022-04-03',35000,'vymena');
INSERT INTO oprava VALUES(NULL,55,444,'2022-04-04',8000,'oprava');
INSERT INTO oprava VALUES(NULL,69,333,'2022-04-05',45000,'vymena');
INSERT INTO oprava VALUES(NULL,42,222,'2022-04-06',12000,'brzdy');
INSERT INTO oprava VALUES(NULL,33,123,'2022-04-07',9500,'vymena');
INSERT INTO oprava VALUES(NULL,77,555,'2022-04-08',18000,'vymena');
INSERT INTO oprava VALUES(NULL,55,999,'2022-04-09',32000,'brzdy');
INSERT INTO oprava VALUES(NULL,69,777,'2022-04-10',28000,'oprava');
INSERT INTO oprava VALUES(NULL,42,888,'2022-04-11',60000,'vymena');
""",
    "dodavatele": """
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS dodava;
DROP TABLE IF EXISTS zbozi;
DROP TABLE IF EXISTS dodavatel;
CREATE TABLE dodavatel (ico INTEGER PRIMARY KEY, nazev TEXT, mesto TEXT, vzdalenost INTEGER);
CREATE TABLE zbozi (kod INTEGER PRIMARY KEY, nazev TEXT, vyrobce TEXT);
CREATE TABLE dodava (ico INTEGER REFERENCES dodavatel, kod INTEGER REFERENCES zbozi, cena INTEGER, PRIMARY KEY (ico, kod));
INSERT INTO dodavatel VALUES(0,'CojavimCorp','Olomouc',67);
INSERT INTO dodavatel VALUES(1,'Stark','Kromeriz',125);
INSERT INTO dodavatel VALUES(2,'Dodavatel od vedle','Kromeriz',12);
INSERT INTO dodavatel VALUES(3,'AiAi','Hradec Kralove',91);
INSERT INTO dodavatel VALUES(4,'Datemer','Hradec Kralove',350);
INSERT INTO dodavatel VALUES(5,'Elektromadar','Kromeriz',261);
INSERT INTO dodavatel VALUES(6,'Hae','Praha',311);
INSERT INTO dodavatel VALUES(7,'Petr','Olomouc',237);
INSERT INTO dodavatel VALUES(8,'Elektro plus','Brno',68);
INSERT INTO dodavatel VALUES(9,'Zeus','Hradec Kralove',85);
INSERT INTO zbozi VALUES(0,'HD 30 GB','Kingston');
INSERT INTO zbozi VALUES(1,'Flashka 3000','Kingston');
INSERT INTO zbozi VALUES(2,'HD monitor','Kingston');
INSERT INTO zbozi VALUES(3,'Televize ako stena','Sony');
INSERT INTO zbozi VALUES(4,'Nejakej mobil','Panasonic');
INSERT INTO zbozi VALUES(5,'Ultrahyperturbo vysavac','Panasonic');
INSERT INTO zbozi VALUES(6,'proste jmeno produktu','Sony');
INSERT INTO zbozi VALUES(7,'Modra lampicka','Samsung');
INSERT INTO zbozi VALUES(8,'Draha krabice','Sony');
INSERT INTO zbozi VALUES(9,'Notebook','Samsung');
INSERT INTO dodava VALUES(7,6,156);
INSERT INTO dodava VALUES(8,9,7310);
INSERT INTO dodava VALUES(4,8,776);
INSERT INTO dodava VALUES(5,1,174);
INSERT INTO dodava VALUES(1,8,5594);
INSERT INTO dodava VALUES(0,6,7148);
INSERT INTO dodava VALUES(8,8,9709);
INSERT INTO dodava VALUES(7,7,6921);
INSERT INTO dodava VALUES(5,9,4284);
INSERT INTO dodava VALUES(3,6,8579);
INSERT INTO dodava VALUES(2,1,3053);
INSERT INTO dodava VALUES(2,0,9156);
INSERT INTO dodava VALUES(6,3,8844);
INSERT INTO dodava VALUES(3,9,2456);
INSERT INTO dodava VALUES(7,2,2750);
INSERT INTO dodava VALUES(4,4,8708);
INSERT INTO dodava VALUES(2,7,5308);
INSERT INTO dodava VALUES(5,7,9704);
INSERT INTO dodava VALUES(1,4,8709);
INSERT INTO dodava VALUES(2,4,6805);
INSERT INTO dodava VALUES(1,7,7213);
INSERT INTO dodava VALUES(9,8,9138);
INSERT INTO dodava VALUES(6,1,4431);
INSERT INTO dodava VALUES(4,7,3345);
INSERT INTO dodava VALUES(1,9,5812);
INSERT INTO dodava VALUES(6,6,9745);
INSERT INTO dodava VALUES(4,9,2960);
INSERT INTO dodava VALUES(2,3,8989);
INSERT INTO dodava VALUES(7,1,9124);
INSERT INTO dodava VALUES(8,2,9323);
INSERT INTO dodava VALUES(5,0,926);
INSERT INTO dodava VALUES(1,5,7343);
INSERT INTO dodava VALUES(7,3,6483);
INSERT INTO dodava VALUES(3,4,8520);
INSERT INTO dodava VALUES(3,8,3805);
""",
    "rezervace": """
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS Rezervace_historie;
DROP TABLE IF EXISTS Rezervace;
DROP TABLE IF EXISTS Predmet;
DROP TABLE IF EXISTS Ucebna;
CREATE TABLE Predmet (zkratkaP TEXT PRIMARY KEY, nazev TEXT NOT NULL);
CREATE TABLE Ucebna (cisloU INTEGER PRIMARY KEY, typ TEXT, pocet_mist INTEGER);
CREATE TABLE Rezervace (ID INTEGER PRIMARY KEY, zkratkaP TEXT REFERENCES Predmet, cisloU INTEGER REFERENCES Ucebna, den TEXT, zacatek TEXT, konec TEXT);
CREATE TABLE Rezervace_historie (ID INTEGER, zkratkaP TEXT, cisloU INTEGER, den TEXT, zacatek TEXT, konec TEXT);
INSERT INTO Predmet VALUES ('IMA','Matematika');
INSERT INTO Predmet VALUES ('ISS','Signaly');
INSERT INTO Predmet VALUES ('IOS','Operacni systemy');
INSERT INTO Ucebna VALUES (1,'PC ucebna',30);
INSERT INTO Ucebna VALUES (2,'Prednaskova',120);
INSERT INTO Ucebna VALUES (3,'PC ucebna',25);
INSERT INTO Rezervace VALUES (1,'IMA',1,'pondeli','08:00','09:50');
INSERT INTO Rezervace VALUES (2,'ISS',2,'pondeli','12:00','13:50');
INSERT INTO Rezervace VALUES (3,'IOS',3,'utery','10:00','11:50');
INSERT INTO Rezervace VALUES (4,'IMA',1,'streda','12:00','13:50');
INSERT INTO Rezervace VALUES (5,'ISS',3,'ctvrtek','14:00','15:50');
"""
}

CHECKS = [
    ("banka", "SELECT COUNT(*) FROM klient", [(7,)], "7 clients"),
    ("banka", "SELECT COUNT(*) FROM ucet WHERE r_cislo NOT IN (SELECT r_cislo FROM klient)", [(0,)], "No orphan accounts (fk)"),
    ("banka", "SELECT COUNT(*) FROM ucet WHERE pobocka NOT IN (SELECT nazev FROM pobocka)", [(0,)], "No orphan accounts (branch)"),
    ("banka", "SELECT COUNT(*) FROM transakce WHERE c_uctu NOT IN (SELECT c_uctu FROM ucet)", [(0,)], "No orphan transactions"),
    ("obchod", "SELECT COUNT(*) FROM zakaznik", [(7,)], "7 customers"),
    ("obchod", "SELECT COUNT(*) FROM koupil WHERE cisloZ NOT IN (SELECT cisloZ FROM zakaznik)", [(0,)], "No orphan purchases (customer)"),
    ("obchod", "SELECT COUNT(*) FROM koupil WHERE kodZb NOT IN (SELECT kodZb FROM zbozi)", [(0,)], "No orphan purchases (product)"),
    ("univerzita", "SELECT COUNT(*) FROM student", [(8,)], "8 students"),
    ("univerzita", "SELECT COUNT(*) FROM predmet", [(7,)], "7 subjects"),
    ("univerzita", "SELECT COUNT(*) FROM zapsal WHERE cisloS NOT IN (SELECT cisloS FROM student)", [(0,)], "No orphan enrollments (student)"),
    ("univerzita", "SELECT COUNT(*) FROM zapsal WHERE zkratkaP NOT IN (SELECT zkratkaP FROM predmet)", [(0,)], "No orphan enrollments (subject)"),
    ("firma", "SELECT COUNT(*) FROM oddeleni", [(5,)], "5 departments"),
    ("firma", "SELECT COUNT(*) FROM zamestnanec WHERE oddelenie NOT IN (SELECT nazov FROM oddeleni)", [(0,)], "No orphan employees"),
    ("firma", "SELECT COUNT(*) FROM zamestnanec WHERE vedeneOddelenie IS NOT NULL AND vedeneOddelenie NOT IN (SELECT nazov FROM oddeleni)", [(0,)], "No orphan managers"),
    ("servis", "SELECT COUNT(*) FROM mechanik", [(5,)], "5 mechanics"),
    ("servis", "SELECT COUNT(*) FROM auto", [(8,)], "8 cars"),
    ("servis", "SELECT COUNT(*) FROM oprava WHERE cisloM NOT IN (SELECT cisloM FROM mechanik)", [(0,)], "No orphan repairs (mechanic)"),
    ("servis", "SELECT COUNT(*) FROM oprava WHERE spz NOT IN (SELECT spz FROM auto)", [(0,)], "No orphan repairs (car)"),
    ("dodavatele", "SELECT COUNT(*) FROM dodavatel", [(10,)], "10 suppliers"),
    ("dodavatele", "SELECT COUNT(*) FROM zbozi", [(10,)], "10 products"),
    ("dodavatele", "SELECT COUNT(*) FROM dodava WHERE ico NOT IN (SELECT ico FROM dodavatel)", [(0,)], "No orphan supplies (supplier)"),
    ("dodavatele", "SELECT COUNT(*) FROM dodava WHERE kod NOT IN (SELECT kod FROM zbozi)", [(0,)], "No orphan supplies (product)"),
]

SEMANTIC = [
    ("banka", "SELECT COUNT(*) FROM klient k LEFT JOIN ucet u ON k.r_cislo = u.r_cislo WHERE u.c_uctu IS NULL", [(3,)], "3 clients without accounts"),
    ("banka", "SELECT COUNT(*) FROM transakce WHERE datum LIKE '1998-10-%'", [(6,)], "6 transactions in October"),
    ("obchod", "SELECT COUNT(*) FROM zakaznik z LEFT JOIN koupil k ON z.cisloZ = k.cisloZ WHERE k.cisloZ IS NULL", [(1,)], "1 customer without purchase"),
    ("obchod", "SELECT COUNT(DISTINCT kategorie) FROM zbozi", [(6,)], "6 product categories"),
    ("univerzita", "SELECT COUNT(*) FROM predmet p LEFT JOIN zapsal z ON p.zkratkaP = z.zkratkaP AND z.ak_rok = 2021 WHERE z.cisloS IS NULL", [(1,)], "1 subject without enrollment"),
    ("univerzita", "SELECT COUNT(*) FROM (SELECT cisloS FROM zapsal WHERE ak_rok = 2021 GROUP BY cisloS HAVING SUM(body) > 70)", [(6,)], "6 students with >70 credits"),
    ("firma", "SELECT COUNT(*) FROM zamestnanec WHERE vedeneOddelenie IS NOT NULL", [(5,)], "5 department managers"),
    ("servis", "SELECT COUNT(*) FROM (SELECT spz FROM oprava GROUP BY spz HAVING SUM(cena) > 50000)", [(3,)], "3 cars with repair costs >50000"),
    ("servis", "SELECT COUNT(DISTINCT typ) FROM oprava", [(3,)], "3 repair types"),
    ("dodavatele", "SELECT COUNT(*) FROM (SELECT kod FROM dodava GROUP BY kod HAVING COUNT(*) = 1)", [(1,)], "1 product from exactly 1 supplier"),
    ("banka", "SELECT COUNT(*) FROM (SELECT k.r_cislo FROM klient k JOIN ucet u ON k.r_cislo = u.r_cislo WHERE k.mesto <> 'Brno' GROUP BY k.r_cislo HAVING SUM(u.stav) > (SELECT MAX(tot) FROM (SELECT SUM(stav) AS tot FROM klient k2 JOIN ucet u2 ON k2.r_cislo = u2.r_cislo WHERE k2.mesto = 'Brno' GROUP BY k2.r_cislo) t))", [(1,)], "1 non-Brno client with balance > all Brno clients"),
    ("servis", "SELECT COUNT(*) FROM (SELECT m.cisloM FROM mechanik m JOIN oprava o ON m.cisloM = o.cisloM GROUP BY m.cisloM, m.meno HAVING COUNT(DISTINCT o.typ) = 3)", [(1,)], "1 mechanic with all 3 repair types"),
    ("rezervace", "SELECT COUNT(*) FROM Rezervace WHERE den = 'pondeli' AND zacatek = '12:00'", [(1,)], "1 reservation on monday at 12:00"),
    ("rezervace", "SELECT COUNT(*) FROM Rezervace_historie", [(0,)], "0 rows in history table initially"),
]

def run():
    errors = []
    for ds, sql, expected, note in CHECKS + SEMANTIC:
        conn = sqlite3.connect(":memory:")
        conn.executescript(DATASETS[ds])
        cur = conn.cursor()
        try:
            cur.execute(sql)
            actual = cur.fetchall()
            if actual != expected:
                errors.append((ds, note, f"Expected {expected}, got {actual}"))
        except Exception as e:
            errors.append((ds, note, str(e)))
        finally:
            conn.close()
    
    print(f"Ran {len(CHECKS)+len(SEMANTIC)} consistency/semantic checks")
    if errors:
        print(f"FAILED: {len(errors)}")
        for ds, note, err in errors:
            print(f"  [{ds}] {note}: {err}")
        sys.exit(1)
    else:
        print("All consistency checks passed!")

if __name__ == "__main__":
    run()
