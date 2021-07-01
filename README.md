## What is this  
Python bindings for Nvidia API. High level wrapper for listing gpus, low level structs copied straight from C implementation.

## Usage  
 - Import main class with `from nvapi import NvidiaAPI`
 - Initialize `api = NvidiaAPI()`, this also calls .Initialize() in the nvapi.dll
 - List GPUs with `api.list_gpus()`, you will get list of PhysicalGPU() objects
 - Each PhysicalGPU has wrappers: `general`, `performance`, `cooler`, `driver`, `thermal`  
 - Each wrapper wraps one ore more native calls to nvapi.dll, most of them then return native ctypes struct.
  
Eventually I want to implement more high level functions, with python classes and handling weird nvapi quirks (f.eg. 3 different functions for getting fan speed depending on GPU generation).  
More low level, native implementation as it is right now will be left untouched.  
There are still many undocumented, not implemented or not tested functions, I will try to test all of them as time goes on.   
  
## Examples  
`example.py` displays basic info about installed physical GPUs  
`overclock.py` tries to overclock GPU0 core by 50Hz and checks the result  