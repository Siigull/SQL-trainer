drop table Dodavatel cascade constraints;
drop table Dodava cascade constraints;
drop table Zbozi cascade constraints;

create table Dodavatel
(
	ICO int
		constraint Dodavatel_pk
			primary key,
	nazev varchar(50),
	mesto varchar(50),
	vzdalenost int
)
/


create table Zbozi
(
	kod int
		constraint Zbozi_pk
			primary key,
	nazev varchar(50),
	vyrobce varchar(50)
)
/


create table Dodava
(
	ICO int,
	foreign key (ICO) references DODAVATEL(ICO),
	kod int,
	foreign key (kod) references ZBOZI(kod), 
	cena int
)
/

ALTER TABLE Dodava
ADD CONSTRAINT Dodava_PK PRIMARY KEY (ico, kod);

insert into DODAVATEL VALUES (0,'CojavimCorp','Olomouc',67);
insert into DODAVATEL VALUES (1,'Stark','Kromezir',125);
insert into DODAVATEL VALUES (2,'Dodavatel od vedle','Kromezir',12);
insert into DODAVATEL VALUES (3,'AiAi','Hradec Kralove',91);
insert into DODAVATEL VALUES (4,'Datemer','Hradec Kralove',350);
insert into DODAVATEL VALUES (5,'Elektromadar','Kromezir',261);
insert into DODAVATEL VALUES (6,'Hae','Praha',311);
insert into DODAVATEL VALUES (7,'Petr','Olomouc',237);
insert into DODAVATEL VALUES (8,'Elektro plus','Brno',68);
insert into DODAVATEL VALUES (9,'Zeus','Hradec Kralove',85);
insert into ZBOZI VALUES (0,'HD 30 GB','Kingston');
insert into ZBOZI VALUES (1,'Flashka 3000','Kingston');
insert into ZBOZI VALUES (2,'HD monitor','Kingston');
insert into ZBOZI VALUES (3,'Televize ako stena','Sony');
insert into ZBOZI VALUES (4,'Nejakej mobil','Panasonic');
insert into ZBOZI VALUES (5,'Ultrahyperturbo vysavac','Panasonic');
insert into ZBOZI VALUES (6,'proste jmeno produktu','Sony');
insert into ZBOZI VALUES (7,'Modra lampicka','Samsung');
insert into ZBOZI VALUES (8,'Draha krabice','Sony');
insert into ZBOZI VALUES (9,'Notebook','Samsung');
insert into DODAVA VALUES (7,6,156);
insert into DODAVA VALUES (8,9,7310);
insert into DODAVA VALUES (4,8,776);
insert into DODAVA VALUES (5,1,174);
insert into DODAVA VALUES (1,8,5594);
insert into DODAVA VALUES (0,6,7148);
insert into DODAVA VALUES (8,8,9709);
insert into DODAVA VALUES (7,7,6921);
insert into DODAVA VALUES (5,9,4284);
insert into DODAVA VALUES (3,6,8579);
insert into DODAVA VALUES (2,1,3053);
insert into DODAVA VALUES (2,0,9156);
insert into DODAVA VALUES (6,3,8844);
insert into DODAVA VALUES (3,9,2456);
insert into DODAVA VALUES (7,2,2750);
insert into DODAVA VALUES (4,4,8708);
insert into DODAVA VALUES (2,7,5308);
insert into DODAVA VALUES (5,7,9704);
insert into DODAVA VALUES (1,4,8709);
insert into DODAVA VALUES (2,4,6805);
insert into DODAVA VALUES (1,7,7213);
insert into DODAVA VALUES (9,8,9138);
insert into DODAVA VALUES (6,1,4431);
insert into DODAVA VALUES (4,7,3345);
insert into DODAVA VALUES (5,7,9193);
insert into DODAVA VALUES (1,9,5812);
insert into DODAVA VALUES (6,6,9745);
insert into DODAVA VALUES (4,9,2960);
insert into DODAVA VALUES (2,3,8989);
insert into DODAVA VALUES (7,1,9124);
insert into DODAVA VALUES (8,2,9323);
insert into DODAVA VALUES (5,0,926);
insert into DODAVA VALUES (1,5,7343);
insert into DODAVA VALUES (5,7,9497);
insert into DODAVA VALUES (9,8,5371);
insert into DODAVA VALUES (7,3,6483);
insert into DODAVA VALUES (7,2,3038);
insert into DODAVA VALUES (3,4,8520);
insert into DODAVA VALUES (3,8,3805);
insert into DODAVA VALUES (0,6,305);

commit;

-- Ukol 1
-- Kteří dodavatelé dodávají zboží s názvem ‘HD 30 GB‘ ?
SELECT dodavatel.nazev from Dodavatel, Dodava, Zbozi
WHERE Dodavatel.ICO = Dodava.ICO and Dodava.kod = Zbozi.kod and Zbozi.nazev = 'HD 30 GB';

SELECT dodavatel.nazev 
FROM dodavatel, zbozi, dodava  
WHERE zbozi.nazev = 'HD 30 GB' AND dodavatel.ICO = dodava.ICO AND dodava.kod = zbozi.kod;

SELECT DODAVATEL.NAZEV, dodava.cena from DODAVATEL
INNER JOIN DODAVA on DODAVA.ICO = DODAVATEL.ICO INNER JOIN ZBOZI on ZBOZI.KOD = DODAVA.KOD  where ZBOZI.nazev = 'HD 30 GB';


-- Ukol 2
-- Který dodavatel dodává zboží s názvem ‘HD 30 GB‘ za nejnižší cenu?
SELECT Dodavatel.nazev, min(dodava.cena)
FROM Dodavatel, Dodava, Zbozi
WHERE zbozi.nazev = 'HD 30 GB' AND dodavatel.ICO = dodava.ICO AND dodava.kod = zbozi.kod
and dodava.cena = ALL(
    SELECT min(dodava.cena) FROM Dodava, Zbozi
    WHERE zbozi.nazev = 'HD 30 GB' and dodava.kod = zbozi.kod)
GROUP BY Dodavatel.nazev;
    
-- pomocny select:
SELECT min(dodava.cena) FROM Dodava, Zbozi
    WHERE zbozi.nazev = 'HD 30 GB' and dodava.kod = zbozi.kod;

-- Ukol 3
-- Kolik druhů zboží dodávají jednotliví dodavatelé?
SELECT Dodavatel.nazev, COUNT(*) as pocet
FROM Dodavatel, Dodava d1
WHERE Dodavatel.ICO = d1.ICO
GROUP BY Dodavatel.nazev
ORDER by Dodavatel.nazev;

-- pomocny select:
SELECT Dodavatel.nazev, Zbozi.nazev as zbozi
FROM Dodavatel, Dodava d1, Zbozi
WHERE Dodavatel.ICO = d1.ICO and d1.kod = Zbozi.kod
ORDER by Dodavatel.nazev;

-- Ukol 4
-- Kolik dodavatelů dodává jednotlivé druhy zboží? Seřaďte sestupně podle počtu dodavatelů.
SELECT Zbozi.nazev, COUNT(*) as pocet_dodavatelu
FROM Zbozi, Dodava
WHERE Zbozi.kod = Dodava.kod
GROUP BY Zbozi.nazev
ORDER BY pocet_dodavatelu DESC;

-- Ukol 5
-- Které zboží dodává jen jeden dodavatel a kdo to je?
SELECT Z.nazev as zbozi_dodavane_jednim, D.nazev
FROM Zbozi Z, Dodava, Dodavatel D
WHERE Z.kod = Dodava.kod and Dodava.ICO = D.ICO
and 1 = ANY(
    SELECT COUNT(*)
    FROM Zbozi ZA, Dodava
    WHERE ZA.kod = Dodava.kod and ZA.kod = Z.kod 
    GROUP BY ZA.nazev
    );
    
-- Ukol 6
-- Kteří dodavatelé dodávají více než dva druhy zboží?
-- bez poctu - toto je delší, protože agregační funkce musí být vždy za SELECT
SELECT DISTINCT D.nazev
FROM Dodava, Dodavatel D
WHERE Dodava.ICO = D.ICO
and 2 <= ANY(
    SELECT COUNT(*)
    FROM Dodava, Dodavatel D2
    WHERE Dodava.ICO = D2.ICO and D.ICO = D2.ICO
    GROUP BY D.nazev
    )
ORDER BY D.nazev;

-- s poctem
SELECT NAZEV, COUNT(*) CNT
FROM DODAVATEL NATURAL JOIN DODAVA
GROUP BY NAZEV
HAVING COUNT(*) >= 2
ORDER BY nazev;




-- THE SAME, SOLVED BY TEDRO

-- Kteří dodavatelé dodávají zboží s názvem ‘HD 30 GB‘ ?
SELECT D.nazev FROM Dodavatel D JOIN Dodava D2 ON D.ICO = D2.ICO JOIN Zbozi Z ON D2.kod = Z.kod
    WHERE Z.nazev = 'HD 30 GB' GROUP BY D.nazev;
    
-- Který dodavatel dodává zboží s názvem ‘HD 30 GB‘ za nejnižší cenu?
SELECT D.nazev FROM Dodavatel D JOIN Dodava D2 ON D.ICO = D2.ICO JOIN Zbozi Z ON D2.kod = Z.kod
    WHERE Z.nazev = 'HD 30 GB' AND D2.cena =
        (SELECT MIN(D2.cena) FROM Dodavatel D JOIN Dodava D2 ON D.ICO = D2.ICO JOIN Zbozi Z ON D2.kod = Z.kod
            WHERE Z.nazev = 'HD 30 GB');
            
-- Kolik druhů zboží dodávají jednotliví dodavatelé?
SELECT D.nazev, COUNT(*) as pocet_druhu_zbozi FROM Dodavatel D JOIN Dodava D2 ON D.ICO = D2.ICO JOIN Zbozi Z ON D2.kod = Z.kod
    GROUP BY D.nazev;
    
-- Kolik dodavatelů dodává jednotlivé druhy zboží? Seřaďte sestupně podle počtu dodavatelů.
SELECT Z.nazev, COUNT(*) as pocet_dodavatelu FROM Dodavatel D JOIN Dodava D2 ON D.ICO = D2.ICO JOIN Zbozi Z ON D2.kod = Z.kod
    GROUP BY Z.nazev ORDER BY pocet_dodavatelu DESC;
    
-- Které zboží dodává jen jeden dodavatel a kdo to je?
SELECT Z.nazev, D.nazev FROM Dodavatel D JOIN Dodava D2 ON D.ICO = D2.ICO JOIN Zbozi Z ON D2.kod = Z.kod
    WHERE Z.kod = (SELECT N.kod 
    	FROM (SELECT Z.kod, COUNT(*) as pocet_dodavatelu FROM Dodavatel D JOIN Dodava D2 ON D.ICO = D2.ICO JOIN Zbozi Z ON D2.kod = Z.kod
		    GROUP BY Z.kod ORDER BY pocet_dodavatelu DESC) N 
	    WHERE pocet_dodavatelu = 1);

-- Kteří dodavatelé dodávají více než dva druhy zboží?     
SELECT D.nazev FROM Dodavatel D
    JOIN (SELECT D.ICO, COUNT(*) as pocet_druhu_zbozi FROM Dodavatel D JOIN Dodava D2 ON D.ICO = D2.ICO JOIN Zbozi Z ON D2.kod = Z.kod
        GROUP BY D.ICO) N ON N.ICO = D.ICO 
    WHERE N.pocet_druhu_zbozi > 2;
