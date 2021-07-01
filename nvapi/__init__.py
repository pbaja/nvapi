from . import nvapi, enums, structs

# Classes
NvidiaAPI = nvapi.NvidiaAPI
NvidiaError = nvapi.NvidiaError
ApiError = nvapi.ApiError

# Structs
NvidiaPerfStatesInfo = structs.performance.NvidiaPerfStatesInfo

# Enums
NvidiaClockDomain = enums.NvidiaClockDomain
NvidiaClockType = enums.NvidiaClockType
NvidiaStatus = enums.NvidiaStatus
