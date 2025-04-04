import subprocess
import time
import os
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Resolve URLs to IPs using dig.")
parser.add_argument("--input", "-i", required=True, help="Input file with URLs (one per line)")
parser.add_argument("--output", "-o", required=True, help="Output file to save resolved IPs")
args = parser.parse_args()

url_file = args.input
output_file = args.output

# Check if input file exists
if not os.path.isfile(url_file):
    print(f"❌ File not found: {url_file}")
    exit(1)

# Clear output file at the start
with open(output_file, "w") as f:
    pass

# Read and process each URL
with open(url_file, "r") as f:
    for line in f:
        url = line.strip()

        # Skip empty lines
        if not url:
            continue

        print(f"\n🔍 Querying: {url}")

        try:
            result = subprocess.run(
                ["dig", "+short", url],
                capture_output=True,
                text=True,
                check=False
            )

            output = result.stdout.strip()

            if output:
                print(output)

                # Write each non-empty IP (line) to output file
                with open(output_file, "a") as out_f:
                    for ip in output.splitlines():
                        if ip.strip():
                            out_f.write(ip.strip() + "\n")
            else:
                print("❌ No response from server")

        except Exception as e:
            print(f"❌ Error querying {url}: {e}")

        time.sleep(1)

# Deduplicate IPs in the file
with open(output_file, "r") as f:
    unique_ips = sorted(set(line.strip() for line in f if line.strip()))

with open(output_file, "w") as f:
    for ip in unique_ips:
        f.write(ip + "\n")

print(f"\n✅ Finished. Unique IPs saved to: {output_file}")
