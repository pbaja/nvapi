from nvapi import NvidiaAPI, NvidiaClockDomain, NvidiaClockType

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
			clockDomain = NvidiaClockDomain(clock.domainId)
			clockType = NvidiaClockType(clock.typeId)
			print(f'  Clock, domain:{clockDomain.name} type:{clockType.name} edit:{clock.blsEditable}')
			print(f'   Delta, min:{clock.freqDelta_kHz.valueRange.min} kHz max:{clock.freqDelta_kHz.valueRange.max} kHz value:{clock.freqDelta_kHz.value} kHz')
			if clockType == NvidiaClockType.Single:
				print(f'   Data, freq:{clock.data.single.freq_khz} kHz')
			else:
				clockRange = clock.data.range
				print(f'   Data, min:{clockRange.minFreq_kHz} kHz max:{clockRange.maxFreq_kHz} kHz domain:{clockRange.domainId} minVoltage:{clockRange.minVoltage_uV} uV maxVoltage:{clockRange.maxVoltage_uV} uV')
	for voltage in states.voltages.voltages[:states.voltages.numVoltages]:
		print(f'Voltage, domain:{voltage.domainId} editable:{voltage.blsEditable} volt:{voltage.volt_uV} uV voltDelta:{voltage.voltDelta_uV} uV')

# Done
api.dispose()