#!/usr/bin/env python

from birdcage import Phrase, Text

a = Text('one hour, fourty-five minutes', '1 hour, 45 minutes', '1h45m', '1:45')
b = Text('until armageddon strikes the earth', trim=True)

phrase = Phrase(a, b)

print('No maximum set, generate phrase\n')
print('expecting:', 'one hour, fourty-five minutes until armageddon strikes the earth')
print('received: ', phrase.generate())
print('\n')


print('No maximum length set, generate phrase with ": " as the delimiter\n')
print('expecting:', 'one hour, fourty-five minutes: until armageddon strikes the earth')
print('received: ', phrase.generate(delimiter=': '))
print('\n')

print('Set a maximum length of 40 characters\n')
print('expecting:', '1h45m until armageddon strikes the earth')
print('received: ', phrase.generate(length=40))
print('\n')

print('Set a maximum length of 30 characters\n')
print('expecting:', '1h45m until armageddon stri...')
print('received: ', phrase.generate(length=30))
print('\n')
