from nvapi import NvidiaAPI

# Load DLL and Initialize
api = NvidiaAPI(verbose=True)
print('API Loaded')
api.init()
print('API Initialized')

# Display some info
print(f'> API Version String: {api.interfaceVersion()}')
print(f'> Driver Version')
for key, value in api.driverVersion().items():
	print(f'  - {key}: {value}')
print('')

print('Physical GPUs:')
print('')
for gidx, gpu in enumerate(api.getPhysicalGPUs()):
	# General info
	print(f'GPU{gidx}: {gpu.getFullName()}')
	print(f' > Core Count: {gpu.getCoreCount()}')
	print(f' > BIOS Version: {gpu.getBiosVersion()}')
	print(f' > BIOS Revision: {gpu.getBiosRevision()}')
	print(f' > BIOS OEM Revision: {gpu.getBiosOEMRevision()}')
	print(f' > Bus ID: {gpu.getBusId()}')
	print(f' > Bus Slot ID: {gpu.getBusSlotId()}')
	print(f' > Perf Decrease Info: {gpu.getPerfDecreaseInfo().name}')
	print(f' > Performance State: {gpu.getPerfState().name}')
	# Memory
	print(f' > Memory Info')
	for key, value in gpu.getMemoryInfo():
		print(f'  - {key}: {round(value,2)} MB')
	# Thermal
	print(' > Thermal Sensors')
	for sidx, sensor in enumerate(gpu.getThermalSensors()):
		print(f'  - {sidx}: {sensor["target"].name}, {sensor["controller"].name}, {sensor["currentTemp"]}C')
	# Tachometer
	try: print(f' > Cooler Tachometer: {gpu.getTachReading()}')
	except: pass
	print('')

# Done
api.dispose()
print('API Disposed')