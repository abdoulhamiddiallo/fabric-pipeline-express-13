-- Contrôle dans WH_Ferje : une ligne par liaison, de la plus sobre à la plus gourmande
SELECT route, COUNT(*) AS traversees, SUM(CAST(cars AS int)) AS voitures, CAST(SUM(CAST(energy_kwh AS int)) * 1.0 / SUM(CAST(cars AS int)) AS decimal(6,2)) AS kwh_par_voiture FROM LH_Ferje.dbo.crossings GROUP BY route ORDER BY kwh_par_voiture;
