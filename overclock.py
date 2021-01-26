from nvapi import NvidiaAPI, NvidiaClockDomain, NvidiaClockType

# Load DLL and Initialize
api = NvidiaAPI(verbose=True)
api.init()

def sign_char(value):
    return '+' if value >= 0 else ''
def pstate_val(idx, curr):
    return f'[P{idx}]' if idx == curr else f'P{idx}'

# List GPUs
gpus = api.getPhysicalGPUs()
def printInfo():
    print('-----------------------')
    for idx, gpu in enumerate(gpus):
        name = gpu.getFullName()
        states = gpu.getPerfStates()
        state = gpu.getPerfState()
        
        print(f'GPU{idx}: {name}')

        pstate_str = ' '.join([pstate_val(x, state) for x in range(13)])
        print(f' - Pstate: {pstate_str}')

        core_curr = states.pstates[0].clocks[0].data.range.maxFreq_kHz // 1000
        core_offs = states.pstates[0].clocks[0].freqDelta_kHz.value // 1000
        print(f' - Core: {core_curr}Mhz {sign_char(core_offs)}{core_offs}Mhz')

        mem_curr = states.pstates[0].clocks[1].data.range.maxFreq_kHz // 1000
        mem_offs = states.pstates[0].clocks[1].freqDelta_kHz.value // 1000
        print(f' - Mem: {mem_curr}Mhz {sign_char(mem_offs)}{mem_offs}Mhz')
    print('-----------------------')


printInfo()
print('Will overclock GPU0 Core by 50Mhz')
struct = gpus[0].getPerfStates()
struct.pstates[0].clocks[0].freqDelta_kHz.value = 0 * 1000
struct.numPstates = 1
struct.numClocks = 1
struct.numBaseVoltages = 0
gpus[0].setPerfStates(struct)
print('Done')
printInfo()

# Done
api.dispose()