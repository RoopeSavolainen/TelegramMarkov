# TelegramMarkov
This program generates comments with a Markov chain. Telegram chat history is used as input.

## Requirements
First off, you need some Telegram chat history in JSON format. You can dump chat history from a group you're a member in with https://github.com/tvdstaaij/telegram-history-dump or your tool of choice.
Assuming you already have the history file, the only other requirement is python3.

## Installation
Simply clone the repo. Before the first-time run, get some Telegram history logs as explained in the Requirements section.

## Usage
### First-time use
For the first run, you'll need to generate the Markov chain probabilities. This is done by running the following command:
`python3 generate-markov.py -i INPUT FILE`
Where INPUT is the file containing your JSON formatted Telegram history and FILE is the file where you want to save the Markov chain data.

### General
Once you've generated the Markov chain data, you can start generating comments. This is done by running:
`python3 generate-markov.py FILE`
Where FILE contains your Markov chain data.

