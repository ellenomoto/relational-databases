#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE from Match;")
    conn.commit() 
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE from Player;")
    conn.commit() 
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) from Player;")
    playerCount = c.fetchone()[0]
    conn.commit() 
    conn.close()
    return playerCount

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    x = name
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Player (name, wins, losses, ties) VALUES (%s, %s, %s, %s);", (name, 0, 0, 0))
    conn.commit() 
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    playerStandings = []
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * from Player;")
    for player in c:
        playerStandings.append((player[0], player[1], player[2], player[2]+player[3]+player[4]))
    conn.commit() 
    conn.close()
    return sorted(playerStandings, key=lambda x: x[2])


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Match (winner, loser) VALUES (%s, %s);", (winner, loser))
    c.execute("UPDATE Player SET wins = wins+1 WHERE id=%s;", (winner,))
    c.execute("UPDATE Player SET losses = losses+1 WHERE id=%s;", (loser,))
    conn.commit() 
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    playerRankings = playerStandings()
    swissPairs = []
    for index in range(len(playerRankings)/2):
        player1 = playerRankings[index*2]
        player2 = playerRankings[(index*2)+1]
        swissPairs.append((player1[0], player1[1], player2[0], player2[1]))
    return swissPairs


