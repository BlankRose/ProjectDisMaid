import discord
import random as rng

class Hello():

	short = "Giving a warm welcome to the maid is always appreciable"
	description = """Giving out a warm welcome to the hard working maid is always appreciated and means a lot to them!~ xoxo~\n
					ARGUMENTS:
					`None` - *Doesn't contains any arguments*"""
	syntax = "hello"
	icon = ":wave:"

	async def run(self, entries: dict, msg: discord.message.Message):
		caseA = ["Hai sweetheart~",
				"Hello there~",
				"Hoi!"]
		strA = caseA[rng.randrange(0, len(caseA))]
		caseB = ["(^owo^)s *Meow.*",
				"How are you?",
				"Would you like some cookies?",
				"Have you seen my cat? I can't find it anywhere."]
		strB = caseB[rng.randrange(0, len(caseB))]
		await msg.reply(strA + "\n" + strB)