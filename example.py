from nvapi import NvidiaAPI

# Load DLL
api = NvidiaAPI(verbose=True)
print('Loaded')

# Initialize API
api.init()
print('Initialized')

# Display some info
print(f'> API Version: {api.interfaceVersion()}')
print(f'> Driver Version: {api.driverVersion()}')
print('')

print('Physical GPUs:')
for gidx, gpu in enumerate(api.getPhysicalGPUs()):
	print(f'GPU{gidx}: {gpu.getFullName()}')
	print(f' > Core Count: {gpu.getCoreCount()}')
	print(f' > BIOS Version: {gpu.getBiosVersion()}')
	print(f' > BIOS Revision: {gpu.getBiosRevision()}')
	print(f' > BIOS OEM Revision: {gpu.getBiosOEMRevision()}')
	print(f' > Bus ID: {gpu.getBusId()}')
	print(f' > Bus Slot ID: {gpu.getBusSlotId()}')
	print(f' > Perf Decrease Info: {gpu.getPerfDecreaseInfo().name}')
	print(f' > Performance State: {gpu.getPerfState().name}')
	
	print(f' > Memory Info')
	for key, value in gpu.getMemoryInfo().items():
		print(f'  - {key}: {round(value,2)} MB')

	print(' > Thermal Sensors')
	for sidx, sensor in enumerate(gpu.getThermalSensors()):
		print(f'  - {sidx}: {sensor["target"].name}, {sensor["controller"].name}, {sensor["currentTemp"]}C')
	

	try: 
		print(f' > Cooler Tachometer: {gpu.getTachReading()}')
	except: 
		pass
print('')

# Done
api.dispose()
print('Disposed')