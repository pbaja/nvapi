import sys
from nvapi import NvidiaAPI, NvidiaError, NvidiaStatus

# Load and initialize API
api = NvidiaAPI()

# Get GPU0
gpu = api.list_gpus()[0]
print(f'Targeting {gpu.general.full_name()}')

# Print clocks
states = gpu.performance.perf_states()
core_current = states.pstates[0].clocks[0].data.range.maxFreq_kHz // 1000
core_offset = states.pstates[0].clocks[0].freqDelta_kHz.value // 1000
print(f'Core P0 Clock: {core_current} Mhz, offset: {core_offset} Mhz')

if core_offset == 50:
    print('Already overclocked!')
    sys.exit(0)

# Add 50Mhz offset to overclock (reusing states struct obtained earlier)
states.pstates[0].clocks[0].freqDelta_kHz.value = 50 * 1000 # 50Mhz offset on first pstate slot, first clock slot. It already has set ClockDomain as GRAPHICS
states.numPstates = 1 # We are changing one Pstate
states.numClocks = 1 # We are changing one clock
states.numBaseVoltages = 0 # We are not changing any base voltages

# Apply changed clocks
print('Overclocking +50Mhz')
try:
    gpu.performance.set_perf_states(states)
except NvidiaError as e:
    if e.status == NvidiaStatus.INVALID_USER_PRIVILEGE:
        print('Error! Overclocking is available only for administrators. Try again with admin rights.')
        sys.exit(0)
    else:
        raise e

# Print clocks again
states = gpu.performance.perf_states()
oc_core_current = states.pstates[0].clocks[0].data.range.maxFreq_kHz // 1000
oc_core_offset = states.pstates[0].clocks[0].freqDelta_kHz.value // 1000
print(f'Core P0 Clock: {oc_core_current} Mhz, offset: {oc_core_offset} Mhz')

# Check
if oc_core_current == core_current + 50:
    print('Success!')

# Done
api.dispose()