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
    print(f' - Current state: P{gpu.performance.perf_state()}')

    # Performance states
    info = gpu.performance.perf_states_info()
    for state in info.pstates:

        # Clocks in this pstate
        for clock in state.clocks:
            print(f' - {state.id.name} {clock.domain.name.title()} Clock: {clock.max} Mhz, offset: {clock.offset.value} Mhz, editable: {clock.is_editable}')

        # Base voltages in this pstate
        for bv in state.base_voltages:
            print(f' - {bv.domain.name} Voltage: {bv.voltage} V, offset: {bv.voltage_offset.value} V, offset range: {bv.voltage_offset.min} - {bv.voltage_offset.max}')

    # Thermal settings
    thermal = gpu.thermal.thermal_settings()
    for sensor in thermal.sensors:
        print(f' - Sensor {sensor.controller.name} Temp: {sensor.current} C, min: {sensor.min} C, max: {sensor.max} C, target: {sensor.target.name}')


# Dispose
api.dispose()