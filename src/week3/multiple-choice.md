# Multiple Choice Questions

Which of the following factors may affect the speed at which an individual consumer can process a single message from a stream? Select all that apply.

x The rate at which producers add new messages to the stream

✔ Latency in the network connection between the consumer and the Redis server

✔ The data contained in the message

x The number of messages in the stream

---

What happens when you use the NOACK option with XREADGROUP?

Select all that apply.

✔ The message delivery semantics will change from at-least-once to at-most-once.

x Messages returned are added to the consumer’s Pending Entries List (PEL).

x The consumer will need to acknowledge each message manually after processing it using the XACK command.

✔ Redis will consider all messages returned by XREADGROUP to be acknowledged

---

What does the XGROUP DELCONSUMER command do?

Select all that apply.

✔ Deletes a consumer from a group

✔ Deletes the consumer's list of pending entries

x Sets the last delivered ID of the group to one before the deleted consumer's first pending message

x Deletes all consumers for a given consumer group
