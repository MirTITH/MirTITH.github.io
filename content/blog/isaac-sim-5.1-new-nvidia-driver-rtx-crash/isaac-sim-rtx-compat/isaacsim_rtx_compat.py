"""Prepare a Vulkan profile for Isaac Sim 5.1 on newer NVIDIA drivers.

Isaac Sim 5.1 can crash in ``librtx.scenedb.plugin.so`` when a newer NVIDIA
driver reports ``VkPhysicalDeviceMaintenance3Properties.maxMemoryAllocationSize``
as ``UINT64_MAX``.  The compatibility layer used here changes only that
reported property before Kit creates its Vulkan instance.

This module is intentionally imported by ``isaac-sim.sh`` before Kit starts.
It does not change the system driver and it is a no-op on older/safe drivers.
Set ``ISAAC_SIM_DISABLE_RTX_COMPAT=1`` to bypass it, or set
``ISAAC_SIM_VULKAN_PROFILES_LAYER`` to use another locally built profiles layer.
"""

from __future__ import annotations

from ctypes import (
    CDLL,
    POINTER,
    Structure,
    addressof,
    byref,
    c_char,
    c_char_p,
    c_int32,
    c_uint8,
    c_uint32,
    c_uint64,
    c_void_p,
)
import json
import os
from pathlib import Path
import sys
import tempfile


_NVIDIA_VENDOR_ID = 0x10DE
_LAST_KNOWN_GOOD_DRIVER = (590, 48, 1, 0)
_TWO_MIB = 2 * 1024 * 1024
_SAFE_ALLOCATION_CAP = 4 * 1024 * 1024 * 1024 - _TWO_MIB
_PROFILE_NAME = "VP_RTX_driver_compat_generated"
_PROFILE_LAYER_API_VERSION = "1.4.341"
_CACHE_ROOT = (
    Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    / "isaac-sim-vulkan-rtx-compat"
)
_BUNDLED_LAYER = (
    Path(__file__).resolve().parent
    / "tools"
    / "vulkan_profiles"
    / "libVkLayer_khronos_profiles.so"
)


class _VkApplicationInfo(Structure):
    _fields_ = [
        ("sType", c_uint32),
        ("pNext", c_void_p),
        ("pApplicationName", c_char_p),
        ("applicationVersion", c_uint32),
        ("pEngineName", c_char_p),
        ("engineVersion", c_uint32),
        ("apiVersion", c_uint32),
    ]


class _VkInstanceCreateInfo(Structure):
    _fields_ = [
        ("sType", c_uint32),
        ("pNext", c_void_p),
        ("flags", c_uint32),
        ("pApplicationInfo", c_void_p),
        ("enabledLayerCount", c_uint32),
        ("ppEnabledLayerNames", c_void_p),
        ("enabledExtensionCount", c_uint32),
        ("ppEnabledExtensionNames", c_void_p),
    ]


class _VkPhysicalDeviceProperties(Structure):
    _fields_ = [
        ("apiVersion", c_uint32),
        ("driverVersion", c_uint32),
        ("vendorID", c_uint32),
        ("deviceID", c_uint32),
        ("deviceType", c_uint32),
        ("deviceName", c_char * 256),
        ("pipelineCacheUUID", c_uint8 * 16),
        # Keep the structure larger than the Vulkan 1.x properties payload.
        ("_rest", c_uint8 * 2048),
    ]


class _VkPhysicalDeviceProperties2(Structure):
    _fields_ = [
        ("sType", c_uint32),
        ("pNext", c_void_p),
        ("properties", _VkPhysicalDeviceProperties),
    ]


class _VkPhysicalDeviceMaintenance3Properties(Structure):
    _fields_ = [
        ("sType", c_uint32),
        ("pNext", c_void_p),
        ("maxPerSetDescriptors", c_uint32),
        ("maxMemoryAllocationSize", c_uint64),
    ]


class _VkMemoryType(Structure):
    _fields_ = [("propertyFlags", c_uint32), ("heapIndex", c_uint32)]


class _VkMemoryHeap(Structure):
    _fields_ = [("size", c_uint64), ("flags", c_uint32)]


class _VkPhysicalDeviceMemoryProperties(Structure):
    _fields_ = [
        ("memoryTypeCount", c_uint32),
        ("memoryTypes", _VkMemoryType * 32),
        ("memoryHeapCount", c_uint32),
        ("memoryHeaps", _VkMemoryHeap * 16),
    ]


def _verbose() -> bool:
    return os.environ.get("ISAAC_SIM_RTX_COMPAT_VERBOSE", "") == "1"


def _log(message: str, *, always: bool = False) -> None:
    if always or _verbose():
        print(f"[isaacsim_rtx_compat] {message}", file=sys.stderr, flush=True)


def _prepend_env(name: str, value: Path) -> None:
    text = str(value)
    old = os.environ.get(name, "")
    parts = old.split(os.pathsep) if old else []
    if text not in parts:
        os.environ[name] = os.pathsep.join([text, *parts])


def _nvidia_driver_version(raw: int) -> tuple[int, int, int, int]:
    # NVIDIA's Vulkan driver version encoding is major/minor/patch/build.
    return (raw >> 22, (raw >> 14) & 0xFF, (raw >> 6) & 0xFF, raw & 0x3F)


def _find_unsafe_allocation_cap() -> int | None:
    override = os.environ.get("RTX_VULKAN_COMPAT_MAX_MEMORY_ALLOCATION_SIZE")
    if override:
        return int(override, 0)

    try:
        vk = CDLL("libvulkan.so.1")
        create_instance = vk.vkCreateInstance
        enumerate_devices = vk.vkEnumeratePhysicalDevices
        get_properties = vk.vkGetPhysicalDeviceProperties2
        get_memory = vk.vkGetPhysicalDeviceMemoryProperties
        destroy_instance = vk.vkDestroyInstance
    except (AttributeError, OSError) as exc:
        _log(f"Vulkan probe unavailable: {exc}")
        return None

    create_instance.argtypes = [
        POINTER(_VkInstanceCreateInfo),
        c_void_p,
        POINTER(c_void_p),
    ]
    create_instance.restype = c_int32
    enumerate_devices.argtypes = [
        c_void_p,
        POINTER(c_uint32),
        POINTER(c_void_p),
    ]
    enumerate_devices.restype = c_int32
    get_properties.argtypes = [c_void_p, POINTER(_VkPhysicalDeviceProperties2)]
    get_memory.argtypes = [c_void_p, POINTER(_VkPhysicalDeviceMemoryProperties)]
    destroy_instance.argtypes = [c_void_p, c_void_p]

    application = _VkApplicationInfo(
        sType=0,
        pApplicationName=b"isaacsim_rtx_compat",
        apiVersion=(1 << 22) | (1 << 12),
    )
    create_info = _VkInstanceCreateInfo(
        sType=1,
        pApplicationInfo=c_void_p(addressof(application)),
    )
    instance = c_void_p()
    if create_instance(byref(create_info), None, byref(instance)) != 0:
        _log("Vulkan instance probe failed")
        return None

    caps: list[int] = []
    try:
        count = c_uint32()
        if enumerate_devices(instance, byref(count), None) != 0 or count.value == 0:
            return None
        devices = (c_void_p * count.value)()
        if enumerate_devices(instance, byref(count), devices) != 0:
            return None

        for device in devices:
            maintenance3 = _VkPhysicalDeviceMaintenance3Properties(
                sType=1000168000
            )
            properties = _VkPhysicalDeviceProperties2(
                sType=1000059001,
                pNext=c_void_p(addressof(maintenance3)),
            )
            get_properties(device, byref(properties))
            device_properties = properties.properties
            driver = _nvidia_driver_version(int(device_properties.driverVersion))
            if device_properties.vendorID != _NVIDIA_VENDOR_ID:
                continue
            if driver <= _LAST_KNOWN_GOOD_DRIVER:
                continue
            if int(maintenance3.maxMemoryAllocationSize) <= _SAFE_ALLOCATION_CAP:
                continue

            memory = _VkPhysicalDeviceMemoryProperties()
            get_memory(device, byref(memory))
            local_heap_size = max(
                (
                    int(memory.memoryHeaps[index].size)
                    for index in range(memory.memoryHeapCount)
                    if memory.memoryHeaps[index].flags & 1
                ),
                default=0,
            )
            caps.append(
                min(_SAFE_ALLOCATION_CAP, local_heap_size - _TWO_MIB)
                if local_heap_size > _TWO_MIB
                else _SAFE_ALLOCATION_CAP
            )
            name = bytes(device_properties.deviceName).split(b"\0", 1)[0]
            _log(
                f"detected {name.decode(errors='replace')} driver {driver}, "
                f"maxMemoryAllocationSize=0x{int(maintenance3.maxMemoryAllocationSize):x}"
            )
    finally:
        destroy_instance(instance, None)

    return (min(caps) // 256) * 256 if caps else None


def _layer_path() -> Path | None:
    configured = os.environ.get("ISAAC_SIM_VULKAN_PROFILES_LAYER")
    candidates = [Path(configured)] if configured else []
    candidates.extend(
        [
            _BUNDLED_LAYER,
            _CACHE_ROOT / "libVkLayer_khronos_profiles.so",
        ]
    )
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
    return None


def _atomic_write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        json.dump(value, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.chmod(0o600)
    os.replace(temporary, path)
    path.chmod(0o600)


def _configure_profile(layer: Path, allocation_cap: int) -> None:
    _CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    _CACHE_ROOT.chmod(0o700)
    profile_dir = _CACHE_ROOT / "profiles"
    data_root = _CACHE_ROOT / "xdg-data"
    manifest_dir = data_root / "vulkan" / "implicit_layer.d"

    _atomic_write_json(
        profile_dir / f"{_PROFILE_NAME}.json",
        {
            "$schema": "https://schema.khronos.org/vulkan/profiles-0.8-latest.json#",
            "capabilities": {
                "RTX_DRIVER_COMPAT": {
                    "properties": {
                        "VkPhysicalDeviceMaintenance3Properties": {
                            "maxMemoryAllocationSize": allocation_cap
                        }
                    }
                }
            },
            "profiles": {
                _PROFILE_NAME: {
                    "version": 1,
                    "api-version": "1.1.0",
                    "label": "Isaac Sim 5.1 RTX Driver Compatibility",
                    "description": "Limits Vulkan allocation reporting for Isaac Sim 5.1.",
                    "capabilities": ["RTX_DRIVER_COMPAT"],
                }
            },
        },
    )
    _atomic_write_json(
        manifest_dir / "VkLayer_KHRONOS_profiles.json",
        {
            "file_format_version": "1.2.1",
            "layer": {
                "name": "VK_LAYER_KHRONOS_profiles",
                "type": "GLOBAL",
                "library_path": str(layer),
                "api_version": _PROFILE_LAYER_API_VERSION,
                "implementation_version": "1.3.0",
                "description": "Khronos Profiles layer",
                "enable_environment": {"RTX_VULKAN_COMPAT_ENABLE_LAYER": "1"},
                "disable_environment": {"RTX_VULKAN_COMPAT_DISABLE_LAYER": ""},
            },
        },
    )

    os.environ["RTX_VULKAN_COMPAT_ENABLE_LAYER"] = "1"
    os.environ["RTX_VULKAN_COMPAT_ACTIVE"] = "1"
    os.environ["RTX_VULKAN_COMPAT_MAX_MEMORY_ALLOCATION_SIZE_ACTIVE"] = str(
        allocation_cap
    )
    os.environ["VK_KHRONOS_PROFILES_PROFILE_NAME"] = _PROFILE_NAME
    os.environ["VK_KHRONOS_PROFILES_SIMULATE_CAPABILITIES"] = (
        "SIMULATE_PROPERTIES_BIT"
    )
    os.environ["VK_KHRONOS_PROFILES_DEBUG_REPORTS"] = "DEBUG_REPORT_ERROR_BIT"
    _prepend_env("VK_KHRONOS_PROFILES_PROFILE_DIRS", profile_dir)
    _prepend_env("VK_ADD_IMPLICIT_LAYER_PATH", manifest_dir)
    _prepend_env("XDG_DATA_DIRS", data_root)


def enable() -> bool:
    """Enable the compatibility profile if the local Vulkan device needs it."""
    if os.environ.get("ISAAC_SIM_DISABLE_RTX_COMPAT") == "1":
        return False
    if os.environ.get("RTX_VULKAN_COMPAT_DISABLE") == "1":
        return False
    if os.environ.get("RTX_VULKAN_COMPAT_ACTIVE") == "1":
        return True

    allocation_cap = _find_unsafe_allocation_cap()
    if allocation_cap is None or allocation_cap <= 0:
        return False

    layer = _layer_path()
    if layer is None:
        _log(
            "unsafe NVIDIA Vulkan allocation limit detected, but no compatible "
            "Vulkan Profiles layer was found; continuing without workaround",
            always=True,
        )
        return False

    _configure_profile(layer, allocation_cap)
    _log(
        "enabled Vulkan compatibility profile: "
        f"maxMemoryAllocationSize={allocation_cap}, layer={layer}",
        always=True,
    )
    return True


try:
    enabled = enable()
except Exception as exc:  # Keep the normal launcher usable if probing fails.
    enabled = False
    _log(f"compatibility setup skipped: {exc}", always=True)

