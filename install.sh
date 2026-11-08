#!/usr/bin/env bash
# Install / remove the Meridian HUD for Team Fortress 2 on Linux.
#
#   ./install.sh                 copy the HUD into tf/custom/meridian
#   ./install.sh --link          symlink instead of copy (edit in place, then `hud_reloadscheme`)
#   ./install.sh --autoexec      also add `exec meridian` to tf/cfg/autoexec.cfg
#   ./install.sh --uninstall     remove the HUD (and the autoexec line if we added it)
#   ./install.sh --tf-dir DIR    use this tf/ directory instead of auto-detecting
#
# TF2_DIR=/path/to/tf can be set instead of --tf-dir.
set -euo pipefail

HUD_NAME=meridian
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$HUD_NAME"
MODE=copy
AUTOEXEC=0
UNINSTALL=0
TF_DIR="${TF2_DIR:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --link) MODE=link ;;
    --autoexec) AUTOEXEC=1 ;;
    --uninstall) UNINSTALL=1 ;;
    --tf-dir) shift; TF_DIR="${1:?--tf-dir needs a path}" ;;
    -h|--help) sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

die() { echo "error: $*" >&2; exit 1; }

find_tf_dir() {
  local roots=(
    "$HOME/.steam/steam"
    "$HOME/.local/share/Steam"
    "$HOME/.var/app/com.valvesoftware.Steam/.local/share/Steam"
    "$HOME/snap/steam/common/.local/share/Steam"
  )
  local libs=() root vdf line
  for root in "${roots[@]}"; do
    [[ -d "$root/steamapps" ]] || continue
    libs+=("$root")
    vdf="$root/steamapps/libraryfolders.vdf"
    if [[ -f "$vdf" ]]; then
      while IFS= read -r line; do libs+=("$line"); done < <(
        sed -n 's/^[[:space:]]*"path"[[:space:]]*"\(.*\)"/\1/p' "$vdf"
      )
    fi
  done
  local lib
  for lib in "${libs[@]}"; do
    if [[ -d "$lib/steamapps/common/Team Fortress 2/tf" ]]; then
      echo "$lib/steamapps/common/Team Fortress 2/tf"
      return 0
    fi
  done
  return 1
}

if [[ -z "$TF_DIR" ]]; then
  TF_DIR="$(find_tf_dir)" || die "could not find Team Fortress 2. Pass --tf-dir '<steam library>/steamapps/common/Team Fortress 2/tf'."
fi
[[ -d "$TF_DIR" ]] || die "not a directory: $TF_DIR"
[[ -f "$TF_DIR/gameinfo.txt" ]] || die "$TF_DIR does not look like TF2's tf/ directory (no gameinfo.txt)"

DEST="$TF_DIR/custom/$HUD_NAME"
AUTOEXEC_FILE="$TF_DIR/cfg/autoexec.cfg"
MARK="exec meridian // added by Meridian install.sh"

if [[ $UNINSTALL -eq 1 ]]; then
  rm -rf "$DEST"
  if [[ -f "$AUTOEXEC_FILE" ]] && grep -qF "$MARK" "$AUTOEXEC_FILE"; then
    grep -vF "$MARK" "$AUTOEXEC_FILE" > "$AUTOEXEC_FILE.tmp" && mv "$AUTOEXEC_FILE.tmp" "$AUTOEXEC_FILE"
  fi
  echo "removed $DEST"
  exit 0
fi

[[ -d "$SRC" ]] || die "missing $SRC"

# The Linux client looks files up in lowercase, so a mixed-case name is silently ignored.
bad="$(cd "$SRC" && find . -type f | grep '[A-Z]' || true)"
[[ -z "$bad" ]] || die "file names must be lowercase:"$'\n'"$bad"

mkdir -p "$TF_DIR/custom"
rm -rf "$DEST"
if [[ $MODE == link ]]; then
  ln -s "$SRC" "$DEST"
else
  cp -r "$SRC" "$DEST"
fi
echo "installed ($MODE): $DEST"

if [[ $AUTOEXEC -eq 1 ]]; then
  mkdir -p "$TF_DIR/cfg"
  touch "$AUTOEXEC_FILE"
  if ! grep -qF "$MARK" "$AUTOEXEC_FILE"; then
    # make sure we start on a fresh line
    [[ -s "$AUTOEXEC_FILE" && -n "$(tail -c1 "$AUTOEXEC_FILE")" ]] && echo >> "$AUTOEXEC_FILE"
    echo "$MARK" >> "$AUTOEXEC_FILE"
  fi
  echo "autoexec: $AUTOEXEC_FILE"
else
  echo "tip: run 'exec meridian' in the TF2 console (or re-run with --autoexec) to apply the recommended cvars."
fi

cat <<'EOM'

Restart TF2 (a HUD change needs a restart; later edits reload with hud_reloadscheme).
Recommended Steam launch options for a 16:10 display, e.g. 1920x1200:
  -novid -w 1920 -h 1200 -fullscreen
EOM
