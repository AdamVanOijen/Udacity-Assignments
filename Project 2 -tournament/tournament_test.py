#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, "win", "lose")
    reportMatch(id3, id4, "win", "lose")
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, "win", "lose")
    reportMatch(id3, id4, "win", "lose")
    standings = playerStandings()
    pairings = swissPairings()

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"


