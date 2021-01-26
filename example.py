from nvapi import NvidiaAPI, NvidiaClockDomain

# Load DLL and Initialize
api = NvidiaAPI(verbose=True)
api.init()

# Display clocks for every GPU
for gidx, gpu in enumerate(api.getPhysicalGPUs()):
	print(f'GPU{gidx}: {gpu.getFullName()}')
	states = gpu.getPerfStates()

	print(f"Editable: {states.blsEditable}")
	print(f"PerfStates:")
	for state in states.pstates[:states.numPstates]:
		print(f' P{state.pStateId}, editable:{state.blsEditable}')
		for clock in state.clocks[:states.numClocks]:
			print(f'  Clock, domain:{NvidiaClockDomain(clock.domainId).name} type:{clock.typeId} edit:{clock.blsEditable}')
			print(f'   freqDelta, min:{clock.freqDelta_kHz.valueRange.min} max:{clock.freqDelta_kHz.valueRange.max} value:{clock.freqDelta_kHz.value}')
			print(f'   data, single: {clock.data.single.freq_Khz}')

# Done
api.dispose()