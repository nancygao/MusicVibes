import socket
import time

power = 63

def set_to_hex(a_set):
    i = 0
    for n in a_set:
        i += 2**(7-n)
    return bytes([i])

def term(s):
    s.send(b'\xff')

def set_power(s, power):
    if power < 0 or power > 255:
        return
    s.send(b'\x04'+bytes([power]))

def set_pow(s, power):
    if power<0 or power > 1:
        return
    set_power(s, int(255*power))

def set_only_one(s, char):
    s.send(b'\x01'+bytes(char, 'utf8'))

def set_init(s, char1, char2):
    s.send(b'\x02'+bytes(char1+char2,'utf8'))

def set_push(s, char):
    s.send(b'\x00'+bytes(char, 'utf8'))

def set_lower_one(s, char):
    s.send(b'\x03'+bytes(char, 'utf8'))

def motor_test():
    sleep_time = 1
    TCP_IP = '127.0.0.1'
    TCP_PORT = 9874
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    set_power(s, power)
    s.send(b'\x0201')
    time.sleep(sleep_time)
    s.send(b'\x04'+bytes([63]))
    time.sleep(sleep_time)
    s.send(b'\x04'+bytes([255]))
    for i in range(2,8):
        time.sleep(sleep_time)
        s.send(b'\x00'+bytes(str(i),'utf8'))
    time.sleep(sleep_time)
    s.send(b'\x000')
    time.sleep(sleep_time)
    s.send(b'\x018')
    time.sleep(sleep_time)
    term(s)
    s.close()

def braille_alphabet():
    sleep_time = 1
    TCP_IP = '127.0.0.1'
    TCP_PORT = 9874
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    set_power(s, power)
    for char in 'abcdefghijklmnopqrstuvwxyz':
        set_only_one(s, char)
        time.sleep(sleep_time)
    term(s)
    s.close()

def power_test():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 9874
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    set_power(s, 63)
    set_only_one(s, '8')
    my_in = input()
    while my_in != '0' and my_in != '':
        set_power(s, int(my_in))
        my_in = input()
    term(s)
    s.close()

def power_test():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 9874
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    set_pow(s, .25)
    set_only_one(s, '8')
    my_in = input()
    while my_in != '0' and my_in != '':
        set_pow(s, float(my_in))
        my_in = input()
    term(s)
    s.close()

#braille_alphabet()
power_test()
