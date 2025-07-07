#!/bin/bash

TARGET_DIR="$HOME/Development/Projects/EMBODY/tts_engines/yourtts_full"
SOURCE_SUBDIRS=("TTS" "models" "trainer" "yourtts.py" "vits.py")
FILE_LIST="/tmp/file_list.txt"

# Step 1: Build file list (filter out blank or invalid entries)
> "$FILE_LIST"
for name in "${SOURCE_SUBDIRS[@]}"; do
  path="$TARGET_DIR/$name"
  if [ -d "$path" ]; then
    find "$path" -name "*.py" >> "$FILE_LIST"
  elif [ -f "$path" ]; then
    echo "$path" >> "$FILE_LIST"
  fi
done

# Step 2: Clean up empty lines
sed -i '' '/^\s*$/d' "$FILE_LIST"

# Step 3: Auto-patch files with syntax errors
while IFS= read -r file; do
  echo "[*] Compiling $file"
  python3 -m py_compile "$file" 2> /tmp/errlog

  if [ $? -ne 0 ]; then
    echo "[!] Compilation failed in $file"
    cat /tmp/errlog
    echo "---"

    LINE_NUM=$(grep -oE "line [0-9]+" /tmp/errlog | grep -oE "[0-9]+")
    if [[ "$LINE_NUM" =~ ^[0-9]+$ ]]; then
      echo "[*] Patching line $LINE_NUM in $file"
      sed -i '' "${LINE_NUM}s/$/  # FIX: syntax issue/" "$file" || \
        echo "[!] Failed to patch $file:$LINE_NUM"
    else
      echo "[!] Couldn't extract valid line number"
    fi
  else
    echo "[✓] Compiled clean: $file"
  fi
done < "$FILE_LIST"
