# COURSE 4 - WEEK 4 - MULTIPLE CHOICE QUESTIONS

What is the time complexity of seeking to a particular message in a Redis stream?

A - Choose one answer:

O(n) on the length of the stream

O(1) (Correct)

O(log n) on the length of the stream

O(n log(n))

What is the time complexity of scanning and returning messages from a Redis stream?

B - Choose one answer:

O(n) on the length of the stream

O(1)

O(log n) on the length of the stream

O(n) on the number of messages returned (Correct)

---

Suppose you're trying to decide whether to use a Redis stream, sorted set, or list. Memory efficiency is the most important criterion. How do you decide which data structure to use?

A - Choose one answer.

Choose the stream

Choose the sorted set

Choose the list

Generate realistic sample data, add the data to each data structure, and then compare the data structures using the MEMORY USAGE command (Correct)

B - If a stream’s growth is allowed to continue unchecked, what will eventually happen once the Redis Server runs out of memory?

Choose one answer.

Redis will automatically truncate the stream

Redis will delete the largest existing key in the keyspace

Redis will reject subsequent write operations (Correct)

Redis will exit with an out-of-memory error

C - Which implementation details account for the memory efficiency of Redis streams?

Choose two answers:

The use of a Radix Tree data structure (Correct)

The use of a Sorted Set data structure

Compression of repeated message field names (Correct)

Compression of message payloads using gzip

---

A - What's the limit in size for a single Redis stream data structure?

Choose one answer.

2^32 bytes

2^32 messages

A single stream can occupy as many bytes as a Redis cluster can provide.

A single stream can occupy as many bytes as a single Redis instance can provide. (Correct)

B - Which of the following are reasons for using consumer groups over a single consumer when processing a stream?

Choose two answers.

You need to write the result of processing to a new stream.

You need to segment the stream across different types of consumers.

You need to process the stream messages out-of-order. (Correct)

Processing the data in your stream requires multiple threads / CPUs in order to keep up (Correct)
