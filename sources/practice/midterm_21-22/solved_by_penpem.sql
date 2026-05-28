SELECT s.cisloS, s.jmeno, SUM(p.kredity) kreditu_celkem
FROM Student s, Zapsal z, Predmet p
WHERE   s.cisloS=z.cisloS
AND     z.zkratkaP=p.zkratkaP
AND     z.ak_rok=2021
HAVING SUM(p.kredity) > 70
GROUP BY s.cisloS, s.jmeno;


SELECT s.jmeno, s.mesto
FROM Student s, Zapsal z, Predmet p
WHERE s.cisloS=z.cisloS
AND z.zkratkaP=p.zkratkaP
AND p.nazev='Matematika'
AND z.ak_rok=2021
AND z.body >= 50
ORDER BY s.jmeno ASC, s.mesto ASC;

CREATE VIEW novy_ziaci(cisloS, jmeno, mesto) AS
    SELECT DISTINCT s.cisloS, s.jmeno, s.mesto
    FROM Student s, Zapsal z
    WHERE NOT EXISTS (
            SELECT *
            FROM Zapsal z
            WHERE s.cisloS=z.cisloS
        );

COMMIT;
