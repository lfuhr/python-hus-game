import copy
from random import shuffle

def move(player, start, field):
	hand = field[player][start]
	field[player][start] = 0
	for dropfield in range(start+1, start+hand+1):
		field[player][dropfield%16] += 1
	stop = (start+hand)%16
	if field[player][stop] > 1:
		near, far = (7-stop)%16, (8+stop)%16
		if stop < 8 and field[1-player][near] > 0:
			field[player][stop] += field[1-player][near] + field[1-player][far]
			field[1-player][near], field[1-player][far] = 0,0
		move(player, stop, field)
	return field

def init_field():
	i = 0
	return [ [ (field >= 4) * 2 for field in range(16) ] for player in range(2) ]
	# Could choose other interesting start configurations
	# return [[2,1,5,1,3,3,2,1,5,4,1,2,0,4,3,0], [1,0,1,0,0,0,0,0,1,0,2,1,2,2,1,0]]

def print_field(field):
	print()
	print('\t'.join(str(hole) for hole in field[0][8:]))
	print('\t'.join(str(hole) for hole in field[0][7::-1]))
	print('-----------------------------')
	print('\t'.join(str(hole) for hole in field[1][:8]))
	print('\t'.join(str(hole) for hole in field[1][:7:-1]))
	print()

def value(player, field):
	return sum(field[player])

def best_move(player, field):
	possibilities = [i for i,v in enumerate(field[player]) if v > 1]
	shuffle(possibilities)
	moves = [ (move(player, start,copy.deepcopy(field)), start) for start in possibilities]
	return max(moves, key=lambda f: value(player,f[0]))

def game_over(field):
	return any([all([h < 2 for h in side]) for side in field])

def turn_possible(player, start, field):
	return field[player][start] >= 2

human = 1
computer = 1-human
field = init_field()
player = int(input("Wer soll beginnen (mensch/computer)? ").lower().startswith('m'))
print_field(field)
while (not game_over(field)):
	if player == computer:
		field, start = best_move(player, field)
		print("Computer wählt %i!"%(start+1))
	else:
		while True:
			start = int(input("Welches Feld (1-16)? "))-1
			if turn_possible(player, start, field): break
			else: print("Geht nicht")
		move(player, start, field)
	player = 1-player
	print_field(field)

print("Game over")
