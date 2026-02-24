#!/bin/sh
set -eu

# On this setup we are using Debian's genisoimage, which outputs a standard
# ISO9660 MODE1/2048 data track (2048 bytes/sector).
# A minimal cue sheet is enough for most emulators and for burning to CD-R.
cat > game.cue <<'CUE'
FILE "game.iso" BINARY
  TRACK 01 MODE1/2048
    INDEX 01 00:00:00
CUE
