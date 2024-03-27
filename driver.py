import sys
import usb.core
import usb.util

VID = 0x260d
WIRE_PID = 0x1112
WIRELESS_PID = 0x1114

END_POINT = 0x82
CONTROLL_EP = 0x00 #need to send contoll out using ctrl_transfer

data_to_send = bytearray([0x08, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4a])

class DareuMouse:
	def __init__(self):
		try:
			self.device = usb.core.find(idVendor=VID, idProduct=WIRE_PID)
		except:
			self.device = usb.core.find(idVendor=VID, idProduct=WIRELESS_PID)
		
		self.configuration = self.device.get_active_configuration()
		self.interface = self.configuration.interfaces()[1]
		self.endpoint = self.interface.endpoints()[0]
		self.detached_kernel = False
		
	#def send_interrupt():
	
	def send_control(self,bmRequestType,bRequest,wValue=0,wIndex=0,data_or_wLength=None,timeout=None):
		try:
			ret = self.device.ctrl_transfer(bmRequestType,bRequest,wValue,wIndex,data_or_wLength,timeout)
		except usb.core.USBError as e:
			sys.exit("ctrl_transfer fail: %s" % str(e))
		return ret
	
	def detach_kernel(self):
		if(device.is_kernel_driver_active(interface.bInterfaceNumber)):
			try:
				self.device.detach_kernel_driver(interface.bInterfaceNumber)
				self.detached_kernel = True
			except usb.core.USBError as e:
				sys.exit("could not detach kernel: %s" % str(e))
	
	def attach_kernel(self):
		if(self.detached_kernel):
			self.device.attach_kernel_driver(interface.bInterfaceNumber)
	
def main():
    # Find the device by vendor and product ID
	mouse = DareuMouse()
	#first send interrupt in then send control out receive control out and finally receive interrupt in	
	#send_interrupt()
	
	ret = mouse.send_control(0x21,0x09,wValue=0x0208,wIndex=0x0001,data_or_wLength=data_to_send)
	print(ret)
	

if __name__ == "__main__":
	main()

