#!/bin/bash

INPUT="your_input.jpg"
OUTPUT="true_cartoonified.png"

# Step 1: Edge detection
convert "$INPUT" -colorspace Gray -edge 1 -negate -normalize edge.png

# Step 2: Blur & blend the original
convert "$INPUT" -blur 0x1 blurred.png

# Step 3: Reduce colors (posterize)
convert blurred.png -posterize 6 simplified.png

# Step 4: Composite edges on top
convert simplified.png edge.png -compose Multiply -composite "$OUTPUT"

echo "✅ Done: $OUTPUT"
open "$OUTPUT"
