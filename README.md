# Introduction
I like watching movies and TV shows with subtitles. Mostly it's because I'm more of a visual person so I like to read the words, rather than just listening. Sometimes it's also because the actors speak with accents, or mumble, or use lingo I'm not familiar with, so it's helpful to confirm what they're saying with the subtitles.

However, I get annoyed when the subtitles aren't what I would deem "perfect". They have typos, or they're all in CAPS, or the words are wrong because the subtitler themselves have misheard. I Googled around a little, but I couldn't find any tool that would let me adjust the subs the way I wanted, so I decided to make it myself. Besides the practicality of this project, I also wanted to create something simple but tangible to show off my coding skills.

Eventually, I hope to turn this into a useful tool with customizable options, to allow other people to use it outside my definition of "perfect". For example, I personally don't like the a name with a colon that indicates who's talking, because I can hear the actor myself. But there are plenty of people who do like that, so that would be an option to turn on or off.

# Usage
This is an executable Python script written in Python 3.7.
You can drag the script to the same level as the subtitle script you want to cleanse, update the `filename` in the `main` func, and execute it from the command line. It will output a new file with the word "-cleansed" attached to the original file name in the same level.

# Features
This script will:
- Re-number subtitle block numberings
- Preserve timestamps
- Remove brackets and their contents `()`, `[]`, `<>`
- Remove musical notes and their contents (usually lyrics for background music)
- Remove names of speakers and their corresponding colon `:` e.g. "Jace: Hello World!" --> "Hello World!"
- Remove spaces before sentence punctuation e.g. "This is a sentence part , this is the other part ." --> "This is a sentence part, this is the other part."
- Add spaces after sentence punctuation e.g. "This is a sentence part,this is the other part.This is a new sentence." --> "This is a sentence part, this is the other part. This is a new sentence."
- Replace double symbols and double spaces with single symbols (ignores ellipses `...`) e.g. "Wait... You  can't do--" --> "Wait... You can't do-"
- Removes unnecessary spaces between common contractions e.g. "can 't" --> "can't"
- Removes subtitle blocks that are non-content like Advertising or Titles based on a custom list of JUNK_PATTERNS that can be expanded upon over time

### Future Features
- Appropriate Capitalizing
- Typo detection and fixes
- Line balancing

# Changelog
<b>10 Aug 2021</b>
- Added `verifyContent` func with detailed docstring and logic to detect junk content
- Added `constants.py` file with a list of JUNK_PATTERNS and used it in `verifyContent` func
- Added logic to skip over non-content `subtitleBlock`s based on results from `verifyContent`

<b>09 Aug 2021</b>
- Added `removeUnwantedContent` func with detailed docstring and logic to remove all unwanted content like bracketed content, speaker names with colons, and preceding hyphens
- Updated `getNextSubtitleBlock` to detect end of file and return `None`
- Added a `while` loop in the `main` func to loop through all `subtitleBlock`s until the end of the file
- Added a `preceding-hypens` key to the `subtitleBlock` to flag it for processing later
- Added `cleanupContent` func with detailed docstring and logic to cleanup simple mistakes like double symbols, double spaces, removing spaces before and adding spaces after sentence punctuations, and removing spaces between common contractions.
- Added logic to write the cleansed subtitle block to a separate file
- Added `COPYING` file with GNU 3.0 licence
- Added `README.md` file with Introduction, Usage, Features and Future Features, and Changelog

<b>07 Aug 2021</b>
- Added `subtitle_cleanser.py` with shebang line and made it executable
- Added `main` func and pseudo code
- Added validation logic to ensure the subtitle file exists and can be opened
- Added `getNextSubtitleBlock` func with detailed docstring and logic to remove Byte Order Marks, ignore the Subtitle Block Number and extract the timestamp and content lines
