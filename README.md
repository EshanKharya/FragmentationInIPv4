# README


## Introduction:

This application models the IPv4 protocol's fragmentation process. It allows a user to input a message and an MTU size. The message input can be given as follows:
1. As the name of a .txt file stored within the same directory (a sample file called test_messages.txt has been provided)
2. By creating a new file through the Menu. This allows the user to enter number of lines in the message. It then takes input for each line and then creates a clientFile.txt which stores the message.

The client instance fragments the files into fragmentation files named frag_i.txt depending on the MTU size. Each fragment file has a header attached to it. These files are then sent to the server.

The server then processes the data using the headers, recreates each fragmented data and stores it in separate files named re_frag_i.txt (these files do not store the header alongwith the data). It then compiles all the data from each re_frag.txt file and generates a receivedFile.txt which contains the original message.

The user can then compare the receivedFile.txt with the original message to confirm that the message has been delivered successfully


## Header:

Like mentioned above, each fragment has a header attached to it. This header is of fixed size 5 Bytes, and can hence be represented as 5 ASCII characters in the fragmented file. The header is formatted as follows:

|ID------|-DM|FRAGOFFSET---|TOTAL_LEN--------|

1. ID => 8b, represents ID of the packet. Is generated randomly once, and is the same value for each fragment.
2. DM => 3b, represents the FLAG value. 
   - The first bit is reserved and is always 0
   - The second bit, D, represents "Do not fragment" when high. For this simple implementation, D is always set to 1
   - The third bit, M, represents "More fragments" when high. When M=0, the fragment is the last fragment of the parent packet.
3. FRAGOFFSET => 13b, represents the data fragmentation offset in 8 byte word, i.e., every bit in FRAGOFFSET represents an offset of 8 bytes (or 8 characters).
4. TOTAL_LEN => 16b, represents the total length of the datagram in 1 byte word, i.e., every bit in TOTAL_LEN represents 1 byte length. Has maximum length of the fragment including header = 2^16^ bytes = 65,535 bytes or characters.

NOTE: Header length is not included in the header as it is fixed!

The header is then converted to 5 ASCII characters by grouping the 40b binary stream into 5 chunks of 8 bits each and is then inserted to the start of every frag file by the client.


## Specifications:

A user must consider the following points before operating the application:

- Max MTU value: 65,535. Hence maximum data transferred in each fragment = 65,535 - 5 = 65,530 bytes or characters

- As the terminal outputs may be long, sometimes the terminal may not print the entire output. In such cases, refer to the created files to validate the output.

- The application does not include the following IPv4 header parameters to maintain simplicity:
  * VER
  * HLEN
  * TOS
  * T2L
  * PROTOCOL
  * CHECKSUM
  * SOURCE IP ADDRESS
  * RECEIVER IP ADDRESS
  * OPTIONS

- The application also provides the following default MTU values for the user to choose from:
  * Ethernet => 1500B
  * Token Ring => 4464B
  * Hyperchannel => 65535B
  * The user can also specify CUSTOM MTU values that range between 6B and 65,535B

- The MTU INCLUDES the header size.
