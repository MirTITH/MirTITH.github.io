Isaac Sim 5.1 RTX driver compatibility package
============================================

Target: Ubuntu 22.04, Linux x86_64, Isaac Sim 5.1.0.
Compatibility module startup validation: RTX 4070 Ti SUPER, driver 610.57.04.

Usage after extracting the complete archive:
  bash isaac-sim-rtx-compat/launch.sh "/path/to/isaacsim-5.1.0"
  bash isaac-sim-rtx-compat/launch.sh "/path/to/isaacsim-5.1.0" --no-window

Replace /path/to/isaacsim-5.1.0 in every command with your installation
directory containing isaac-sim.sh and kit/. Run these commands from the
parent of the extracted isaac-sim-rtx-compat directory. Keep path quotes.

The launcher uses Isaac Sim's bundled Python to configure the compatibility
layer, then calls the existing isaac-sim.sh with all remaining arguments.
It does not replace installation files or install a system-wide Vulkan layer.
Keep the extracted package intact and use launch.sh for subsequent launches.

Diagnostics:
  ISAAC_SIM_RTX_COMPAT_VERBOSE=1 bash isaac-sim-rtx-compat/launch.sh "/path/to/isaacsim-5.1.0"
Disable for one launch:
  ISAAC_SIM_DISABLE_RTX_COMPAT=1 bash isaac-sim-rtx-compat/launch.sh "/path/to/isaacsim-5.1.0"

By default, generated profiles and manifests are written below:
  ~/.cache/isaac-sim-vulkan-rtx-compat
The tilde denotes the running user's home directory.
XDG_CACHE_HOME overrides the cache base directory.

The layer overrides maxMemoryAllocationSize only when the Python module's
driver/property checks match. It does not cap total GPU memory to 4 GiB.
This workaround does not address unrelated ROS, port, or rendering errors.
No compiler, additional Python packages, or source editing is required on
the target platform. Other platforms may require a different library build.

Library provenance:
  https://github.com/KhronosGroup/Vulkan-Profiles/tree/v1.4.341
  Built with the Ubuntu 22.04 toolchain.
Related issue:
  https://github.com/isaac-sim/IsaacSim/issues/568

See THIRD_PARTY_NOTICES.txt and licenses/ for third-party license texts.

Validation scope: the compatibility module and library reached app ready in
GUI and headless tests. The distributed launch.sh wrapper was separately
checked for environment/argument forwarding, paths with spaces, and the
disable switch; a full Isaac Sim launch through this wrapper was not rerun.
