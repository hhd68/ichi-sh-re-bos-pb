#!/bin/bash
# Test script for main.sh

echo "Testing main.sh..."

# Run the script and capture output
output=$(./main.sh)

# Expected output
expected="ichi+sh+re+bos+pb"

# Compare output
if [ "$output" = "$expected" ]; then
    echo "✓ Test passed: Output matches expected value"
    exit 0
else
    echo "✗ Test failed: Expected '$expected', got '$output'"
    exit 1
fi
