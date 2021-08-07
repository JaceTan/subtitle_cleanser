#!/usr/bin/env python3

# Open the subtitle file
# Read lines enough for the first block
# Determine which lines are content lines (could be 1, 2 or even 3 lines)
# Run the content lines through multiple stages of cleansing
# Determine if there's any content lines left
# If yes, write to a new file
# If no, skip the whole block
