#!/usr/bin/env python3

import constants
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
    Dictionary. The subtitleBlock containing the timestamp, content
    and preceding-hyphens. If EOF is reached, returns None instead.
    """
    subtitleBlock = {
        "timestamp": "",
        "content": [],
        "preceding-hyphens": False,
    }

    lineCounter = 0 # Limit 7 lines read to prevent reading until the end of file
    while lineCounter < 7:
        lineCounter += 1

        # Read the next line
        nextline = subsFile.readline()

        # End of File
        if lineCounter == 1 and nextline == "":
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

def verifyContent(subtitleBlock):
    """
    Checks the contents of a subtitleBlock and determines if it's
    actual content or just junk like Title or Advertising. Uses the
    JUNK_PATTERNS constant in the constants.py file as a database.

    Parameters
    ----------
    subtitleBlock: Dictionary. The subtitleBlock containing
    the timestamp, content and preceding-hyphens.

    Returns
    -------
    Boolean. True if the content is actual content. False
    if the content is random junk like Title or Advertising.
    """
    for pattern in constants.JUNK_PATTERNS:
        iterator = re.compile(pattern)
        matches = list(filter(iterator.search, subtitleBlock["content"]))
        if len(matches) > 0:
            return False

    return True

def removeUnwantedContent(subtitleBlock):
    """
    Checks the contents of a subtitleBlock and removes all unwanted content.

    Parameters
    ----------
    subtitleBlock: Dictionary. The subtitleBlock containing
    the timestamp, content and preceding-hyphens.

    Returns
    -------
    Dictionary. The subtitleBlock containing the timestamp, content
    and preceding-hyphens after all unwanted content has been removed.
    """
    content = []

    for line in subtitleBlock["content"]:
        # Remove all round backet () pairs if any
        line = re.sub("\(.*\)", "", line).strip()

        # Remove all square bracket [] pairs if any
        line = re.sub("\[.*\]", "", line).strip()

        # Remove all angular bracket <> pairs if any
        line = re.sub("<.*?>", "", line).strip()

        # Remove all musical notes ♪ ♪ pairs and single musical notes if any
        line = re.sub("♪.*♪", "", line).strip()
        line = re.sub("♪", "", line).strip()

        # Remove speaker's name and corresponding colon if any
        line = re.sub("(^|[.,!?\s])[A-Za-z]+?:", r"\1", line).strip()

        # Record and remove preceding hyphens if any
        if re.match("^-", line):
            subtitleBlock["preceding-hyphens"] = True
            line = re.sub("^-", "", line).strip()

        # Only add if line still has any characters
        if line:
            content.append(line)

    subtitleBlock["content"] = content
    return subtitleBlock

def cleanupContent(subtitleBlock):
    """
    Checks the contents of a subtitleBlock and cleans up minor
    errors and inconsistencies including but not limited to:
    - capitalizing pronouns (Sherlock, not sherlock)
    - removing spaces between contractions (don't, not don 't)
    - double hyphens (--)
    - removing spaces before periods
    - adding spaces after periods

    Parameters
    ----------
    subtitleBlock: Dictionary. The subtitleBlock containing
    the timestamp, content and preceding-hyphens.

    Returns
    -------
    Dictionary. The subtitleBlock containing the timestamp, content,
    and preceding-hyphens after all cleanup has been performed.
    """
    content = []

    for line in subtitleBlock["content"]:
        # Fix double symbols and spaces except periods
        line = re.sub(r"([^\w\.])\1", r"\1", line)

        # Fix exception for double periods vs ellipses
        line = re.sub("[^\.]\.\.[^\.]", ".", line)

        # Recognize acronyms if any
        acronym = re.search("(^|\W)((\w\.){2,})", line)
        if acronym:
            # Replace the acronym with a placeholder first
            line = line.replace(acronym.group(2), "__acronym__")

        # Add a space after sentence punctuation
        line = re.sub("([\.,?!])([A-Za-z])", r"\1 \2", line)
        if acronym:
            # Replace the placeholder with the uppercased acronym
            line = line.replace("__acronym__", acronym.group(2).upper())

        # Add a space between a small letter followed by a capital letter (indicates joined words)
        line = re.sub("([a-z])([A-Z])", r"\1 \2", line)

        # Remove a space before sentence punctuation
        line = re.sub("(\w)\s([\.,?!])", r"\1\2", line)

        # Fix common contractions with spaces
        line = re.sub("(\w)\s'(s|ll|t|re|d|m|ve)", r"\1'\2", line)

        content.append(line)

    subtitleBlock["content"] = content
    return subtitleBlock

def balanceContent(subtitleBlock):
    """
    Balances the content lines by combining them into single lines if able, or
    by making them as even as possible. Adds back preceding hyphens if needed.

    Parameters
    ----------
    subtitleBlock: Dictionary. The subtitleBlock containing
    the timestamp, content and preceding-hyphens.

    Returns
    -------
    Dictionary. The subtitleBlock containing the timestamp, content,
    and preceding-hyphens after lines have been balanced.
    """
    if subtitleBlock["preceding-hyphens"]:
        subtitleBlock["content"] = ["- " + line for line in subtitleBlock["content"]]
        return subtitleBlock

    # Combine all lines (regardless 2 or 3 lines) to make a single line
    singleLine = " ".join(subtitleBlock["content"])
    lineLength = len(singleLine)

    # If all chars can fit into a single line, work is done.
    if lineLength <= 40:
        subtitleBlock["content"] = [singleLine]
        return subtitleBlock

    # Split the line into 2 roughly even lines
    midIndex = int(lineLength / 2)
    line1 = singleLine[:midIndex]
    line2 = singleLine[midIndex:]

    # If line1 ends with a space or line2 begins with one, then line are already even
    if line1.endswith(" ") or line2.startswith(" "):
        subtitleBlock["content"] = [line1.strip(), line2.strip()]
        return subtitleBlock

    # The smaller part needs to join the bigger part
    wordPart1 = line1.split(" ")[-1]
    wordPart2 = line2.split(" ")[0]

    # Shift wordPart2 to the end of line1 if it's smaller than wordPart1
    if len(wordPart1) > len(wordPart2):
        line1 = line1 + wordPart2
        line2 = line2[len(wordPart2):].strip()
    else: # Otherwise, move wordPart1 to the beginning of line2
        line1 = line1[:-len(wordPart1)].strip()
        line2 = wordPart1 + line2

    subtitleBlock["content"] = [line1, line2]
    return subtitleBlock

def main():
    # Make sure the subtitle file is in the same level as this file
    filename = "07 Sober Companions.srt"
    outputFilename = filename.replace(".", "-cleansed.")

    # Check that subsFile can be opened and read
    try:
        subsFile = open(filename, "r")
    except FileNotFoundError:
        print("Unable to find or open the file: {}.".format(filename))
        return

    subtitleBlockIndex = 0
    while True:
        # Read enough lines for the first block
        subtitleBlock = getNextSubtitleBlock(subsFile)

        # Exit the loop once None is returned, marking EOF
        if not subtitleBlock:
            break

        # Skip if content is non-content like Title, Advertising, etc
        if not verifyContent(subtitleBlock):
            continue

        # Remove unwanted content
        subtitleBlock = removeUnwantedContent(subtitleBlock)

        # If there's no more content, skip to the next subtitleBlock
        if subtitleBlock["content"] == []:
            continue

        # Cleanup minor mistakes in content
        subtitleBlock = cleanupContent(subtitleBlock)

        # Process remaning content to have even lines
        subtitleBlock = balanceContent(subtitleBlock)

        # Write remaining content to a separate file
        subtitleBlockIndex += 1
        with open(outputFilename, "a+") as outputFile:
            if subtitleBlockIndex > 1:
                outputFile.write("\n\n")
            outputFile.write(str(subtitleBlockIndex) + "\n")
            outputFile.write(subtitleBlock["timestamp"] + "\n")
            outputFile.write("\n".join(subtitleBlock["content"]))

main()
