import time
import socket
import sys
import serial
import serial.tools.list_ports

def set_to_hex(a_set):
    i = 0
    for n in a_set:
        i += 2**(7-n)
    return bytes([i])

my_dict = {}

my_dict['a']= {7}
my_dict['b']= {6,7}
my_dict['c']= {1,7}
my_dict['d']= {1,2,7}
my_dict['e']= {2,7}
my_dict['f']= {1,6,7}
my_dict['g']= {1,2,6,7}
my_dict['h']= {2,6,7}
my_dict['i']= {1,6}
my_dict['j']= {1,2,6}
my_dict['k']= {5,7}
my_dict['l']= {5,6,7}
my_dict['m']= {1,5,7}
my_dict['n']= {1,2,5,7}
my_dict['o']= {2,5,7}
my_dict['p']= {1,5,6,7}
my_dict['q']= {1,2,5,6,7}
my_dict['r']= {2,5,6,7}
my_dict['s']= {1,5,6}
my_dict['t']= {1,2,5,6}
my_dict['u']= {3,5,7}
my_dict['v']= {3,5,6,7}
my_dict['w']= {1,2,3,6}
my_dict['x']= {1,3,5,7}
my_dict['y']= {1,2,3,5,7}
my_dict['z']= {2,3,5,7}

temp = set(my_dict.keys())

for a in temp:
    my_dict[a.upper()] = my_dict[a]

my_dict['up']= {0}
my_dict['up_right']= {1}
my_dict['right']= {2}
my_dict['bottom_right']= {3}
my_dict['bottom']= {4}
my_dict['bottom_left']= {5}
my_dict['left']= {6}
my_dict['up_left']= {7}
my_dict['clear'] = {}

my_dict['8']= {0}
my_dict['9']= {1}
my_dict['6']= {2}
my_dict['3']= {3}
my_dict['2']= {4}
my_dict['1']= {5}
my_dict['4']= {6}
my_dict['7']= {7}

my_dict['5'] = {0,1,2,3,4,5,6,7}

my_dict['0'] = {}

new_dict = {}
for a in my_dict.keys():
    new_dict[a] = set_to_hex(my_dict[a])

ports = list(serial.tools.list_ports.comports())
ser = serial.Serial()
ser.baudrate = 9600
for p in ports:
    if 'Arduino' in p.description:
        ser.port = p.device
        break

if ser.port is not None:
    ser.open()
else:
    raise(OSError('Could not find Arduino Leonardo in devices'))


def set_high_power(ser):
    ser.write(b'\x04'+bytes([255]))

def set_low_power(ser):
    ser.write(b'\x04'+bytes([63]))

def set_power(ser, byte):
    ser.write(b'\x04'+byte)

def ser_init(ser, byte_1, byte_2):
    ser.write(b'\x02'+byte_1+byte_2)

def ser_only_one(ser, byte):
    ser.write(b'\x01'+byte)

def ser_lower_one(ser, byte):
    ser.write(b'\x03'+byte)

def ser_push(ser, byte):
    ser.write(b'\x00'+byte)

def ser_term(ser):
    ser.write(b'\x01\x00')

def my_enqueue(ser, my_queue, my_byte):
    my_queue.append(my_byte)
    if(len(my_queue)==1):
        ser_only_one(ser, my_queue[0])

def my_dequeue(ser, my_queue):
    if len(my_queue)>1:
        my_queue.pop(0)
        ser_only_one(ser, my_queue[0])
    elif len(my_queue)==1:
        my_queue.pop(0)
        ser_term(ser)
    else:
        ser_term(ser)

def my_dumpqueue(my_queue):
    global cur_byte
    while(len(my_queue)>0):
        my_queue.pop(0)
        
def motor_test():
    ser_only_one(ser, new_dict['up'])
    time.sleep(1)
    #input()
    ser_only_one(ser, new_dict['up_right'])
    time.sleep(1)
    #input()
    ser_only_one(ser, new_dict['right'])
    time.sleep(1)
    #input()
    ser_only_one(ser, new_dict['bottom_right'])
    time.sleep(1)
    #input()
    ser_only_one(ser, new_dict['bottom'])
    time.sleep(1)
    #input()
    ser_only_one(ser, new_dict['bottom_left'])
    time.sleep(1)
    #input()
    ser_only_one(ser, new_dict['left'])
    time.sleep(1)
    #input()
    ser_only_one(ser, new_dict['up_left'])
    time.sleep(1)
    #input()
    ser_term(ser)

def settings_test():
    ser_init(ser, new_dict['f'], new_dict['o'])
    input()
    set_low_power(ser)
    input()
    set_high_power(ser)
    input()
    set_high_power(ser)
    input()
    ser_term(ser)

def listen():
    byte_queue = []
    TCP_IP = '127.0.0.1'
    TCP_PORT = 9874
    BUFFER_SIZE = 1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    while 1:
        data = conn.recv(1)
        print(data)
        if data==b'\x00':
            try:
                byte = new_dict[chr(conn.recv(1)[0])]
                ser_push(ser, byte)
            except:
                print('Key not found in dictionary', file=sys.stderr)
        elif data==b'\x01':
            try:
                byte = new_dict[chr(conn.recv(1)[0])]
                byte_queue = []
                ser_only_one(ser, byte)
            except:
                print('Key not found in dictionary', file=sys.stderr)
        elif data==b'\x02':
            try:
                byte_1 = new_dict[chr(conn.recv(1)[0])]
                byte_2 = new_dict[chr(conn.recv(1)[0])]
                ser_init(ser, byte_1, byte_2)
            except:
                print('Key not found in dictionary', file = sys.stderr)
        elif data==b'\x03':
            try:
                byte = new_dict[chr(conn.recv(1)[0])]
                ser_lower_one(ser, byte)
            except:
                print('Key not found in dictionary', file=sys.stderr)
        elif data == b'\x04':
            byte = conn.recv(1)
            set_power(ser, byte)
        elif data == b'\x05':
            my_enqueue(ser, byte_queue, new_dict[chr(conn.recv(1)[0])])
        elif data == b'\x06':
            my_dequeue(ser, byte_queue)
        elif data == b'':
            conn, addr = s.accept()
        elif data==b'\xFF':
            break

    ser_term(ser)
    s.close()

def braille_test():
    for char in 'abcdefghijklmnopqrstuvwxyz':
        ser_only_one(ser, new_dict[char])
        input()
    ser_term(ser)

def queue_test():
    byte_queue = []
    my_enqueue(ser, byte_queue, new_dict['up'])
    my_enqueue(ser, byte_queue, new_dict['bottom'])
    my_enqueue(ser, byte_queue, new_dict['left'])
    my_enqueue(ser, byte_queue, new_dict['right'])
    input()
    my_dequeue(ser, byte_queue)
    input()
    my_dequeue(ser, byte_queue)
    input()
    my_dequeue(ser, byte_queue)
    input()
    my_dequeue(ser, byte_queue)
    input()
    ser_term(ser)

#motor_test()
#settings_test()
listen()
#braille_test()
#ser_term(ser)
#queue_test()
