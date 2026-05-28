#!/usr/bin/env python3
"""
SQL Trainer Validator
Runs every hint SQL against its dataset using sqlite3 and reports issues.
"""
import sqlite3
import io
import sys

# ============== DATASETS ==============
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
"""
}

# ============== QUESTIONS ==============
# This list mirrors the questions in index.html
QUESTIONS = [
    # banka
    {"id":"b1","dataset":"banka","title":"Klienti z Brna","hint":"SELECT r_cislo, jmeno, ulice, mesto FROM klient WHERE mesto = 'Brno' ORDER BY jmeno ASC"},
    {"id":"b2","dataset":"banka","title":"Města klientů","hint":"SELECT DISTINCT mesto FROM klient"},
    {"id":"b3","dataset":"banka","title":"Účty s vysokým zůstatkem","hint":"SELECT * FROM ucet WHERE stav > 20000"},
    {"id":"b4","dataset":"banka","title":"Jmění poboček v USD","hint":"SELECT nazev, jmeni / 25.0 AS jmeni_usd FROM pobocka"},
    {"id":"b5","dataset":"banka","title":"Klienti s účtem","hint":"SELECT DISTINCT k.r_cislo, k.jmeno FROM klient k JOIN ucet u ON k.r_cislo = u.r_cislo"},
    {"id":"b6","dataset":"banka","title":"Transakce 14. 10. 1998","hint":"SELECT k.r_cislo, k.jmeno, t.c_uctu, t.castka FROM klient k JOIN ucet u ON k.r_cislo = u.r_cislo JOIN transakce t ON u.c_uctu = t.c_uctu WHERE t.datum = '1998-10-14'"},
    {"id":"b7","dataset":"banka","title":"Klienti na stejné adrese","hint":"SELECT k1.jmeno AS jmeno1, k1.r_cislo AS rc1, k2.jmeno AS jmeno2, k2.r_cislo AS rc2, k1.ulice, k1.mesto FROM klient k1 JOIN klient k2 ON k1.mesto = k2.mesto AND k1.ulice = k2.ulice WHERE k1.r_cislo > k2.r_cislo"},
    {"id":"b8","dataset":"banka","title":"Počet klientů ve městech","hint":"SELECT mesto, COUNT(*) AS pocet FROM klient GROUP BY mesto"},
    {"id":"b9","dataset":"banka","title":"Statistiky zůstatků","hint":"SELECT MIN(stav) AS min_stav, AVG(stav) AS prumer, MAX(stav) AS max_stav FROM ucet"},
    {"id":"b10","dataset":"banka","title":"Celkový zůstatek na pobočce","hint":"SELECT pobocka, SUM(stav) AS celkem FROM ucet GROUP BY pobocka"},
    {"id":"b11","dataset":"banka","title":"Účty a zůstatky klientů","hint":"SELECT k.jmeno, k.r_cislo, COUNT(*) AS pocet, SUM(u.stav) AS celkem FROM klient k JOIN ucet u ON k.r_cislo = u.r_cislo GROUP BY k.jmeno, k.r_cislo"},
    {"id":"b12","dataset":"banka","title":"Klienti bez účtu","hint":"SELECT k.jmeno, k.r_cislo FROM klient k LEFT JOIN ucet u ON k.r_cislo = u.r_cislo WHERE u.c_uctu IS NULL"},
    {"id":"b13","dataset":"banka","title":"Jen pobočka Jánská","hint":"SELECT DISTINCT k.r_cislo, k.jmeno FROM klient k JOIN ucet u ON k.r_cislo = u.r_cislo WHERE u.pobocka = 'Janska' AND NOT EXISTS (SELECT 1 FROM ucet u2 WHERE u2.r_cislo = k.r_cislo AND (u2.pobocka <> 'Janska' OR u2.pobocka IS NULL))"},
    {"id":"b14","dataset":"banka","title":"Více než všichni z Brna","hint":"SELECT k.jmeno, k.r_cislo, k.mesto, SUM(u.stav) AS celkem FROM klient k JOIN ucet u ON k.r_cislo = u.r_cislo WHERE k.mesto <> 'Brno' GROUP BY k.jmeno, k.r_cislo, k.mesto HAVING SUM(u.stav) > (SELECT MAX(brno_totals.total) FROM (SELECT SUM(u2.stav) AS total FROM klient k2 JOIN ucet u2 ON k2.r_cislo = u2.r_cislo WHERE k2.mesto = 'Brno' GROUP BY k2.r_cislo) brno_totals)"},
    {"id":"b15","dataset":"banka","title":"Transakce v říjnu 1998","hint":"SELECT * FROM transakce WHERE datum BETWEEN '1998-10-01' AND '1998-10-31'"},
    {"id":"b16","dataset":"banka","title":"UNION: Pobočky a města","hint":"SELECT nazev AS place FROM pobocka UNION SELECT mesto AS place FROM klient"},
    {"id":"b17","dataset":"banka","title":"Maximum z průměrů","hint":"SELECT MAX(avg_stav) AS max_prumer FROM (SELECT AVG(stav) AS avg_stav FROM ucet GROUP BY r_cislo)"},
    {"id":"b18","dataset":"banka","title":"Klient s nejvyšším průměrem","hint":"SELECT k.jmeno, k.r_cislo, AVG(u.stav) AS prumer FROM klient k JOIN ucet u ON k.r_cislo = u.r_cislo GROUP BY k.jmeno, k.r_cislo HAVING AVG(u.stav) >= (SELECT MAX(avg_stav) FROM (SELECT AVG(stav) AS avg_stav FROM ucet GROUP BY r_cislo))"},
    # obchod
    {"id":"o1","dataset":"obchod","title":"Nákupy monitorů 2019","hint":"SELECT CAST(SUBSTR(datum,6,2) AS INTEGER) AS mesic, COUNT(*) AS pocet_nakupu FROM koupil k JOIN zbozi z ON k.kodZb = z.kodZb WHERE z.kategorie = 'monitory' AND datum BETWEEN '2019-01-01' AND '2019-12-31' GROUP BY CAST(SUBSTR(datum,6,2) AS INTEGER)"},
    {"id":"o2","dataset":"obchod","title":"Zboží pro mladé","hint":"SELECT z.kodZb, z.nazev, z.kategorie FROM zbozi z WHERE NOT EXISTS (SELECT 1 FROM koupil k JOIN zakaznik za ON k.cisloZ = za.cisloZ WHERE k.kodZb = z.kodZb AND za.dat_nar <= '2000-12-31')"},
    {"id":"o3","dataset":"obchod","title":"Samsung A20 nejdražší","hint":"SELECT za.cisloZ, za.jmeno, za.mesto FROM zakaznik za JOIN koupil k ON za.cisloZ = k.cisloZ JOIN zbozi z ON k.kodZb = z.kodZb WHERE z.nazev = 'Samsung A20' AND k.cena = (SELECT MAX(k2.cena) FROM koupil k2 JOIN zbozi z2 ON k2.kodZb = z2.kodZb WHERE z2.nazev = 'Samsung A20')"},
    {"id":"o4","dataset":"obchod","title":"Příjmy podle kategorie","hint":"SELECT z.kategorie, SUM(k.cena) AS celkem FROM koupil k JOIN zbozi z ON k.kodZb = z.kodZb GROUP BY z.kategorie ORDER BY celkem DESC LIMIT 1"},
    {"id":"o5","dataset":"obchod","title":"Zákazníci s 3+ produkty","hint":"SELECT za.cisloZ, za.jmeno, COUNT(DISTINCT k.kodZb) AS pocet_produktu FROM zakaznik za JOIN koupil k ON za.cisloZ = k.cisloZ GROUP BY za.cisloZ, za.jmeno HAVING COUNT(DISTINCT k.kodZb) >= 3"},
    {"id":"o6","dataset":"obchod","title":"Zákazníci bez nákupu","hint":"SELECT z.cisloZ, z.jmeno FROM zakaznik z LEFT JOIN koupil k ON z.cisloZ = k.cisloZ WHERE k.cisloZ IS NULL"},
    {"id":"o7","dataset":"obchod","title":"Výrobci v kategoriích","hint":"SELECT vyrobce, COUNT(DISTINCT kategorie) AS pocet_kategorii FROM zbozi GROUP BY vyrobce HAVING COUNT(DISTINCT kategorie) >= 2"},
    {"id":"o8","dataset":"obchod","title":"Celkové výdaje zákazníků","hint":"SELECT z.cisloZ, z.jmeno, COALESCE(SUM(k.cena),0) AS celkem_utraceno FROM zakaznik z LEFT JOIN koupil k ON z.cisloZ = k.cisloZ GROUP BY z.cisloZ, z.jmeno"},
    # univerzita
    {"id":"u1","dataset":"univerzita","title":"Více než 70 kreditů","hint":"SELECT s.cisloS, s.jmeno, SUM(p.kredity) AS kreditu_celkem FROM student s JOIN zapsal z ON s.cisloS = z.cisloS JOIN predmet p ON z.zkratkaP = p.zkratkaP WHERE z.ak_rok = 2021 GROUP BY s.cisloS, s.jmeno HAVING SUM(p.kredity) > 70"},
    {"id":"u2","dataset":"univerzita","title":"Prošel matematiku","hint":"SELECT s.jmeno, s.mesto FROM student s JOIN zapsal z ON s.cisloS = z.cisloS JOIN predmet p ON z.zkratkaP = p.zkratkaP WHERE p.nazev = 'Matematika' AND z.ak_rok = 2021 AND z.body >= 50 ORDER BY s.jmeno ASC, s.mesto ASC"},
    {"id":"u3","dataset":"univerzita","title":"Průměr bodů z předmětů","hint":"SELECT p.nazev, AVG(z.body) AS prumer FROM predmet p JOIN zapsal z ON p.zkratkaP = z.zkratkaP GROUP BY p.nazev"},
    {"id":"u4","dataset":"univerzita","title":"Nejlepší student","hint":"SELECT s.cisloS, s.jmeno, SUM(z.body) AS celkem_bodu FROM student s JOIN zapsal z ON s.cisloS = z.cisloS WHERE z.ak_rok = 2021 GROUP BY s.cisloS, s.jmeno HAVING SUM(z.body) >= (SELECT MAX(tot.total) FROM (SELECT SUM(z2.body) AS total FROM zapsal z2 WHERE z2.ak_rok = 2021 GROUP BY z2.cisloS) tot)"},
    {"id":"u5","dataset":"univerzita","title":"Nepoužité předměty","hint":"SELECT p.zkratkaP, p.nazev FROM predmet p LEFT JOIN zapsal z ON p.zkratkaP = z.zkratkaP AND z.ak_rok = 2021 WHERE z.cisloS IS NULL"},
    {"id":"u6","dataset":"univerzita","title":"Město s nejvíce studenty","hint":"SELECT s.mesto, COUNT(DISTINCT s.cisloS) AS pocet FROM student s JOIN zapsal z ON s.cisloS = z.cisloS WHERE z.ak_rok = 2021 GROUP BY s.mesto ORDER BY pocet DESC, s.mesto ASC LIMIT 1"},
    {"id":"u7","dataset":"univerzita","title":"Studenti ve všech předmětech","hint":"SELECT s.cisloS, s.jmeno FROM student s WHERE NOT EXISTS (SELECT 1 FROM predmet p WHERE NOT EXISTS (SELECT 1 FROM zapsal z WHERE z.cisloS = s.cisloS AND z.zkratkaP = p.zkratkaP))"},
    {"id":"u8","dataset":"univerzita","title":"Zápis do Databáze s průměrem >60","hint":"SELECT s.mesto, AVG(z.body) AS prumer FROM student s JOIN zapsal z ON s.cisloS = z.cisloS JOIN predmet p ON z.zkratkaP = p.zkratkaP WHERE p.nazev = 'Databaze' GROUP BY s.mesto HAVING AVG(z.body) > 60"},
    # firma
    {"id":"f1","dataset":"firma","title":"Průměrná mzda v oddělení","hint":"SELECT oddelenie, AVG(mzda) AS prumerna_mzda FROM zamestnanec GROUP BY oddelenie"},
    {"id":"f2","dataset":"firma","title":"Oddělení s nejvyšší průměrnou mzdou","hint":"SELECT oddelenie, AVG(mzda) AS prumerna_mzda FROM zamestnanec GROUP BY oddelenie HAVING AVG(mzda) >= (SELECT MAX(avg_mzda) FROM (SELECT AVG(mzda) AS avg_mzda FROM zamestnanec GROUP BY oddelenie) dept_avgs)"},
    {"id":"f3","dataset":"firma","title":"Manažeři oddělení","hint":"SELECT id, meno, vedeneOddelenie FROM zamestnanec WHERE vedeneOddelenie IS NOT NULL"},
    {"id":"f4","dataset":"firma","title":"Počet zaměstnanců včetně prázdných oddělení","hint":"SELECT o.nazov, o.popis, COUNT(z.id) AS pocet_zamestnancu FROM oddeleni o LEFT JOIN zamestnanec z ON o.nazov = z.oddelenie GROUP BY o.nazov, o.popis"},
    {"id":"f5","dataset":"firma","title":"Nad průměrem oddělení","hint":"SELECT z1.id, z1.meno, z1.mzda, z1.oddelenie FROM zamestnanec z1 WHERE z1.mzda > (SELECT AVG(z2.mzda) FROM zamestnanec z2 WHERE z2.oddelenie = z1.oddelenie)"},
    {"id":"f6","dataset":"firma","title":"Oddělení s vysokými platy","hint":"SELECT oddelenie, MAX(mzda) AS max_mzda FROM zamestnanec GROUP BY oddelenie HAVING MAX(mzda) > 4000"},
    # servis
    {"id":"s1","dataset":"servis","title":"Mechanik s nejvíce auty","hint":"SELECT m.cisloM, m.meno, COUNT(DISTINCT o.spz) AS pocet_aut FROM mechanik m JOIN oprava o ON m.cisloM = o.cisloM GROUP BY m.cisloM, m.meno ORDER BY pocet_aut DESC, m.cisloM ASC LIMIT 1"},
    {"id":"s2","dataset":"servis","title":"Náklady na opravu auta","hint":"SELECT a.spz, a.znacka, SUM(o.cena) AS celkem FROM auto a JOIN oprava o ON a.spz = o.spz GROUP BY a.spz, a.znacka"},
    {"id":"s3","dataset":"servis","title":"Průměrná cena opravy podle značky","hint":"SELECT a.znacka, AVG(o.cena) AS prumerna_cena FROM auto a JOIN oprava o ON a.spz = o.spz GROUP BY a.znacka"},
    {"id":"s4","dataset":"servis","title":"Značky pouze od Adama","hint":"SELECT DISTINCT a.znacka FROM auto a JOIN oprava o ON a.spz = o.spz JOIN mechanik m ON o.cisloM = m.cisloM WHERE m.meno = 'Adam' AND NOT EXISTS (SELECT 1 FROM oprava o2 JOIN mechanik m2 ON o2.cisloM = m2.cisloM JOIN auto a2 ON o2.spz = a2.spz WHERE a2.znacka = a.znacka AND m2.meno <> 'Adam')"},
    {"id":"s5","dataset":"servis","title":"Auta s náklady > 50000","hint":"SELECT a.spz, a.znacka, SUM(o.cena) AS celkem FROM auto a JOIN oprava o ON a.spz = o.spz GROUP BY a.spz, a.znacka HAVING SUM(o.cena) > 50000"},
    {"id":"s6","dataset":"servis","title":"Mechanici všechny typy oprav","hint":"SELECT m.cisloM, m.meno FROM mechanik m JOIN oprava o ON m.cisloM = o.cisloM GROUP BY m.cisloM, m.meno HAVING COUNT(DISTINCT o.typ) = 3"},
    {"id":"s7","dataset":"servis","title":"Mechanici nad průměrnou cenou","hint":"SELECT m.cisloM, m.meno, AVG(o.cena) AS prumerna_cena FROM mechanik m JOIN oprava o ON m.cisloM = o.cisloM GROUP BY m.cisloM, m.meno HAVING AVG(o.cena) > (SELECT AVG(cena) FROM oprava)"},
    # dodavatele
    {"id":"d1","dataset":"dodavatele","title":"Dodavatelé HD 30 GB","hint":"SELECT DISTINCT d.nazev FROM dodavatel d JOIN dodava da ON d.ico = da.ico JOIN zbozi z ON da.kod = z.kod WHERE z.nazev = 'HD 30 GB'"},
    {"id":"d2","dataset":"dodavatele","title":"Nejnižší cena HD 30 GB","hint":"SELECT d.nazev, da.cena FROM dodavatel d JOIN dodava da ON d.ico = da.ico JOIN zbozi z ON da.kod = z.kod WHERE z.nazev = 'HD 30 GB' AND da.cena = (SELECT MIN(da2.cena) FROM dodava da2 JOIN zbozi z2 ON da2.kod = z2.kod WHERE z2.nazev = 'HD 30 GB')"},
    {"id":"d3","dataset":"dodavatele","title":"Počet druhů zboží na dodavatele","hint":"SELECT d.nazev, COUNT(*) AS pocet FROM dodavatel d JOIN dodava da ON d.ico = da.ico GROUP BY d.nazev ORDER BY d.nazev"},
    {"id":"d4","dataset":"dodavatele","title":"Počet dodavatelů na zboží","hint":"SELECT z.nazev, COUNT(*) AS pocet_dodavatelu FROM zbozi z JOIN dodava da ON z.kod = da.kod GROUP BY z.nazev ORDER BY pocet_dodavatelu DESC"},
    {"id":"d5","dataset":"dodavatele","title":"Zboží od jediného dodavatele","hint":"SELECT z.nazev AS zbozi_nazev, d.nazev AS dodavatel_nazev FROM zbozi z JOIN dodava da ON z.kod = da.kod JOIN dodavatel d ON da.ico = d.ico WHERE z.kod IN (SELECT kod FROM dodava GROUP BY kod HAVING COUNT(*) = 1)"},
    {"id":"d6","dataset":"dodavatele","title":"Dodavatelé s více než 2 produkty","hint":"SELECT d.nazev, COUNT(*) AS pocet FROM dodavatel d JOIN dodava da ON d.ico = da.ico GROUP BY d.nazev HAVING COUNT(*) > 2"},
    {"id":"d7","dataset":"dodavatele","title":"Kroměřížští dodavatelé nejdražšího","hint":"SELECT d.nazev, MAX(da.cena) AS max_cena FROM dodavatel d JOIN dodava da ON d.ico = da.ico WHERE d.mesto = 'Kromeriz' GROUP BY d.nazev HAVING MAX(da.cena) > 5000"},
    {"id":"d8","dataset":"dodavatele","title":"Dodavatelé nad průměrnou vzdáleností","hint":"SELECT nazev, mesto, vzdalenost FROM dodavatel WHERE vzdalenost > (SELECT AVG(vzdalenost) FROM dodavatel)"},
]


def run_one(q):
    conn = sqlite3.connect(":memory:")
    conn.executescript(DATASETS[q["dataset"]])
    cur = conn.cursor()
    try:
        cur.execute(q["hint"])
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        return {"ok": True, "cols": cols, "rows": rows, "count": len(rows)}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        conn.close()


def main():
    fails = []
    passes = []
    for q in QUESTIONS:
        res = run_one(q)
        if not res["ok"]:
            fails.append((q, res["error"]))
            print(f"FAIL {q['id']} ({q['title']}): {res['error']}")
        else:
            passes.append((q, res))
            print(f"PASS {q['id']} ({q['title']}): {res['count']} rows, cols={res['cols']}")

    print(f"\n=== SUMMARY ===")
    print(f"Passed: {len(passes)} / {len(QUESTIONS)}")
    print(f"Failed: {len(fails)} / {len(QUESTIONS)}")
    if fails:
        print("\nFailed questions:")
        for q, err in fails:
            print(f"  {q['id']} {q['title']} [{q['dataset']}]")
            print(f"    SQL: {q['hint']}")
            print(f"    ERROR: {err}")
        sys.exit(1)
    else:
        print("All OK!")


if __name__ == "__main__":
    main()
