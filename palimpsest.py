# coding: latin-1

# First get the lm-sensors data from the sensors.data file
import re
import random

#token_pat = re.compile("\s*(?:(\d+)|(.))")
#token_pat = re.compile("(\d+)|(.)")
token_pat = re.compile("(\+[0-9][0-9])|(.)")

def tokenize(text):
    for number, operator in token_pat.findall(text):
        if number:
            print("number")
        else:
            print("trash")

f = open('sensors.data', 'r')

l = []

for line in f:
	text = line.split(':')
        #print text,
    	for number, operator in token_pat.findall(line):
            if number:
	      t = int(number.split('+')[1])
              if t < 38:
		l.append("ice aged")
	      elif t >= 38 and t < 39:
                l.append("frozen")
	      elif t >= 39 and t < 40:
                l.append("frozen yoghurt")
	      elif t >= 40 and t < 42:
                l.append("drafty")
	      elif t >= 42 and t < 44:
                l.append("gushy")
	      elif t >= 44 and t < 46:
		l.append("cold")
  	      elif t >= 46 and t < 48:
                l.append("mild")
	      elif t >= 48 and t < 50:
		l.append("heated")
              elif t >= 50 and t < 52:
                l.append("hot")
  	      elif t >= 52 and t < 55:
                l.append("too hot")
  	      elif t >= 55 and t < 57:
                l.append("Hotter than July")
	      elif t >= 57:
 		l.append("inferno")
# uncomment the following line to see the printed list of lm-sensors results
#print l

hc_grammar = ''

#iterate through list and generate grammar possibilities
for s in l:
	hc_grammar+=' '
	hc_grammar+=s
	hc_grammar+=' |'

hc_grammar = hc_grammar.rpartition(' |')[0]
# uncomment the following line to see the formatted list of lm-sensors results
#print hc_grammar

"""Module to generate random sentences from a grammar.  The grammar
consists of entries that can be written as S = 'NP VP | S and S',
which gets translated to {'S': [['NP', 'VP'], ['S', 'and', 'S']]}, and
means that one of the top-level lists will be chosen at random, and
then each element of the second-level list will be rewritten; if it is
not in the grammar it rewrites as itself.  The functions rewrite and
rewrite_tree take as input a list of words and an accumulator (empty
list) to which the results are appended.  The function generate and
generate_tree are convenient interfaces to rewrite and rewrite_tree
that accept a string (which defaults to 'S') as input."""


def make_grammar(**grammar):
  "Create a dictionary mapping symbols to alternatives."
  for k in grammar.keys():
    grammar[k] = [alt.strip().split() for alt in grammar[k].split('|')]
  return grammar
  
grammar = make_grammar(
  S = 'NP VP NO N',
  NP = 'Art P N',
  VP = 'V NP',
  NO = 'Dev Art',
  Art = 'the | a',
  Dev = 'in | on',
  N = 'man | ball | woman | table | computer | hole | phone | cat | monkey | mouse | sax | gramophone | software | core | board | bird | pencil | girl | hydrogen | oxygen | gas | magnet | rapper | improviser | laser | phaser | oscillator | nemesis | planet | ship',
  V = 'hit | took | wrote | liked | flew | crashed | ran | caught | mingled | hoped | talked | left | bought | failed | drew | hyperemphasized | sulfatized | reliberated | predissolved | reharmonized',
  P = hc_grammar
  )

def rewrite(words, into):
  "Replace each word in the list with a random entry in grammar (recursively)."
  for word in words:
    if word in grammar: rewrite(random.choice(grammar[word]), into)
    else: into.append(word)
  return into

def rewrite_tree(words, into):
  "Replace the list of words into a random tree, chosen from grammar."
  for word in words:
    if word in grammar:
      into.append({word: rewrite_tree(random.choice(grammar[word]), [])})
    else:
      into.append(word)
  return into

def generate(str='S'):
  "Replace each word in str by a random entry in grammar (recursively)."
  return ' '.join(rewrite(str.split(), []))

def generate_tree(cat='S'):
  "Use grammar to rewrite the category cat"
  return rewrite_tree([cat], [])

#=================================================================
print(generate('S'))
