Use Birdcage to constrain tweets.

Library to take text collections and create a Phrase of those text collections
and fit within the specified length.

This library allows you to send different length text items to generate a
phrase. When the phrase is generated with a maximum length, the maximum length
text items are selected.

If you have a message that you're trying to generate to post on Twitter, 
you may represent a time horizon in multiple ways. If you have the room for
the longest representation, you would use that, but, if the rest of your
message contains text that needs to be represented, Birdcage will try to 
assemble the phrase using the longest submitted text objects.

Here's how Birdcage works:

No maximum set, generate phrase. In this case, we're sending four different
representations of the time, and a fixed text that can be trimmed if required.
Since there is no maximum length set, the generated phrase will contain the
longest elements and won't trim the Text that has the trim attribute set.

a = Text('one hour, fourty-five minutes', '1 hour, 45 minutes', '1h45m', '1:45')
b = Text('until armageddon strikes the earth', trim=True)
phrase = Phrase(a, b)

phrase contains 'one hour, fourty-five minutes until armageddon strikes the earth'


No maximum length set, generate phrase with ": " as the delimiter In this
case, we're sending four different representations of the time, and a
fixed text that can be trimmed if required. Since there is no maximum
length set, the generated phrase will contain the longest elements and
won't trim the Text that has the trim attribute set.

a = Text('one hour, fourty-five minutes', '1 hour, 45 minutes', '1h45m', '1:45')
b = Text('until armageddon strikes the earth', trim=True)
phrase = phrase.generate(delimiter=': ')

phrase contains 'one hour, fourty-five minutes: until armageddon strikes the earth'


Set a maximum length of 40 characters. In this case, we're sending four 
different representations of the time, and a fixed text that can be
trimmed if required. Since there is a maximum length of 40 characters set,
the generated phrase will contain the shortest time element and will trim
the Text that has the trim attribute set.

a = Text('one hour, fourty-five minutes', '1 hour, 45 minutes', '1h45m', '1:45')
b = Text('until armageddon strikes the earth', trim=True)
phrase = phrase.generate(length=40)

phrase contains '1h45m until armageddon strikes the earth'


Set a maximum length of 30 characters. In this case, we're sending four 
different representations of the time, and a fixed text that can be
trimmed if required. Since there is a maximum length of 40 characters set,
the generated phrase will contain the shortest time element and will trim
the Text that has the trim attribute set.

a = Text('one hour, fourty-five minutes', '1 hour, 45 minutes', '1h45m', '1:45')
b = Text('until armageddon strikes the earth', trim=True)
phrase = phrase.generate(length=40)

expecting: 1h45m until armageddon stri...
received:  1h45m until armageddon stri...
