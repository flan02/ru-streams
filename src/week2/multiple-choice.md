# Multiple Choice Questions

We have a stream containing 3 messages with IDs as follows : 1-0 2-0 3-0

## Which of the following commands would return only the last message added to this stream?

Select all that apply.

x XRANGE teststream - + COUNT 1

✔ XRANGE teststream 3-0 3-0

x XREVRANGE teststream + +

✔ XREVRANGE teststream 3-0 3-0

✔ XREVRANGE teststream + - COUNT 1

## Which of the following statements about the XREAD, XRANGE, and XREVRANGE commands are true?

Select all that apply.

✔ Only XREAD can read from multiple streams at once

x XREAD, XRANGE and XREVRANGE can all be used in a blocking mode

✔ XREAD, XRANGE and XREVRANGE all support a COUNT option to set a maximum number of messages returned

✔ XREAD can be used in a way that does not require consumers to calculate message IDs when requesting data from the stream
