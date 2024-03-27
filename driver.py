import sys
import usb.core
import usb.util

VID = 0x260d
WIRE_PID = 0x1112
WIRELESS_PID = 0x1114

INTERRUPT_EP = 0x82

TIMEOUT = 1000 

data_to_send = bytearray([0x08, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4a])

class DareuMouse:
	detached_kernel = False
	
	def __init__(self, VID, PID):
		# Find the device by vendor and product ID
		self.device = usb.core.find(idVendor=VID, idProduct=PID)
		self.configuration = self.device.get_active_configuration()
		self.interface = self.configuration.interfaces()[1]
		
		self.detach_kernel(self.interface.bInterfaceNumber)
		
		self.endpoint = self.interface.endpoints()[0]
		
	def send_interrupt(self, data, timeout=TIMEOUT):
		try:
			return self.endpoint.write(data,timeout)
		except: 
			sys.exit("can not send interrrupt")
	
	def send_control(self,bmRequestType,bRequest,wValue=0,wIndex=0,data_or_wLength=None,timeout=None):
		try:
			return self.device.ctrl_transfer(bmRequestType,bRequest,wValue,wIndex,data_or_wLength,timeout)
		except usb.core.USBError as e:
			sys.exit("ctrl_transfer fail: %s" % str(e))
	
	def detach_kernel(self, bInterfaceNumber):
		if(self.device.is_kernel_driver_active(bInterfaceNumber)):
			try:
				self.device.detach_kernel_driver(bInterfaceNumber)
				DareuMouse.detached_kernel = True
			except usb.core.USBError as e:
				sys.exit("could not detach kernel: %s" % str(e))
	
	def attach_kernel(self,bInterfaceNumber):
		if(DareuMouse.detached_kernel):
			self.device.attach_kernel_driver(bInterfaceNumber)
	
def main():
    
	try:
		mouse = DareuMouse(VID,WIRE_PID)
		print("working in wire mode")
	except:
		try:
			mouse = DareuMouse(VID,WIRELESS_PID)
			print("working in wireless mode")
		except:
			sys.exit("can not find device")
		
	#first send interrupt in then send control out receive control out and finally receive interrupt in	
	#print(mouse.send_interrupt())
	
	ret = mouse.send_control(0x21,0x09,wValue=0x0208,wIndex=0x0001,data_or_wLength=data_to_send)
	print(ret)
	

if __name__ == "__main__":
	main()

