To run the program on Linux, first SSH in to the virtual machine, and change to the directory containing tournament.sql. From the corresponding directory, run 'psql -f tournament.sql' to run the code that creates the database. After creating the database, run 'python tournament_test.py' from the same directory to run the python application.

The arguments of reportMatch in tournament_test.py have been modified to accomodate to the extra credit task. "Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch." Also, I accidently deleted code in testPairings that checks to see if the pairs are correct. My application did pass 'testPairings' before I deleted that code though.

My project has been made to pass two of the extra credit tasks:

1. "Don’t assume an even number of players. If there is an odd number of players, assign one player a “bye” (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.""

2. "Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch.""