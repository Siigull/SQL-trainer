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
