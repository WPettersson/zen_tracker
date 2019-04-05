Zen doesn't not (as I write this) have any mechanism to let its customers know
about upcoming maintenance that might affect them, instead we have to keep
checking a website, so I wrote this script to do the checking for me.

# Usage

I use this is a cron job, it simply checks the current status and prints output
to standard out.

# Configuration

There is an optional prefix you can add, up near the top of the script. It
needs to be at least 4 numbers to work, and any more than 5 is quite
potentially useless, I don't know.

