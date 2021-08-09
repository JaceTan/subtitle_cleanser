# Introduction
I like watching movies and TV shows with subtitles. Mostly it's because I'm more of a visual person so I like to read the words, rather than just listening. Sometimes it's also because the actors speak with accents, or mumble, or use lingo I'm not familiar with, so it's helpful to confirm what they're saying with the subtitles.

However, I get annoyed when the subtitles aren't what I would deem "perfect". They have typos, or they're all in CAPS, or the words are wrong because the subtitler themselves have misheard. I Googled around a little, but I couldn't find any tool that would let me adjust the subs the way I wanted, so I decided to make it myself. Besides the practicality of this project, I also wanted to create something simple but tangible to show off my coding skills.

Eventually, I hope to turn this into a useful tool with customizable options, to allow other people to use it outside my definition of "perfect". For example, I personally don't like the a name with a colon that indicates who's talking, because I can hear the actor myself. But there are plenty of people who do like that, so that would be an option to turn on or off.

# Usage
This is an executable Python script written in Python 3.7.
You can drag the script to the same level as the subtitle script you want to cleanse, update the `filename` in the `main` func, and execute it from the command line. It will output a new file with the word "-cleansed" attached to the original file name in the same level.
