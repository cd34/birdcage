Use Birdcage to constrain tweets.

Library to take text collections and create a Phrase of those text collections
and fit within the specified length.

This is what the library does:

$ birdcage/example.py 
No maximum set, generate phrase

expecting: one hour, fourty-five minutes until armageddon strikes the earth
expecting: one hour, fourty-five minutes until armageddon strikes the earth


No maximum length set, generate phrase with ": " as the delimiter

expecting: one hour, fourty-five minutes: until armageddon strikes the earth
expecting: one hour, fourty-five minutes: until armageddon strikes the earth


Set a maximum length of 40 characters

expecting: 1h45m until armageddon strikes the ea...
expecting: 1h45m until armageddon strikes the ea...
