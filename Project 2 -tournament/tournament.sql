-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


--players table contains general information on each player
create table players ( name text, player_ID serial primary key );
--matches table contains information about a match between two players
create table matches ( player1 serial references players, player2 serial references players, player1_result text, player2_result text, tournament_ID int , match_ID serial, primary key(match_id ) );

