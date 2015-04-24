-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop database if exists tournament;
create database tournament;
\c tournament;

--players table contains general information on each player
create table players(   name text, 
                        player_ID serial primary key );
--matches table contains information about a match between two players
create table matches ( player1 serial references players, 
                       player2 serial references players, 
                       player1_result text, 
                       player2_result text, 
                       match_ID serial, 
                       primary key(match_id ) );




--Creating a view that contains records of each player's wins and matches -- player standings
CREATE VIEW player_standings AS 
    SELECT 
        players.player_ID, 
        players.name, 
        CASE WHEN win_count.wins IS Null THEN 0 ELSE win_count.wins END, 
        --store 0 wins as '0' rather than 'null'
        CASE WHEN match_count.matches IS Null THEN 0 ELSE match_count.matches END, 
        --store 0 matches as '0' rather than 'null'
        row_number() over(PARTITION BY wins ORDER BY win_count.wins DESC) AS nrow 
        --numbering each row of each partition; implemented to be used by 'pairs' view
    FROM players                                                                    
    LEFT JOIN                                                                      
        (
        SELECT 
            player_ID, 
            count(*) AS matches 
            --counts how many times each player_ID appears across the rows of a table, to give the match count
        FROM 
            players, 
            matches 
        WHERE 
            (players.player_ID = matches.player1 OR players.player_ID = player2) 
        GROUP BY player_ID) 
    AS match_count 
    ON match_count.player_ID = players.player_ID 
    LEFT JOIN 
        (SELECT --counts how many times a corresponding 'wins' appears for each player over a table
            player_ID, 
            count(*) AS wins 
        FROM 
            players, matches 
        WHERE 
            (matches.player1_result = 'win' AND players.player_ID = matches.player1) 
            OR (matches.player2_result = 'win' AND players.player_ID = matches.player2) 
        GROUP BY player_ID) 
    AS win_count 
    ON win_count.player_ID = players.player_ID 
    ORDER BY players.player_ID DESC;


--Creating a view that contains pairs of players for the next round.

--The query accomodates for situations where there are an odd number of players with the
--same amount of wins.
CREATE VIEW pairs AS 
    SELECT 
        player_standings.player_ID AS p1ID, 
        player_standings.name AS p1Name, 
        matched_player.player_ID AS p2ID, 
        matched_player.name as p2Name 
    FROM player_standings 
    LEFT JOIN 
        (SELECT 
            player_ID, 
            name, 
            wins, 
            nrow 
        FROM player_standings) 
    AS matched_player 
    ON matched_player.wins = player_standings.wins AND matched_player.nrow = player_standings.nrow+1
    WHERE player_standings.nrow % 2 = 1;
--to accomodate for the extra credit task - I have adapted my table to accomodate for a tie. Therefore, both players are specified, and the outcome for each player is specified

