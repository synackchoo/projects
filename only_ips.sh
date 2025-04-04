#!/bin/bash

# Check for input file
if [[ -z "$1" ]]; then
  echo "Usage: $0 <input_file>"
  exit 1
fi

# Output file (optional customization)
output_file="cleaned_ips.txt"

# Grep out only valid IPv4 addresses
grep -oE '\b((25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\b' "$1" > "$output_file"

echo "Clean IPs saved to $output_file"
