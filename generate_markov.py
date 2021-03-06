#!/usr/bin/env python3

import argparse
import sys
import json
import pickle
import random

# Defines how many preceding words we use to predict the next one
# With really large datasets you might wanna increase this to create syntatically better results
history_len = 1 

def main():
    args = parse_arguments()
    
    if args.input:
        generate_data(args.input, args.FILE)
    else:
        print(generate_comment(args.FILE))


def generate_comment(input):
    try:
        infile = open(input, 'rb')
        data = pickle.load(infile)

        probs = data['probs']
        begin = data['begin']

        comment = []

        prev = random.choice(begin)

        for i in range(len(prev) - 1):
            comment.append(prev[i])

        while prev[-1] != 0:
            comment.append(prev[-1])
            new = random.choice(probs[prev])
            prev = prev[1:] + (new,)

        return ' '.join(comment)
    except Exception as err:
        sys.stderr.write(str(err)+'\n')
        sys.exit(1)


# Generates the Markov chain data based on JSON formatted chat history from the input file
def generate_data(input, output):
    try:
        infile = open(input, 'r')
        outfile = open(output, 'wb+')

        # This will hold the current -> next state probabilities
        probs = {}

        # Entry points for comments
        begin = []

        for line in infile.readlines():
            data = json.loads(line)

            # We exclude media messages, system messages, bot commands and forwarded msgs
            if data['event'] != 'message' or 'media' in data or data['text'][0] == '/' or 'fwd_from' in data:
                continue

            words = data['text'].split()

            # Construct the probabilities
            for t in gen_trigram(words, history_len):
                key = t[:-1]
                value = t[-1]
                if key in probs:
                    probs[key].append(value)
                else:
                    probs[key] = [value]

            if len(words) > history_len:
                begin.append(tuple(words[:history_len]))

        infile.close()
        dump = {'probs' : probs, 'begin' : begin}
        pickle.dump(dump, outfile)
        outfile.close()

    except Exception as err:
        sys.stderr.write(str(err)+'\n')
        sys.exit(1)


# Generate n-grams for following word predictions.
def gen_trigram(words, history):
    if len(words) < history+1:
        return
    for i in range(len(words) - history + 1):
        if i == len(words) - history:
            # 0 marks the end of a comment
            t = tuple(words[i:i+history])+(0,)
        else:
            t = tuple(words[i:i+history+1])
        yield t


# Basic argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='This flag causes the program to generate FILE based on INPUT before generating a comment.')
    parser.add_argument('FILE', help='File to be used as input for comment generation and for Markov chain data, if -g is used.')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()

