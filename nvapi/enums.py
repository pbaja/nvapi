from enum import IntEnum, IntFlag
from .constants import *


# Flags

class NvidiaCoolerTarget(IntFlag):
    NONE         = 0b00000000
    GPU          = 0b00000001
    MEMORY       = 0b00000010
    POWER_SUPPLY = 0b00000100
    ALL = GPU | MEMORY | POWER_SUPPLY

class NvidiaClockDomain(IntFlag):
    GRAPHICS  = 0b00000000
    MEMORY    = 0b00000100
    PROCESSOR = 0b00000111
    UNDEFINED = NVAPI_MAX_GPU_PUBLIC_CLOCKS

class NvidiaPerfDecreaseReason(IntFlag):
    '''Bit mask for knowning the exact reason for performance decrease'''

    NONE               = 0b00000000 # No slowdown detected
    THERMAL_PROTECTION = 0b00000001 # Thermal slowdown/shutdown/POR thermal protection
    POWER_CONTROL      = 0b00000010 # Power capping / pstate cap 
    AC_BATT            = 0b00000100 # AC->BATT event
    API_TRIGGERED      = 0b00001000 # API triggered slowdown
    INSUFFICIENT_POWER = 0b00010000 # Power connector missing
    UNKNOWN            = 0x80000000 # Unknown reason

class NvidiaThermalTarget(IntFlag):
    '''Thermal targets used in thermal settings'''
    NONE         = 0b00000000
    GPU          = 0b00000001 # GPU core temperature
    MEMORY       = 0b00000010 # Memory modules temperature
    POWER_SUPPLY = 0b00000100 # Power supply temperature
    BOARD        = 0b00001000 # Board ambient temperature

    # These require ComputingDevice handle instead of PhysicalGpu
    VCD_BOARD    = 0b00001001 # Visual Computing Device
    VCD_INLET    = 0b00001010 # Visual Computing Device
    VCD_OUTLET   = 0b00001011 # Visual Computing Device

    ALL          = 0b00001111
    UNKNOWN      = 0b10000000 # -1


# Enums

class NvidiaClockType(IntEnum):
    SINGLE             = 0b00000000 # Domains that use single frequency value within given pstate
    RANGE              = 0b00000001 # Domains that allow range of frequency values within given pstate

class NvidiaThermalController(IntEnum):
    NONE = 0
    GPU_INTERNAL = 1
    ADM1032 = 2
    MAX6649 = 3 
    MAX1617 = 4
    LM99 = 5
    LM89 = 6
    LM64 = 7
    ADT7473 = 8
    SBMAX6649 = 9
    VBIOSEVT = 10
    OS = 11
    UNKNOWN = -1 

class NvidiaStatus(IntEnum):
    OK = 0
    ERROR = -1
    LIBRARY_NOT_FOUND = -2
    NO_IMPLEMENTATION = -3
    API_NOT_INITIALIZED = -4
    INVALID_ARGUMENT = -5
    NVIDIA_DEVICE_NOT_FOUND = -6
    END_ENUMERATION = -7
    INVALID_HANDLE = -8
    INCOMPATIBLE_STRUCT_VERSION = -9
    HANDLE_INVALIDATED = -10
    OPENGL_CONTEXT_NOT_CURRENT = -11
    INVALID_POINTER = -14
    NO_GL_EXPERT = -12
    INSTRUMENTATION_DISABLED = -13
    NO_GL_NSIGHT = -15
    EXPECTED_LOGICAL_GPU_HANDLE = -100
    EXPECTED_PHYSICAL_GPU_HANDLE = -101
    EXPECTED_DISPLAY_HANDLE = -102
    INVALID_COMBINATION = -103
    NOT_SUPPORTED = -104
    PORTID_NOT_FOUND = -105
    EXPECTED_UNATTACHED_DISPLAY_HANDLE = -106
    INVALID_PERF_LEVEL = -107
    DEVICE_BUSY = -108
    NV_PERSIST_FILE_NOT_FOUND = -109
    PERSIST_DATA_NOT_FOUND = -110
    EXPECTED_TV_DISPLAY = -111
    EXPECTED_TV_DISPLAY_ON_DCONNECTOR = -112
    NO_ACTIVE_SLI_TOPOLOGY = -113
    SLI_RENDERING_MODE_NOTALLOWED = -114
    EXPECTED_DIGITAL_FLAT_PANEL = -115
    ARGUMENT_EXCEED_MAX_SIZE = -116
    DEVICE_SWITCHING_NOT_ALLOWED = -117
    TESTING_CLOCKS_NOT_SUPPORTED = -118
    UNKNOWN_UNDERSCAN_CONFIG = -119
    TIMEOUT_RECONFIGURING_GPU_TOPO = -120
    DATA_NOT_FOUND = -121
    EXPECTED_ANALOG_DISPLAY = -122
    NO_VIDLINK = -123
    REQUIRES_REBOOT = -124
    INVALID_HYBRID_MODE = -125
    MIXED_TARGET_TYPES = -126
    SYSWOW64_NOT_SUPPORTED = -127
    IMPLICIT_SET_GPU_TOPOLOGY_CHANGE_NOT_ALLOWED = -128
    REQUEST_USER_TO_CLOSE_NON_MIGRATABLE_APPS = -129
    OUT_OF_MEMORY = -130
    WAS_STILL_DRAWING = -131
    FILE_NOT_FOUND = -132
    TOO_MANY_UNIQUE_STATE_OBJECTS = -133
    INVALID_CALL = -134
    D3D10_1_LIBRARY_NOT_FOUND = -135
    FUNCTION_NOT_FOUND = -136
    INVALID_USER_PRIVILEGE = -137
    EXPECTED_NON_PRIMARY_DISPLAY_HANDLE = -138
    EXPECTED_COMPUTE_GPU_HANDLE = -139
    STEREO_NOT_INITIALIZED = -140
    STEREO_REGISTRY_ACCESS_FAILED = -141
    STEREO_REGISTRY_PROFILE_TYPE_NOT_SUPPORTED = -142
    STEREO_REGISTRY_VALUE_NOT_SUPPORTED = -143
    STEREO_NOT_ENABLED = -144
    STEREO_NOT_TURNED_ON = -145
    STEREO_INVALID_DEVICE_INTERFACE = -146
    STEREO_PARAMETER_OUT_OF_RANGE = -147
    STEREO_FRUSTUM_ADJUST_MODE_NOT_SUPPORTED = -148
    TOPO_NOT_POSSIBLE = -149
    MODE_CHANGE_FAILED = -150
    D3D11_LIBRARY_NOT_FOUND = -151
    INVALID_ADDRESS = -152
    STRING_TOO_SMALL = -153
    MATCHING_DEVICE_NOT_FOUND = -154
    DRIVER_RUNNING = -155
    DRIVER_NOTRUNNING = -156
    ERROR_DRIVER_RELOAD_REQUIRED = -157
    SET_NOT_ALLOWED = -158
    ADVANCED_DISPLAY_TOPOLOGY_REQUIRED = -159
    SETTING_NOT_FOUND = -160
    SETTING_SIZE_TOO_LARGE = -161
    TOO_MANY_SETTINGS_IN_PROFILE = -162
    PROFILE_NOT_FOUND = -163
    PROFILE_NAME_IN_USE = -164
    PROFILE_NAME_EMPTY = -165
    EXECUTABLE_NOT_FOUND = -166
    EXECUTABLE_ALREADY_IN_USE = -167
    DATATYPE_MISMATCH = -168
    PROFILE_REMOVED = -169
    UNREGISTERED_RESOURCE = -170
    ID_OUT_OF_RANGE = -171
    DISPLAYCONFIG_VALIDATION_FAILED = -172
    DPMST_CHANGED = -173
    INSUFFICIENT_BUFFER = -174
    ACCESS_DENIED = -175
    MOSAIC_NOT_ACTIVE = -176
    SHARE_RESOURCE_RELOCATED = -177
    REQUEST_USER_TO_DISABLE_DWM = -178
    D3D_DEVICE_LOST = -179
    INVALID_CONFIGURATION = -180
    STEREO_HANDSHAKE_NOT_DONE = -181
    EXECUTABLE_PATH_IS_AMBIGUOUS = -182
    DEFAULT_STEREO_PROFILE_IS_NOT_DEFINED = -183
    DEFAULT_STEREO_PROFILE_DOES_NOT_EXIST = -184
    CLUSTER_ALREADY_EXISTS = -185
    DPMST_DISPLAY_ID_EXPECTED = -186
    INVALID_DISPLAY_ID = -187
    STREAM_IS_OUT_OF_SYNC = -188
    INCOMPATIBLE_AUDIO_DRIVER = -189
    VALUE_ALREADY_SET = -190
    TIMEOUT = -191
    GPU_WORKSTATION_FEATURE_INCOMPLETE = -192
    STEREO_INIT_ACTIVATION_NOT_DONE = -193
    SYNC_NOT_ACTIVE = -194
    SYNC_MASTER_NOT_FOUND = -195
    INVALID_SYNC_TOPOLOGY = -196
    ECID_SIGN_ALGO_UNSUPPORTED = -197
    ECID_KEY_VERIFICATION_FAILED = -198
    FIRMWARE_OUT_OF_DATE = -199
    FIRMWARE_REVISION_NOT_SUPPORTED = -200
    LICENSE_CALLER_AUTHENTICATION_FAILED = -201
    D3D_DEVICE_NOT_REGISTERED = -202
    RESOURCE_NOT_ACQUIRED = -203
    TIMING_NOT_SUPPORTED = -204
    HDCP_ENCRYPTION_FAILED = -205
    PCLK_LIMITATION_FAILED = -206
    NO_CONNECTOR_FOUND = -207
    HDCP_DISABLED = -208
    API_IN_USE = -209
    NVIDIA_DISPLAY_NOT_FOUND = -210
    PRIV_SEC_VIOLATION = -211
    INCORRECT_VENDOR = -212
    DISPLAY_IN_USE = -213
    UNSUPPORTED_CONFIG_NON_HDCP_HMD = -214
    MAX_DISPLAY_LIMIT_REACHED = -215
    INVALID_DIRECT_MODE_DISPLAY = -216
    GPU_IN_DEBUG_MODE = -217
    D3D_CONTEXT_NOT_FOUND = -218
    STEREO_VERSION_MISMATCH = -219
    GPU_NOT_POWERED = -220
    ERROR_DRIVER_RELOAD_IN_PROGRESS = -221
    WAIT_FOR_HW_RESOURCE = -222
    REQUIRE_FURTHER_HDCP_ACTION = -223
    DISPLAY_MUX_TRANSITION_FAILED = -224 