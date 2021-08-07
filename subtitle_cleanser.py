#!/usr/bin/env python3

import re

def getNextSubtitleBlock(subsFile):
    """
    Reads the few next lines of the subtitle file to
    identify, create and return a subtitleBlock dictionary.

    A subtitle block should have the following pattern:
    Section Index Number
    Timestamp --> Timestamp
    Content Line1
    Content Line2 or Newline
    Content Line3 or Newline

    Example:
    1
    00:00:00,045 --> 00:00:01,361
    WATSON:
    <i>Previously on</i> Elementary...

    Parameters
    ----------
    subsFile: File. The file object to read subtitle lines from.

    Returns
    -------
    Dictionary. The subtitleBlock containing the timestamp and content.
    """
    subtitleBlock = {
        "timestamp": "",
        "content": [],
    }

    lineCounter = 0 # Limit 7 lines read to prevent reading until the end of file
    while lineCounter < 7:
        lineCounter += 1

        # Read the next line
        nextline = subsFile.readline().strip()
        print(nextline)

        # End of the subtitle block
        if nextline == "":
            break

        # If nextline contains a Byte Order Mark (BOM), remove it
        if re.search("\uFEFF", nextline):
            nextline = re.sub("\uFEFF", "", nextline)

        # Ignore the Section Index Number
        if lineCounter == 1 and nextline.isnumeric():
            continue


    return subtitleBlock

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
    subtitleBlock = getNextSubtitleBlock(subsFile)

    # Determine which lines are content lines (could be 1, 2 or even 3 lines)
    # Run the content lines through multiple stages of cleansing
    # Determine if there's any content lines left
    # If yes, write to a new file
    # If no, skip the whole block

main()
