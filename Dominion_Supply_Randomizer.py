# DOMINION SUPPLY RANDOMIZER SECOND TAKE
"""
This program randomly pulls cards to create the supply in the game Dominion. It lets the user specify the minimum and maximum
number of cards to be drawn from each expansion set used in the game, and also lets the user draw fewer than (or more than) 10 cards
with which to stock the supply pile. The output of the simulation is independent of the order of expansion sets from which cards are drawn.
"""

# MODULES
from random import random
from random import sample
from sys import exit

import random
import sys

# Expansion Sets with lists of card names
Base = ['Adventurer', 'Bureaucrat', 'Cellar', 'Chancellor', 'Chapel', 'Council_Room', 'Feast', 'Gardens', 'Festival', 'Laboratory', 'Library', 'Market', 'Militia', 'Mine', 'Moat', 'Moneylender', 'Remodel', 'Smithy', 'Spy', 'Thief', 'Throne_Room', 'Village', 'Witch', 'Woodcutter', 'Workshop']
Hinterlands = ['Border_Village', 'Cache', 'Cartographer', 'Crossroads', 'Develop', 'Duchess', 'Embassy', 'Farmland', 'Fools_Gold', 'Haggler', 'Highway', 'Ill_Gotten_Gains', 'Inn', 'Jack_of_All_Trades', 'Mandarin', 'Margrave', 'Noble_Brigand', 'Nomad_Camp', 'Oasis', 'Oracle', 'Scheme', 'Silk_Road', 'Spice_Merchant', 'Stables', 'Trader', 'Tunnel']
Intrigue = ['Baron', 'Bridge', 'Conspirator', 'Coppersmith', 'Courtyard', 'Duke', 'Great_Hall', 'Harem', 'Ironworks', 'Masquerade', 'Mining_Village', 'Minion', 'Nobles', 'Pawn', 'Saboteur', 'Scout', 'Secret_Chamber', 'Shanty_Town', 'Steward', 'Swindler', 'Torturer', 'Trading_Post', 'Tribute', 'Upgrade', 'Wishing_Well']
Seaside = ['Ambassador', 'Bazaar', 'Caravan', 'Cutpurse', 'Embargo', 'Explorer', 'Fishing_Village', 'Ghost_Ship', 'Haven', 'Island', 'Lighthouse', 'Lookout', 'Merchant_Ship', 'Native_Village', 'Navigator', 'Outpost', 'Pearl_Diver', 'Pirate_Ship', 'Salvager', 'Sea_Hag', 'Smuggler', 'Tactician', 'Treasure_Map', 'Treasury', 'Warehouse', 'Wharf',]
Prosperity = ['Bank', 'Bishop', 'City', 'Contraband', 'Counting_House', 'Expand', 'Forge', 'Goons', 'Grand_Market', 'Hoard', 'Kings_Court', 'Loan', 'Mint', 'Monument', 'Mountebank', 'Peddler', 'Quarry', 'Rabble', 'Royal_Seal', 'Talisman', 'Trade_Route', 'Vault', 'Venture', 'Watchtower', 'Workers_Village']
Dark_Ages = ['Altar', 'Armory', 'Band_of_Misfits', 'Bandit_Camp', 'Beggar', 'Catacombs', 'Counterfeit', 'Cultist', 'Death_Cart', 'Feodum', 'Forager', 'Fortress', 'Graverobber', 'Hermit', 'Hunting_Grounds', 'Ironmonger', 'Junk_Dealer', 'Maurader', 'Market_Square', 'Mystic', 'Pillage', 'Poor_House', 'Procession', 'Rats', 'Rebuild', 'Rogue', 'Sage', 'Scavenger', 'Squire', 'Storeroom', 'Urchin', 'Vagrant', 'Wandering_Minstrel']
Cornucopia = ['Fairgrounds', 'farming_Village', 'Fortune_Teller', 'Hamlet', 'Harvest', 'Horn_of_Plenty', 'Horse_Traders', 'Hunting_Party', 'Jester', 'Menagerie', 'Remake', 'Tournament', 'Young_Witch']

# The following list specifies cards which are banned from the supply pile.
Banned_Cards = ['Chapel', 'Pirate_Ship', 'Jack_of_All_Trades', 'Library', 'Scheme']
	# Remove banned cards from the card lists
Base = [card for card in Base if card not in Banned_Cards]
Hinterlands = [card for card in Hinterlands if card not in Banned_Cards]
Intrigue = [card for card in Intrigue if card not in Banned_Cards]
Seaside = [card for card in Seaside if card not in Banned_Cards]
Prosperity = [card for card in Prosperity if card not in Banned_Cards]
Dark_Ages = [card for card in Dark_Ages if card not in Banned_Cards]


# PARAMETERS 
	# Inelegant
# These lists contains the minimum and maximum number of cards to be included from each set
undrawn_cards = 10

Par_Base = [Base, 3,3]
Par_Hinterlands = [Hinterlands, 0,3]
Par_Seaside = [Seaside, 0,3]
Par_Intrigue = [Intrigue, 0,0]
Par_Prosperity = [Prosperity, 0,0]
Par_Dark_Ages = [Dark_Ages, 4,4]

Parameters = [Par_Base, Par_Hinterlands, Par_Seaside, Par_Intrigue, Par_Prosperity, Par_Dark_Ages]
Parameters = [i for i in Parameters if i[2] > 0]		# Cut out expansion packs with a max card count of zero


# Check to make sure the sum of the min card requirements does not exceed 10
if sum( [i[1] for i in Parameters] ) > undrawn_cards: 
	sys.exit("Too many min card requirements")

if sum( [i[2] for i in Parameters] ) < undrawn_cards:
	sys.exit("max card limits are too small")


# FUNCTIONS
def fact(x):
	"factorial function"
	return x > 1 and x * fact(x - 1) or 1
	
def pascals_table(row, col):
	"Returns a value from Pascal's Triangle as depicted in table form, where n = row number and r = column number"
	# Note that row corresponds to number of sets, collumn corresponds to number of cards
	return fact(row+col-1)/(fact(row-1)*fact(col))

def cards_from_a_set(min_draw, max_draw, number_sets):
	"Returns the number of cards to be drawn from a particular Dominion expansion pack"
	# outcome_vector will represent a (truncated) sample row from Pascals table, where 0 entry counts the number of scenarios
	# in which the min number of cards could be drawn from the given set
	outcome_vector = [0]*(max_draw-min_draw+1)
	
	# Populate outcome vector
	for i in range(max_draw - min_draw + 1):
		outcome_vector[i] = pascals_table(number_sets - 1, i+min_draw)
#	print "Outcome vector is", outcome_vector
	normalized_outcome = [(x/(1.0*sum(outcome_vector))) for x in outcome_vector]
#	print "Normalized outcome vector is", normalized_outcome	
	
	# Now pul a random number and see where on the outcome vector it falls
	random_draw = random.random()	# Gives a random number between 0 and 1
	draw_number = 0
	for i in range(max_draw - min_draw + 1):
		if random_draw <= normalized_outcome[i]:
			draw_number = max_draw - i
			return draw_number
		random_draw -= normalized_outcome[i]
	return draw_number


###################################################################################

# Main

number_sets = len(Parameters)
print "number_sets is", number_sets

final_supply = []

# This loop goes through each set that we wish to draw from, balances the min and max numbers to account for min/max requirements
# from other sets and for already drawn cards, and then pulls cards for the supply.
for i in range(len(Parameters)):
	current_set = Parameters[i]
	
	min_draw = max( current_set[1], undrawn_cards - sum([ j[2] for j in Parameters[i+1:]]))
	max_draw = min( current_set[2], undrawn_cards - sum([ j[1] for j in Parameters[i+1:]]))
	if number_sets > 1:
		draw_number = cards_from_a_set(min_draw, max_draw, number_sets)
	else:
		draw_number = undrawn_cards
	number_sets -= 1
	
#	print "Draw number is", draw_number
	cards = random.sample( current_set[0], draw_number )
	final_supply += cards
	print "Cards are", cards
	undrawn_cards -= draw_number




