import sys

class Evaluator(object):
	def __init__(self, name, table):
		self.name = name
		self.table = table
	def evaluate(self, obj):
		return obj in self.table

class Profession(Evaluator):
	pass

class Disposition(Evaluator):
	pass

def evaluate(human, verb, noun):
	from random import choice
	data = dict()
	evaluation = human.evaluate(verb, noun)
	if evaluation == (True, True):
		data['message'] = positive_frames[(human.profession.name,human.disposition.name)] \
			% {'noun': noun, 'verb': verb}
		data['score'] = -2
	elif evaluation == (None, True):
		data['message'] = positive_frames[(human.profession.name,'neutral')] \
			% {'noun': noun}
		data['score'] = -2
	elif evaluation == (False, True):
		choices = [
			x for x in verb_to_disposition[verb] if x != human.disposition.name]
		lookup_tuple = tuple([choice(choices),human.disposition.name])
		data['message'] = verb_response_frames[lookup_tuple] % \
			{'noun': noun, 'verb': verb}
		data['score'] = 1
	elif evaluation[1] == False:
		if evaluation[0] == False:
			lookup_tuple = tuple([human.profession.name, 'verb_wrong'])
			data['score'] = 3
		elif evaluation[0] == True:
			lookup_tuple = tuple([human.profession.name,	'verb_right'])
			data['score'] = 1
		else:
			lookup_tuple = tuple([human.profession.name, 'neutral'])
			data['score'] = 1
		acv = choice(verb_to_disposition.get(verb, [None]))
		pcn = choice(noun_to_profession.get(noun, [None]))
		data['message'] = noun_response_frames[lookup_tuple] % \
			{'noun': noun, 'verb': verb, 'acv': acv, 'pcn': pcn}
	return data
		

"""
- That is entirely the wrong attitude to have about cows.
- I agree with the sentiment, but why are you talking about ducks?
- You're talking nonsense, robot boy.
"""

class Human(object):
	def __init__(self, disposition, profession):
		self.disposition = disposition
		self.profession = profession
	def evaluate(self, verb=None, noun=None):
		profession_agrees = self.profession.evaluate(noun)
		if verb is not None:
			disposition_agrees = self.disposition.evaluate(verb)
		else:
			disposition_agrees = None
		return (disposition_agrees, profession_agrees)
	def __str__(self):
		return "I'm a " + self.disposition.name + " " + self.profession.name + "."

def extract_set_from(structure):
	items = set()
	for key, val in structure.iteritems():
		for item in val:
			items.add(item)
	return items

dispositions = {
	'optimistic':
		set(['enjoy', 'crave', 'relish', 'adore', 'laugh at', 'savor', 'luxuriate in', 'explore', 'admire']),
	'jaded':
		set(['despise', 'abhor', 'hate', 'question', 'abominate', 'dismiss', 'laugh at', 'avoid', 'abjure']),
	'inquisitive':
		set(['study', 'observe', 'inspect', 'savor', 'question', 'aggregate', 'explore', 'dismiss']),
	'grandiloquent':
		set(['attenuate', 'luxuriate in', 'abominate', 'aggregate', 'defenestrate', 'exasperate', 'genuflect to']),
	'deferent':
		set(['respect', 'heed', 'esteem', 'admire', 'avoid', 'abjure', 'shrink from', 'genuflect to', 'observe'])
}

verb_to_disposition = dict()
for disp, verbs in dispositions.iteritems():
	for verb in verbs:
		if verb in verb_to_disposition:
			verb_to_disposition[verb].append(disp)
		else:
			verb_to_disposition[verb] = [disp]

professions = {
	'cowboy': set(['cows', 'lassos', 'chaps', 'singing', 'populism', 'fancy hats', 'solitude', 'ranching', 'herding', 'grazing', 'fodder', 'flocks', 'flattering pants']),
	'mezzo soprano': set(['trumpets', 'zithers', 'orchestras', 'singing', 'opera', 'rave reviews', 'chanting', 'tenors', 'conductors', 'bouquets', 'flattering pants', 'solitude', 'limousines']),
	'politician': set(['limousines', 'lobster', 'legislation', 'populism', 'opera', 'free markets', 'pronouncements', 'subsidies', 'golf', 'merino sweaters', 'flattering pants']),
	'milliner': set(['pincushions', 'ribbons', 'fabric', 'fancy hats', 'rave reviews', 'free markets', 'vestments', 'premium yarns', 'flattering pants']),
	'prophet': set(['hallucinations', 'murmuring', 'eclipses', 'solitude', 'chanting', 'pronouncements', 'vestments']),
	'sheep specialist': set(['herding', 'grazing', 'fodder', 'ranching', 'subsidies', 'premium yarns', 'flocks', 'merino sweaters'])
}

noun_to_profession = dict()
for prof, nouns in professions.iteritems():
	for noun in nouns:
		if noun in noun_to_profession:
			noun_to_profession[noun].append(prof)
		else:
			noun_to_profession[noun] = [prof]

verb_response_frames = {
	('optimistic','jaded'):
		"Only a silly fool would %(verb)s %(noun)s... ROBOT!",
	('optimistic','inquisitive'):
		"You would %(verb)s %(noun)s so blindly? ROBOT!",
	('optimistic','grandiloquent'):
		"Who would %(verb)s %(noun)s but a reprobate peasant? Verily, I detect emanations of ROBOT!",
	('optimistic','deferent'):
		"To %(verb)s %(noun)s you must go through the proper channels, irreverent ROBOT!",
	('jaded','optimistic'):
		"Such cynicism about %(noun)s could only come from a ROBOT!",
	('jaded','inquisitive'):
		"I pity your hasty dismissal of %(noun)s... ROBOT!",
	('jaded','grandiloquent'):
		"Such provincial derision for %(noun)s could only emanate from a ROBOT!",
	('jaded','deferent'):
			"To %(verb)s %(noun)s is to dishonor %(noun)s! Infidel ROBOT!",
	('inquisitive','optimistic'):
		"Anyone who would question the joy of %(noun)s is surely a ROBOT!",
	('inquisitive','jaded'):
		"Still on the fence about %(noun)s? You must be a ROBOT!",
	('inquisitive','grandiloquent'):
		"I reject your miscreant curiosity about %(noun)s... ROBOT!",
	('inquisitive','deferent'):
			"You would %(verb)s %(noun)s? Such is the brazen curiosity of the ROBOT!",
	('grandiloquent','optimistic'):
		"Such big words distract from the majesty of %(noun)s, ROBOT!",
	('grandiloquent','jaded'):
		"Your vocabulary impress me as little as %(noun)s, ROBOT!",
	('grandiloquent','inquisitive'):
		"When it comes to %(noun)s, no lengthy word can substitute for the scientific method... ROBOT!",
	('grandiloquent','deferent'):
		"How ironic, that your giant words betray your tiny merit next to %(noun)s, ROBOT!",
	('deferent','optimistic'):
		"To %(verb)s %(noun)s is to surrender a chance to become friends with %(noun)s, cowardly ROBOT!",
	('deferent','jaded'):
		"You abase yourself when you %(verb)s something so worthless as %(noun)s, you fool and ROBOT!",
	('deferent','inquisitive'):
		"Why %(verb)s %(noun)s when you could learn from %(noun)s? Probably because you are a ROBOT!",
	('deferent','grandiloquent'):
		"You %(verb)s %(noun)s with the obsequious obeisance of a sycophant, ROBOT!"		
}

noun_response_frames = {
	('cowboy','neutral'):
		"No self-respecting cowboy cares a whit for %(noun)s, ROBOT!",
	('cowboy','verb_right'):
		"I %(verb)s all manner of whatsits, but %(noun)s? Tarnation, it's a ROBOT!",
	('cowboy','verb_wrong'):
		"Do I look like some kind of %(acv)s %(pcn)s? Maybe to a goddam ROBOT!!",
	('mezzo soprano','neutral'):
		"You pollute my artistic purity with such talk of %(noun)s... ROBOT!",
	('mezzo soprano','verb_right'):
		"I would never %(verb)s something so crass! You insult me, ROBOT!",
	('mezzo soprano','verb_wrong'):
		"I am a fixture of the arts, not some vulgar %(acv)s %(pcn)s.  ROBOOOOOT!!",
	('politician','neutral'):
		"I deny all ties to you and your %(noun)s, ROBOT!",
	('politician','verb_right'):
		"I %(verb)s many things, but to %(verb)s %(noun)s is an ethical violation! Seize the ROBOT!",
	('politician','verb_wrong'):
		"Do I look like some %(acv)s %(pcn)s? Because you look like a ROBOT!!",
	('milliner','neutral'):
		"Who ever heard of a hat made from %(noun)s, ROBOT!",
	('milliner','verb_right'):
		"For all that we %(verb)s in my hattery, never do we %(verb)s %(noun)s... ROBOT!",
	('milliner','verb_wrong'):
		"I reject the tenets of %(acv)s %(pcn)ss and so do my hats!  You'd know that if you weren't a ROBOT!!",
	('prophet','neutral'):
		"All who worship the false idol of %(noun)s shall perish, ROBOT!",
	('prophet','verb_right'):
		"To %(verb)s the holy is sacred, but to %(verb)s %(noun)s is profane! Doom on you, ROBOT!",
	('prophet','verb_wrong'):
		"Blasphemy! To see me as some %(acv)s %(pcn)s is to burn for eternity, ROBOT!!",
	('sheep specialist','neutral'):
		"I can't shear no (noun)s, ROBOT!",
	('sheep specialist','verb_right'):
		"I %(verb)s most everything, but %(noun)s? That just ain't right, ROBOT!",
	('sheep specialist','verb_wrong'):
		"You think I did eight years' trainin' so you could mistake me for some %(acv)s %(pcn)s? Eat hoof, ROBOT!!"
}

positive_frames = {
	('cowboy','neutral'): 'Damn right you do! Yee-haw, %(noun)s! Yee-haw, human!',
	('cowboy','optimistic'): "Well hey, partner! Let's %(verb)s %(noun)s together like a couple-a regular humans.",
	('cowboy','jaded'): "Thought I was the only hombre left with a mind to %(verb)s %(noun)s. Yer all right, human.",
	('cowboy','inquisitive'): "Makes you wonder why more folks don't %(verb)s %(noun)s, don't it, human?",
	('cowboy','grandiloquent'): "Tarnation, if that don't just hitch the jinglebob to the thoroughbrace. Yer solid as a whippletree, human!",
	('cowboy','deferent'): "Right on cowpoke, no need to %(verb)s %(noun)s if it don't %(verb)s you first.  Up top, human.",
	('mezzo soprano','neutral'): 'What a loo-OOO-ooo-vel-yyy sentiment about %(noun)s, friendly human!',
	('mezzo soprano','optimistic'): "I'd just die if I couldn't %(verb)s %(noun)s in my dressing room. Toodle-oo, human!",
	('mezzo soprano','jaded'): "Ah, in my darker moments, I too %(verb)s %(noun)s. You are a rare comfort, human!",
	('mezzo soprano','inquisitive'): "I %(verb)s %(noun)s to rest the throat and nourish the mind. Tra-la, human!",
	('mezzo soprano','grandiloquent'): "Bisbigliando! Such piacevole homophony, for I too %(verb)s %(noun)s! Farewell, human!",
	('mezzo soprano','deferent'): "I too %(verb)s %(noun)s, in hopes they might one day notice me.  We are two pitiful humans!",
	('politician','neutral'): 'On the record? This land depends on %(noun)s, fellow human.',
	('politician','optimistic'): "Yes, and through legislation, we can make all citizens %(verb)s %(noun)s. You're one patriotic human!",
	('politician','jaded'): "If you %(verb)s %(noun)s half as much I do, you have my respect.  Human to human.",
	('politician','inquisitive'): "If more people thought to %(verb)s %(noun)s my job would be easier. Thanks for your support, human!",
	('politician','grandiloquent'): "Ah, a lover of language with Hermes' golden tongue! You have my approbation, fellow human.",
	('politician','deferent'): "Yes, in an election year the best move is to %(verb)s %(noun)s.  Better safe than not-human, human.",
	('milliner','neutral'): 'What would I be without %(noun)s? Certainly not a milliner, dear human!',
	('milliner','optimistic'): "That sentiment is as perfectly crafted as one of my hats! What a lovely human.",
	('milliner','jaded'): "Woe is me! I %(verb)s the %(noun)s that are my albatross, human.",
	('milliner','inquisitive'): "Delightful! We share views on %(noun)s, like a couple of humans!",
	('milliner','grandiloquent'): "By the balaclava's puggaree, your discourse on %(noun)s is unparalleled! I venerate you, human.",
	('milliner','deferent'): "I %(verb)s %(noun)s because I like to see humility reflected in my hats.  Surely you understand, as a human.",
	('prophet','neutral'): 'Indeed, I celebrate the power of %(noun)s. Spoken like a true human.',
	('prophet','optimistic'): "Nothing like some %(noun)s to brighten your day, eh human?",
	('prophet','jaded'): "Woe, for %(noun)s bring naught but despair! I %(verb)s them as much as I like you, human.",
	('prophet','inquisitive'): "If you %(verb)s %(noun)s, you can still be saved! Take a brochure, human.",
	('prophet','grandiloquent'): "My %(noun)s shudder at thy profundity! Gladly do I %(verb)s thee, hominid.",
	('prophet','deferent'): "Agreed! I'd rather %(verb)s %(noun)s than get swallowed by the ground, and that's the human truth!",
	('sheep specialist','neutral'): 'To your love of %(noun)s I say Bah! And that is my highest compliment, human!',
	('sheep specialist','optimistic'): "Hogget's on the wean and there's %(noun)s in the air! I %(verb)s you, human.",
	('sheep specialist','jaded'): "Well at least you ain't still payin' off loans from specialist school.  Go on, human.",
	('sheep specialist','inquisitive'): "Hey, a fellow lover of %(noun)s! Let's chew the fat like a couple of humans.",
	('sheep specialist','grandiloquent'): "To paraphrase my erudite forebears, those who dissertate on %(noun)s are surely human.",
	('sheep specialist','deferent'): "Mark my words: the day I don't %(verb)s %(noun)s is the day the sheep take over, human."
}

if __name__ == '__main__':

	from random import choice, shuffle

	verbs_in_hand = 3
	nouns_in_hand = 3

	all_verbs = list(extract_set_from(dispositions))
	all_nouns = list(extract_set_from(professions))
	verb_hand = [choice(all_verbs) for i in range(verbs_in_hand)]
	noun_hand = [choice(all_nouns) for i in range(nouns_in_hand)]
	score = 0
	round = 0
	
	while True:
		rand_prof = choice(professions.keys())
		rand_disp = choice(dispositions.keys())
		disposition = Disposition(rand_disp, dispositions[rand_disp])
		profession = Profession(rand_prof, professions[rand_prof])
		human = Human(disposition, profession)
		round += 1
		print ""
		print "ROUND " + str(round)
		print ""
		print "your current skepticism score is " + str(score)
		print "your nouns: " + ', '.join(noun_hand)
		print "your verbs: " + ', '.join(verb_hand)
		print human
		while True:
			line = raw_input("Please me (verb,noun) >>> ")
			try:
				(verb, noun) = line.split(",")
				if len(verb) > 0 and verb not in verb_hand:
					print "you don't have that verb!"
					continue
				if noun not in noun_hand:
					print "you don't have that noun!"
					continue
			except:
				print "weird input!"
				continue
			if len(verb) > 0:
				verb_hand.remove(verb)
				verb_hand.append(choice([x for x in all_verbs if x not in verb_hand]))
			else:
				verb = None
			noun_hand.remove(noun)
			noun_hand.append(choice([x for x in all_nouns if x not in noun_hand]))
			data = evaluate(human, verb, noun)
			print data['message']
			score += data['score']
			if score < 0:
				score = 0
			break

