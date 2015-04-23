#Embedded file name: /vagrant/tournament/tournament.py
import psycopg2
import bleach
def connect():
    """Connect to the PostgreSQL database;  Returns a database connection."""
    return psycopg2.connect('dbname=tournament')

PG = connect()
DB = PG.cursor()
def deleteMatches():
    """Remove all the match records from the database."""
    DB.execute('DELETE FROM matches')


def deletePlayers():
    """Remove all player records from the database"""
    DB.execute('DELETE FROM players')



def countPlayers():
    """ Counts how many players are registered in the current tournament"""
    DB.execute('SELECT count(*) AS num FROM players')
    result = DB.fetchone()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database. Does so in a way that prevents 
    malicious code being inserted in to the database"""
    bleachedData = bleach.clean(name) #sanitizing input
    DB.execute('INSERT INTO players VALUES(%s)', ( bleachedData.encode('ascii') , ))

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB.execute('select player_ID, name, wins, matches from player_standings order by wins desc')
    standings = DB.fetchall()
    return standings


def reportMatch(player1, player2, player1_result, player2_result):#arguments must be changed in tournament_test module
    """Records the outcome of a single match between two players.
    outcome be winner/loser or winner/winner
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    DB.execute('SELECT count(*) FROM matches')
    nMatches = DB.fetchall()
    DB.execute('INSERT INTO matches VALUES(%s ,%s, %s, %s)', (player1,
     player2,
     player1_result,
     player2_result))
    DB.execute('SELECT * FROM matches')
    a = DB.fetchall()
    return a

def swissPairings():
    """Returns a list of pairs of players for the next round of a match."""    

    """ If a player cannot be paired with another player, he/she is assigned
    a bye round and recieves a win. 
    If the player has already recieved a bye round, they do not recieve another """
    DB.execute('''SELECT p1ID 
        FROM pairs, matches 
        WHERE p2ID IS NULL AND p1ID != matches.player1 AND p1ID != matches.player2 ''')
        #don't give unmatched player a default win if he has already been allocated one
    defaultWinners = DB.fetchall()
    
    for player in defaultWinners:
        reportMatch(player, player, 'win', 'win') 

    DB.execute("SELECT * FROM pairs")
    pairs = DB.fetchall()
    print pairs
    return pairs

    """Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pass
