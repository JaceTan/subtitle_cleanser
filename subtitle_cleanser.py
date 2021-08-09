#!/usr/bin/env python3

import re

def getNextSubtitleBlock(subsFile):
    """
    Reads the few next lines of the subtitle file to identify, create
    and return a subtitleBlock Dictionary, or None if EOF is reached.

    A subtitle block should have the following pattern:
    Subtitle Block Number
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
    If EOF is reached, returns None instead.
    """
    subtitleBlock = {
        "timestamp": "",
        "content": [],
    }

    lineCounter = 0 # Limit 7 lines read to prevent reading until the end of file
    while lineCounter < 7:
        lineCounter += 1

        # Read the next line
        nextline = subsFile.readline()

        # End of File
        if nextline == "":
            return None

        # End of the subtitle block
        if re.match("\n", nextline):
            break

        # Remove Byte Order Mark (BOM) (if any) and surrounding whitespce
        nextline = re.sub("\uFEFF", "", nextline).strip()

        # Ignore the subtitle block number
        if lineCounter == 1 and nextline.isnumeric():
            continue

        # Identify and save the timestamp line
        if lineCounter == 2 and re.match("\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", nextline):
            subtitleBlock["timestamp"] = nextline
            continue

        # All subsequent lines are content
        subtitleBlock["content"].append(nextline)

    return subtitleBlock

def removeUnwantedContent(subtitleBlock):
    """
    Checks the contents of a subtitleBlock and removes all unwanted content.

    Parameters
    ----------
    subtitleBlock: Dictionary. The subtitleBlock containing the timestamp and content.

    Returns
    -------
    Dictionary. The subtitleBlock containing the timestamp and content,
                after all unwanted content has been removed.
    """
    content = []

    for line in subtitleBlock["content"]:
        # Remove all regualar () pairs if any
        line = re.sub("\(.*\)", "", line).strip()

        # Remove all square bracket [] pairs if any
        line = re.sub("\[.*\]", "", line).strip()

        # Remove all angular bracket <> pairs if any
        line = re.sub("<.*?>", "", line).strip()

        # Remove all musical notes ♪ ♪ pairs if any
        line = re.sub("♪", "", line).strip()

        # Remove speaker's name and corresponding colon if any
        line = re.sub("^\w+:", "", line).strip()

        # Only add if line still has any characters
        if line:
            content.append(line)

    subtitleBlock["content"] = content
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

    while True:
        # Read enough lines for the first block
        subtitleBlock = getNextSubtitleBlock(subsFile)

        # Exit the loop once None is returned, marking EOF
        if not subtitleBlock:
            break

        # Remove unwanted content
        subtitleBlock = removeUnwantedContent(subtitleBlock)
        print(subtitleBlock)

        # If there's no more content, skip to the next subtitleBlock
        if subtitleBlock["content"] == []:
            continue

        # Process remaning content to have even lines
        # Write remaining to a new file

main()
