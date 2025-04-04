#!/bin/bash

#Usage: ./clean_urls.sh input_file.txt output_file.txt

INPUT="$1"
OUTPUT="$2"

if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
echo "Usage: $0 input_file.txt output_file.txt"
exit 1
fi

#Clean each line:

#1. Remove leading non-alphanumeric characters (like bullets or whitespace)

#2. Remove 'http://' or 'https://' (case-insensitive)

#3. Remove trailing slash (optional)

sed -E 's/^[^a-zA-Z0-9]*//; s|https?://||I; s|/$||' "$INPUT" > "$OUTPUT"

echo "[+] Cleaned URLs written to: $OUTPUT"
