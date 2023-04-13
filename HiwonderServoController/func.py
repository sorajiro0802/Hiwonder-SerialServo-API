import serial

CMD_SERVO_MOVE = 0x03
CMD_GET_BATTERY_VOLTAGE = 0x0f
CMD_MULT_SERVO_POS_READ = 0x15

# set config
def setConfig(set_port = '/dev/ttyAMA0', timeout = 5):
    global _serial
    _serial = serial.Serial(set_port)
    _serial.baudrate = 9600
    _serial.parity = serial.PARITY_NONE
    _serial.bytesize = serial.EIGHTBITS
    _serial.stopbits = serial.STOPBITS_ONE
    _serial.timeout = timeout

# move any servo. (id: int[], position: int[], time: int)
def moveServoArray(id=None,position=None,time=None):
    buf = bytearray(b'\x55\x55')
    buf.append(5 + (len(id) * 3))
    buf.append(CMD_SERVO_MOVE)
    # # parameters
    buf.append(len(id))
    buf.extend([(0xff & time), (0xff & (time >> 8))])
    for i in range(len(id)):
        buf.append(id[i])
        buf.extend([(0xff & position[i]), (0xff & (position[i] >> 8))])
    _serial.write(buf)

# move the servo. (id: int, position: int, time: int)
def moveServo(id=None,position=None,time=None):
    buf = bytearray(b'\x55\x55')
    buf.append(8)
    buf.append(CMD_SERVO_MOVE)
    # parameters
    buf.append(1)
    buf.extend([(0xff & time), (0xff & (time >> 8))])
    buf.append(id)
    buf.extend([(0xff & position), (0xff & (position >> 8))])
    _serial.write(buf)

# get current voltage.
def getBatteryVoltage():
    buf = bytearray(b'\x55\x55')
    buf.append(2)
    buf.append(CMD_GET_BATTERY_VOLTAGE)
    _serial.write(buf)
    _serial.flush()
    result = _serial.read(5)
    a = result[4] | result[5] << 8
    return a

# get current servo angle. (ids: array[id_1, id_2, ... , id_n])
def multServoPosRead(ids):
    buf = bytearray(b'\x55\x55')
    servo_num = len(ids)
    buf.append(servo_num + 3)
    buf.append(CMD_MULT_SERVO_POS_READ)
    buf.append(servo_num)
    for id in ids:
        buf.append(id)
    _serial.write(buf)
    _serial.flush()
    result = _serial.readline()
    data = {}
    for num in range(servo_num):
        i = 3 * num
        data[result[5 + i]] = result[5 + i + 1] | result[5 + i + 2] << 8

    return data

def ServoPosRead(id):
    buf = bytearray(b'\x55\x55')
    servo_num = id
    buf.append(servo_num + 3)
    buf.append(CMD_MULT_SERVO_POS_READ)
    buf.append(servo_num)
    buf.append(id)
    _serial.write(buf)
    _serial.flush()
    res = _serial.read(8)
    data = {}
    data[res[5]] = res[6] | res[7] << 8
    return data


def deg2serialAngle(deg):
    min = 0
    max = 240 
    if min <= deg <= max:
        angle = int(1000/max*deg)
    else:
        # whereas
        angle = 0
    return angle

def serialAngle2deg(angle):
    max = 1000
    min = 0
    eps = 5
    if min - eps <= angle <= max + eps:
        deg = int(240/max*angle)
    else:
        # 0°の状態での取得値が6万になる事があるため
        deg = 0
    return deg