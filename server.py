import socket

def decrypt(header):
    binary_string = ""
    for c in header:
        binary_string += bin(ord(c))[2:].zfill(8)
    print(binary_string)

    _id = int(binary_string[:8], 2)
    d = int(binary_string[9], 2)
    m = int(binary_string[10], 2)
    fragoffset = int(binary_string[11:24], 2)
    total_len = int(binary_string[24:], 2)

    return _id, d, m, fragoffset, total_len


def create_frag_files(data_stream):
    file_number = 0
    pointer = 0

    print("`````````````````````````````````````````````````````````````````````````````````")

    while(True):
        print(f"Received Fragment {file_number}.")
        header = data_stream[pointer:pointer+5]
        print(f"Encrypted header: {header}")
        _id, d, m, fragoffset, total_len = decrypt(header)
        print(f"Decrypted header: {_id} {d} {m} {fragoffset} {total_len}")
        packet_data = data_stream[pointer+5:pointer+total_len]
        print(f"Packet data: {packet_data}")
        with open(f"re_frag{file_number}.txt", "w") as frag:
            frag.write(packet_data)
            frag.close()
        print(f"Created frag file re_flag{file_number}.txt\n")
        pointer += total_len
        file_number += 1

        if(pointer==len(data_stream)):
            print("`````````````````````````````````````````````````````````````````````````````````")
            break
    
    return file_number


def create_received_file(client_socket, file_name):
    total_data = ""
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        total_data += data
    number_of_files = create_frag_files(total_data)
    with open(file_name, 'w') as file:
        for i in range(number_of_files):
            frag_data = ""
            with open(f"re_frag{i}.txt", 'r') as frag:
                frag_data = frag.read()
                frag.close()
            file.write(frag_data)
        file.close()



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 5000

    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    connection, address = server_socket.accept()
    print(f"Connection from {address}")

    try:
        file_name = "receivedFile.txt"
        create_received_file(connection, file_name)
        print(f"File '{file_name}' received successfully")

    except Exception as err:
        print("Error has occured!")
        print(err)

    connection.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
