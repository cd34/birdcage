#!/usr/bin/env python

from birdcage import (Phrase,
                      Text)
"""
create a Text object with a series of possible strings
"""
a = Text('one hour, fourty-five minutes', '1 hour, 45 minutes', '1h45m', '1:45')

"""
create a Text object that has an additional phrase to be displayed
after the first Text object. We will set the attribute trim which will allow
this text to be sliced if there isn't enough room.
"""
b = Text('until armageddon strikes the earth', trim=True)

"""
Create the phrase from the Text objects
"""
phrase = Phrase(a, b)

"""
Generate the phrase
"""
print 'No maximum set, generate phrase\n'
print 'expecting:', 'one hour, fourty-five minutes until armageddon strikes the earth'
print 'expecting:', phrase.generate()
print '\n'


"""
Select a different delimiter between the Text objects
"""
print 'No maximum length set, generate phrase with ": " as the delimiter\n'
print 'expecting:', 'one hour, fourty-five minutes: until armageddon strikes the earth'
print 'expecting:', phrase.generate(delimiter=': ')
print '\n'

"""
Set a maximum length for the message. Birdcage will try to compact the string
gracefully.
"""
print 'Set a maximum length of 40 characters\n'
print 'expecting:', '1h45m until armageddon strikes the ea...'
print 'expecting:', phrase.generate(length=40)
print '\n'
