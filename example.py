from nvapi import NvidiaAPI, NvidiaClockDomain

# Load and initialize API
api = NvidiaAPI()

# List GPUs
gpus = api.list_gpus()
for idx, gpu in enumerate(gpus):

    # General info
    print(f'GPU{idx}')
    print(f' - Name: {gpu.general.full_name()}')
    print(f' - Core Count: {gpu.general.core_count()}')
    print(f' - BIOS Version: {gpu.general.bios_version()}')
    print(f' - BIOS Revision: {gpu.general.bios_revision()}')
    print(f' - BIOS OEM Revision: {gpu.general.bios_oem_revision()}')
    print(f' - Bus ID: {gpu.general.bus_id()}')
    print(f' - Bus Slot ID: {gpu.general.bus_slot_id()}')
    
    # Iterate over pstates
    print(f' - Current state: P{gpu.performance.perf_state()}')
    states = gpu.performance.perf_states()
    for state in states.pstates[:states.numPstates]:
        # Iterate over clocks
        for clock in state.clocks[:states.numClocks]:
            domain = NvidiaClockDomain(clock.domainId)
            current = clock.data.range.maxFreq_kHz // 1000
            offset = clock.freqDelta_kHz.value // 1000
            print(f' - P{state.pStateId} {domain.name.title()} Clock: {current} Mhz, offset: {offset} Mhz')

# Dispose
api.dispose()