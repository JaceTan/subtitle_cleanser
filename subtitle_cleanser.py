#!/usr/bin/env python3

def main():
    # Open the subtitle file
    # Make sure the subtitle file is in the same level as this file
    filename = "24 Hurt Me, Hurt You.srt"

    # Check that subsFile can be read
    try:
        subsFile = open(filename, "r")
    except FileNotFoundError:
        print("Unable to find or open the file: {}.".format(filename))
        return

    # Read enough lines for the first block
    # Determine which lines are content lines (could be 1, 2 or even 3 lines)
    # Run the content lines through multiple stages of cleansing
    # Determine if there's any content lines left
    # If yes, write to a new file
    # If no, skip the whole block

main()
