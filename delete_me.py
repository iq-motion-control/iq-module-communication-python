import iqmotion

com = Communication('USB0')
port = port.open("usb0")
my_motor1 = IQModuleSimple('dev/ttyUSB1', 0)
my_motor2 = IQModule('dev/ttyUSB0', 2)


my_motor1.set("client1", "client_entry", my_value)

my_motor1.client1.client_entry.set(my_value)

my_motor1.set.client1.client_entry(my_value)  # ugly


my_value, success = my_motor1.getAndCheck("client1", "client_entry")
