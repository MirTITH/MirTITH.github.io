#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || ${1:-} == --help || ${1:-} == -h ]]; then
    printf 'Usage: bash %s /path/to/isaacsim-5.1.0 [Isaac Sim arguments...]\n' "$0"
    if [[ $# -lt 1 ]]; then exit 2; fi
    exit 0
fi

PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ISAAC_ROOT="$(cd -- "$1" && pwd)"
shift
ISAAC_PYTHON="$ISAAC_ROOT/kit/python/bin/python3"
ISAAC_LAUNCHER="$ISAAC_ROOT/isaac-sim.sh"
PROFILE_LAYER="$PACKAGE_DIR/tools/vulkan_profiles/libVkLayer_khronos_profiles.so"

if [[ $(uname -m) != x86_64 ]]; then
    printf 'This package requires Linux x86_64.\n' >&2
    exit 1
fi
if [[ ! -x "$ISAAC_PYTHON" || ! -f "$ISAAC_LAUNCHER" ]]; then
    printf 'Expected kit/python/bin/python3 and isaac-sim.sh in: %s\n' "$ISAAC_ROOT" >&2
    exit 1
fi
if [[ ! -f "$PACKAGE_DIR/isaacsim_rtx_compat.py" || ! -x "$PROFILE_LAYER" ]]; then
    printf 'Incomplete package or missing library permissions. Extract the complete tar.gz again.\n' >&2
    exit 1
fi

export PYTHONPATH="$PACKAGE_DIR${PYTHONPATH:+:$PYTHONPATH}"
export ISAAC_SIM_VULKAN_PROFILES_LAYER="${ISAAC_SIM_VULKAN_PROFILES_LAYER:-$PROFILE_LAYER}"
cd -- "$ISAAC_ROOT"
exec "$ISAAC_PYTHON" -c \
    'import os, sys; import isaacsim_rtx_compat; os.execv("/bin/bash", ["bash", *sys.argv[1:]])' \
    "$ISAAC_LAUNCHER" "$@"
