JO_COMPILE_WITH_VIDEO_MODULE = 0
JO_COMPILE_WITH_BACKUP_MODULE = 0
JO_COMPILE_WITH_TGA_MODULE = 1
JO_COMPILE_WITH_AUDIO_MODULE = 0
JO_COMPILE_WITH_3D_MODULE = 0
JO_COMPILE_WITH_PSEUDO_MODE7_MODULE = 0
JO_COMPILE_WITH_EFFECTS_MODULE = 0
JO_COMPILE_WITH_PRINTF_MODULE = 0
JO_DEBUG = 1

SRCS=main.c libc_stubs.c

# Jo Engine instalado no Raspberry Pi
JO_ENGINE_SRC_DIR=/home/pi/joengine/jo_engine
COMPILER_DIR=/home/pi/joengine/Compiler

include $(COMPILER_DIR)/COMMON/jo_engine_makefile

# The upstream CueMaker binary shipped with Jo Engine is x86, and fails on ARM64.
# Override it with a tiny shell script that generates a valid .cue for MODE1/2352.
CUE_MAKER=./make_cue.sh
