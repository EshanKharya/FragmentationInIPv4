import math
import random
import socket

#Helper functions
def binaryToAscii(b_header):
    ascii_string = ""
    for i in range (5):
        chunk = b_header[i*8: (i+1)*8]
        ascii_string += chr(int(chunk, 2))
    return ascii_string

def makeClientFile(file_name, message):
    with open(file_name, "w") as client_file:
        client_file.write(message)
        client_file.close()


#main functions
def menu():
    welcome_string = """
    Welcome! \n
    Specifications Loadout:\n
    Header Specifications:\n
    1. HLEN => fixed of size 5B (hence, not included in the header).\n
    2. ID => 8b, represents ID of the superfile.\n
    3. DM => 3b, flag value. \n
    4. FRAGOFFSET => 13b, represents fragmentation offset in 8 byte word\n
    5. TOTAL_LEN => 16b, represents the total length of the datagram in 1 byte word.\n
    Hence, max MTU value => 65,535 (for hyperchannels)
    Max data size in the packet => 65,530 (for hyperchannels)
    \n
    Default values for MTU: \n
    1. Ethernet => 1500B \n
    2. Token Ring => 4464B \n
    3. Hyperchannels => 65535B \n
    """
    print(welcome_string)
    print("``````````````````````````````````````````````````````````````````````````````````````````")
    
    choice = input("Do you wish to create a new file? (y/n)")
    message = ""

    if (choice.lower() == "y"):
        lines = int(input("Enter number of lines in the text file: "))
        for i in range (lines):
            message += "\n"
            message += input(f"Enter line {i+1}: ")
        message = message[1:]
        makeClientFile("clientFile.txt", message)
    
    else:
        file_name = input("Enter filename in the directory: ")
        with open (file_name, "r") as client_file:
            message = client_file.read()

    choice2 = int(input("Enter MTU choice:\n 1. Ethernet(1500B)\n 2. Token Ring(4464B)\n 3. Hyperchannel(65535B)\n 4. Custom \n"))
    mtu = 0

    if (choice2==1):
        mtu = 1500
    elif (choice2==2):
        mtu = 4464
    elif (choice2==3):
        mtu = 65535
    else:
        mtu = int(input("Enter MTU value (min: 6B, max: 65535B): "))
    
    print("``````````````````````````````````````````````````````````````````````````````````````````")

    return message, mtu

def makeHeader(id, d, m, offset, datalen):
    b_id = bin(id)[2:].zfill(8)
    b_offset = bin(offset)[2:].zfill(13)
    b_total_len = bin(datalen+5)[2:].zfill(16)
    b_header = b_id + "0" + d + m + b_offset + b_total_len

    ascii_header = binaryToAscii(b_header)

    return ascii_header, int(b_total_len, 2)


def makeFragmentFiles(message, mtu):
    id = random.randint(0, 255)
    max_datalen = ((mtu - 5) // 8) * 8      #Closest multiple of 8 to MTU-12 which is the maximum permissible data length
    number_of_files = math.ceil(len(message)/max_datalen)       

    print(f"""
    Following is the fragmentation process
    1. id: {id}
    2. maximum length of data: {max_datalen}
    3. length of message: {len(message)}
    3. number of files: {number_of_files}
    The files are as follows: \n
    """)

    for i in range (number_of_files):
        print(f"File{i}:")

        d = "1"
        m = "0" if i == number_of_files - 1 else "1"
        offset = max_datalen*i//8        #(max_datalen*i)//8
        datalen = len(message) - max_datalen*i if i == number_of_files - 1 else max_datalen
        header, total_len = makeHeader(id, d, m, offset, datalen)
        
        print(f"""
        Header:
        1. id: {id}
        2. d: {d}
        3. m: {m}
        4. offset: {offset}
        5. total length: {total_len}
            """)

        with open (f"frag{i}.txt", "w") as frag:
            print(f"Encrypted header: f{header}")
            frag.write(header)
            data = message[i*max_datalen : min((i+1)*max_datalen, len(message))]
            print(f"Data to be written:\n{data}")
            frag.write(data)
            frag.close()
        
        print("")
    return number_of_files

def send_files(file_names):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 5000

    client_socket.connect((host, port))

    for file_name in file_names:
        with open(file_name, 'r') as file:
            for data in file:
                client_socket.sendall(data.encode())
    
    client_socket.close()

if __name__ == "__main__":
    message, mtu = menu()
    number_of_files = makeFragmentFiles(message, mtu)
    file_names = []
    for i in range (number_of_files):
        file_names.append(f"frag{i}.txt")
    
    send_files(file_names)




        