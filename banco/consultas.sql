SELECT * FROM Disciplina;

SELECT * FROM Usuario;

SELECT * FROM Disciplina WHERE nome = 'Cálculo I';

SELECT id_disciplina, nome, carga_horaria 
FROM Disciplina 
ORDER BY carga_horaria DESC;

SELECT nome, email 
FROM Usuario 
ORDER BY nome ASC;