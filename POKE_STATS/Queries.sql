DROP TABLE Pokemon_Stats;

-- Crear la tabla Pokemon_Stats
CREATE TABLE Pokemon_Stats (
    ID SERIAL PRIMARY KEY,
	poke_id INT,
    Name VARCHAR(255),
    Type_1 VARCHAR(255),
    Type_2 VARCHAR(255),
    Total INT,
    HP INT,
    Attack INT,
    Defense INT,
    Sp_Atk INT,
    Sp_Def INT,
    Speed INT,
    Generation INT,
    Legendary BOOLEAN
);

-- Copiar datos desde un archivo CSV a la tabla Pokemon_Stats
COPY Pokemon_Stats(poke_id, Name, Type_1, Type_2, Total, HP, Attack, Defense, Sp_Atk, Sp_Def, Speed, Generation, Legendary)
FROM '/mnt/50A68CE3A68CCB44/UTEC/2023_2/Software_02/Semana08/Lab/archive/Pokemon.csv' DELIMITER ',' CSV HEADER;
DROP TABLE Pokemon_Stats;

-- Crear la tabla Pokemon_Stats
CREATE TABLE Pokemon_Stats (
    ID SERIAL PRIMARY KEY,
	poke_id INT,
    Name VARCHAR(255),
    Type_1 VARCHAR(255),
    Type_2 VARCHAR(255),
    Total INT,
    HP INT,
    Attack INT,
    Defense INT,
    Sp_Atk INT,
    Sp_Def INT,
    Speed INT,
    Generation INT,
    Legendary BOOLEAN
);

-- Copiar datos desde un archivo CSV a la tabla Pokemon_Stats
COPY Pokemon_Stats(poke_id, Name, Type_1, Type_2, Total, HP, Attack, Defense, Sp_Atk, Sp_Def, Speed, Generation, Legendary)
FROM '/mnt/50A68CE3A68CCB44/UTEC/2023_2/Software_02/Semana08/Lab/archive/Pokemon.csv' DELIMITER ',' CSV HEADER;
