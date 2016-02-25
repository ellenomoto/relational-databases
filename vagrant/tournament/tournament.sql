-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--CREATE DATABASE tournament;

CREATE TABLE Player (
id SERIAL PRIMARY KEY,
name VARCHAR(30),
wins INTEGER,
losses INTEGER,
ties INTEGER
);

CREATE TABLE Match (
id SERIAL PRIMARY KEY,
winner INTEGER,
loser INTEGER
);
