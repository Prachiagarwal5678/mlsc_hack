import serial
import sqlite3

change = 0
flag = 0
conn = sqlite3.connect('site.db')
cur = conn.cursor()
serial_port = 'COM5'
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)
while True:
    line = ser.readline().decode()
    line = str(line.strip())
    slot = line.split(" ")
    if (slot[0] == ''):
        continue
    if (slot[1] == '1' or slot[1] == '0'):
        flag = flag - 1
    print(slot[1])
    slot[1] = bool(int(slot[1]))
    print(slot[1])
    if(change != int(slot[1]) and flag != 3):
        cur.execute('UPDATE parking_lot SET parked=? WHERE slot_no=? AND level=1', [int(slot[1]), slot[0]])
        cur.execute("SELECT * FROM parking_lot WHERE parked=?", [int(slot[1])])
        flag = flag + 1
        print(cur.fetchone())
        conn.commit()
        change = not change

