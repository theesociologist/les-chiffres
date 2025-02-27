"""
Survivor: Python Edition

This is a text-based role-playing game based on the reality series, "Survivor".
Players compete in immunity challenges, explore the Island, interact with tribe
mates and attempt to avoid elimination at a daily Tribal Council. If
you outwit, outplay, and outlast the other castaways, you are the Sole Survivor and
the winner of one million dollars!
"""

import random

# Section 1 - Game Setup

"""
This determines player characters, attributes, and flaws. Each Survivor contestant
has unique skills, weaknesses, and statistics that affects performance. Each 
character is based on a real Survivor player. 
"""

CHARACTERS = {
    "Evvie": {
        "attributes": ["Extrovert", "Disarming", "Smart"],
        "flaws": ["Cerebral", "Naive", "Unathletic"],
        "currentHealth": 90,
        "maxHealth": 100,
        "inventory": [],
        "socialStatus": 0
    },
    "Teeny": {
        "attributes": ["Disarming", "Sneaky", "Sweet"],
        "flaws": ["Moody", "Insecure", "Follower"],
        "currentHealth": 80,
        "maxHealth": 100,
        "inventory": [],
        "socialStatus": 0
    },
    "Parvati": {
        "attributes": ["Confident", "Athletic", "Resourceful"],
        "flaws": ["Delusionally Confident", "Self-Indulgent", "Jealous"],
        "currentHealth": 100,
        "maxHealth": 100,
        "inventory": [],
        "socialStatus": 0
    }
}

ATTRIBUTE_SCORES = {
    "Extrovert": 5, "Disarming": 10, "Smart": 7, "Confident": 8,
    "Athletic": 6, "Resourceful": 7, "Sneaky": 4, "Sweet": 5, "Charismatic": 9,
    "Patient": 6, "Resilient": 9
}

FLAW_PENALTIES = {
    "Cerebral": -4, "Naive": -2, "Unathletic": -5, "Moody": -6,
    "Insecure": -7, "Follower": -3, "Delusionally Confident": -6,
    "Self-Indulgent": -5, "Jealous": -8, "Blunt": -10
}


# Section 2 - Attributes and Flaws

def initializeStats(character):
    """
    Generates social status and health based on attributes and flaws.

    Parameters:
        character (dict): Character's attributes, flaws, and stats.

    Returns:
        None
    """
    baseSocialStatus = 50
    baseHealth = character["currentHealth"]

    for attr in character.get("attributes", []):
        baseSocialStatus += ATTRIBUTE_SCORES.get(attr, 0)
    for flaw in character.get("flaws", []):
        baseSocialStatus += FLAW_PENALTIES.get(flaw, 0)

    for attr in character["attributes"]:
        baseHealth += ATTRIBUTE_SCORES.get(attr, 0) // 2
    for flaw in character["flaws"]:
        baseHealth += FLAW_PENALTIES.get(flaw, 0) // 2

    character["socialStatus"] = max(0, baseSocialStatus)
    character["currentHealth"] = min(baseHealth, character["maxHealth"])


# Section 3 - Tribe Mates
def generateTribe():
    """
    Generates random tribe members with attributes, flaws, and health.

    Returns:
        list: A randomized list of tribe member names, attributes, and flaws.
    """
    tribe = []
    names = [
        "Brice", "Sandra", "Coach", "Boston Rob", "Tasha", "Spencer",
        "Dom", "Fabio", "Kass", "Ozzy", "Shan", "J.T.", "Yve", "Q", "Donathan",
        "Tiffany", "Katurah", "Shambo", "Wendell", "Rachel", "Hunter", "Venus"
    ]
    for name in random.sample(names, 5):
        attributes = random.sample(list(ATTRIBUTE_SCORES.keys()), 3)
        flaws = random.sample(list(FLAW_PENALTIES.keys()), 3)
        currentHealth = 70 + 10 * ("Resilient" in attributes) - 5 * (
                "Reckless" in flaws)
        member = {
            "name": name,
            "attributes": attributes,
            "flaws": flaws,
            "currentHealth": currentHealth,
            "maxHealth": 100,
            "socialStatus": 50
        }
        initializeStats(member)
        tribe.append(member)
    return tribe


# Section 4 - Immunity Challenges (Combat)

import time
import random

# List of valid attributes and flaws for the trait challenge.
VALID_TRAITS = [
    "Extrovert", "Disarming", "Smart", "Confident", "Athletic",
    "Resourceful", "Sneaky", "Sweet", "Charismatic", "Strategic",
    "Cerebral", "Naive", "Unathletic", "Moody", "Insecure",
    "Follower", "Delusionally Confident", "Self-Indulgent", "Jealous", "Blunt"
]


def traitChallenge(player, tribeMates):
    """
    Starts a challenge where the player recalls an attribute or flaw.

   Parameters:
       player (dict): The player's character details including social status
                     and health.
       tribeMates (list): List of dictionaries with tribe mate details.

   Returns:
       bool: True if the player wins the trait challenge, False otherwise.
   """

    print("\n🔍 **Trait Challenge: Recall an Attribute or Flaw!**")
    print("You must name one attribute or flaw of any character in the game!")
    print("⏳ You have **30 seconds** to enter a valid response!")

    startTime = time.time()
    userInput = input("\n💡 Enter an attribute or flaw: ").strip().title()
    endTime = time.time()

    if endTime - startTime > 30:
        print("\n⏰ **Time's up!** You failed to respond in time.")
        player["socialStatus"] = max(0, player["socialStatus"] - 10)
        player["currentHealth"] = max(0, player["currentHealth"] - 10)
        print("📉 **You lost -10 Social Status and -10 Health.**")
        return False  # Player loses

    if userInput in VALID_TRAITS:
        print(f"\n✅ **Correct!** {userInput} is a valid trait.")
        player["socialStatus"] += 25
        player["maxHealth"] += 25
        player["currentHealth"] += 25
        print("📈 **You gained +25 Social Status and +25 Health!**")
        print(
            f"🏥 **Current Health:** {player['currentHealth']} / "
            f"{player['maxHealth']}")
        print(f"📊 **Social Status:** {player['socialStatus']}")
        return True  # Player wins
    else:
        print(f"\n❌ **Incorrect!** {userInput} is not a valid trait.")
        player["socialStatus"] = max(0, player["socialStatus"] - 10)
        player["currentHealth"] = max(0, player["currentHealth"] - 10)
        print("📉 **You lost -10 Social Status and -10 Health.**")
        print(
            f"🏥 **Current Health:** {player['currentHealth']} / "
            f"{player['maxHealth']}")
        print(f"📊 **Social Status:** {player['socialStatus']}")
        return False  # Player loses


def tribeMemory(player, tribeMates):
    """
    Starts a tribe memory challenge where the player arranges
    tribe members' names in alphabetical order.

    Parameters:
        player (dict): The player's character details including social status
                      and health.
        tribeMates (list): List of dictionaries with tribe mate details.

    Returns:
        bool: True if the player successfully orders names, False otherwise.
    """

    correctOrder = sorted([mate["name"] for mate in tribeMates])
    print("\n🧠 **Tribe Memory Challenge: Alphabetical Order!**")
    print("List your tribe mates in **alphabetical order**, separated by commas.")
    print(
        f"🌿 Your current tribe mates: "
        f"{', '.join([mate['name'] for mate in tribeMates])}")

    userInput = input("\n💡 Enter tribe mates in alphabetical order: ").strip(

    ).lower()
    userList = [name.strip().title() for name in userInput.split(",") if name.strip()]

    if userList == correctOrder:
        print("\n✅ **Correct! You remembered your tribe mates perfectly!**")
        player["socialStatus"] += 25
        player["maxHealth"] += 25
        player["currentHealth"] += 25
        print("📈 **You gained +25 Social Status and +25 Health!**")
        print(
            f"🏥 **Current Health:** {player['currentHealth']} / "
            f"{player['maxHealth']}")
        print(f"📊 **Social Status:** {player['socialStatus']}")
        return True  # Player wins
    else:
        print("\n❌ **Incorrect order!**")
        print(f"📜 The correct order was: {', '.join(correctOrder)}")
        player["socialStatus"] = max(0, player["socialStatus"] - 10)
        player["currentHealth"] = max(0, player["currentHealth"] - 10)
        print("📉 **You lost -10 Social Status and -10 Health.**")
        print(
            f"🏥 **Current Health:** {player['currentHealth']} / "
            f"{player['maxHealth']}")
        print(f"📊 **Social Status:** {player['socialStatus']}")
        return False  # Player loses


def numberGame(player, tribeMates):
    """
    Starts a challenge where the player guesses a random number between 1 and 10.

    Parameters:
        player (dict): The player's character details.
        tribeMates (list): List of dictionaries with tribe mate details.

    Returns:
        bool: True if the player guesses correctly, False otherwise.
    """

    correctNumber = random.randint(1, 10)
    print("\n🔢 **Number Guessing Challenge!**")
    print("Try to guess the correct number between **1 and 10**.")

    try:
        userGuess = int(input("\n💡 Enter your guess: ").strip())
    except ValueError:
        print("\n❌ **Invalid input! You must enter a number.**")
        return False  # Player loses

    if userGuess == correctNumber:
        print(f"\n✅ **Correct! The number was {correctNumber}.**")
        player["socialStatus"] += 25
        player["currentHealth"] += 25
        print(f"📈 **+25 Social Status & Health!**")
        return True
    else:
        print(f"\n❌ **Incorrect! The number was {correctNumber}.**")
        player["socialStatus"] = max(0, player["socialStatus"] - 10)
        player["currentHealth"] = max(0, player["currentHealth"] - 10)
        print(f"📉 **-10 Social Status & Health!**")
        return False


def riddleGame(player, tribeMates):
    """
    Starts a Survivor riddle challenge where the player answers a random
    Survivor-themed riddle.

    Parameters:
        player (dict): The player's character details.
        tribeMates (list): List of dictionaries with tribe mate details.

    Returns:
        bool: True if the player answers correctly, False otherwise.
        """
    riddles = {
        "I grant safety, but remain hidden unless found. What am I?": "idol",
        "With fire and parchment, I speak for the tribe. What am I?": "tribal "
                                                                      "council",
        "The more you win me, the longer you stay in the game. What am I?": "immunity"
    }

    riddle, answer = random.choice(list(riddles.items()))
    print("\n🧠 **Survivor Riddle Challenge!**")
    print(f"❓ **Riddle:** {riddle}")

    userGuess = input("\n💡 Enter your answer: ").strip().lower()

    if userGuess == answer:
        print("\n✅ **Correct! You solved the riddle.**")
        player["socialStatus"] += 25
        player["currentHealth"] += 25
        print(f"📈 **+25 Social Status & Health!**")
        return True
    else:
        print(f"\n❌ **Incorrect! The correct answer was: {answer}.**")
        player["socialStatus"] = max(0, player["socialStatus"] - 10)
        player["currentHealth"] = max(0, player["currentHealth"] - 10)
        print(f"📉 **-10 Social Status & Health!**")
        return False


def logicGame(player, tribeMates):
    """
     Starts a Survivor-themed logic game where the player solves puzzles
     or scenarios relevant to the game.

     Parameters:
         player (dict): The player's character details.
         tribeMates (list): List of dictionaries with tribe mate details.

     Returns:
         bool: True if the player solves the logic puzzle, False otherwise.
     """
    puzzles = {
        "There are three players left: Jerri, Rupert, and Cirie. Jerri and Rupert "
        "both voted for Cirie. Cirie didn't vote for Jerri. Who was eliminated?":
            "cirie",
        "You find a Hidden Immunity Idol. Do you play it before or after the votes "
        "are read?": "before",
        "On an island, I help you live / boil me first before I give": "water"
    }

    puzzle, answer = random.choice(list(puzzles.items()))
    print("\n🧩 **Survivor Logic Challenge!**")
    print(f"❓ **Puzzle:** {puzzle}")

    userGuess = input("\n💡 Enter your answer: ").strip().lower()

    if userGuess == answer:
        print("\n✅ **Correct! You solved the puzzle.**")
        player["socialStatus"] += 25
        player["currentHealth"] += 25
        print(f"📈 **+25 Social Status & Health!**")
        return True
    else:
        print(f"\n❌ **Incorrect! The correct answer was: {answer}.**")
        player["socialStatus"] = max(0, player["socialStatus"] - 10)
        player["currentHealth"] = max(0, player["currentHealth"] - 10)
        print(f"📉 **-10 Social Status & Health!**")
        return False


def anagramGame(player, tribeMates):
    """
    Starts a challenge where the player unscrambles a Survivor-related phrase.

    Parameters:
        player (dict): The player's character details.
        tribeMates (list): List of dictionaries with tribe mate details.

    Returns:
        bool: True if the player correctly solves the anagram, False otherwise.
    """
    phrases = {
        "fire represents life": "perresents file rife",
        "the tribe has spoken": "sah nopesk brite the",
        "final three": "treeh nifla"
    }

    phrase, anagram = random.choice(list(phrases.items()))
    print("\n🔀 **Anagram Challenge!**")
    print(f"🔄 Unscramble this Survivor phrase: **{anagram}**")

    userInput = input("\n💡 Enter the correct phrase: ").strip()

    if userInput.lower == phrase.lower():
        print("\n✅ **Correct! You solved the anagram.**")
        player["socialStatus"] += 25
        player["currentHealth"] += 25
        print(f"📈 **+25 Social Status & Health!**")
        return True
    else:
        print(f"\n❌ **Incorrect! The correct phrase was: {phrase}.**")
        player["socialStatus"] = max(0, player["socialStatus"] - 10)
        player["currentHealth"] = max(0, player["currentHealth"] - 10)
        print(f"📉 **-10 Social Status & Health!**")
        return False


def dailyChallenge(player, tribeMates, eliminatedTribeMates, roundNumber):
    """
    Launches a challenge where the player competes against tribe mates to gain
    immunity.

    Parameters:
        player (dict): The player's character details.
        tribeMates (list): List of dictionaries representing the current tribe.
        eliminatedTribeMates (list): List tracking eliminated tribe mates.
        roundNumber (int): The current round of the game.

    Returns:
        tuple: Updated tribe list and whether the player was eliminated.
      """

    print("\n🏆 ⚔️ It's time for the immunity challenge!")

    challenges = {
        1: traitChallenge,
        2: tribeMemory,
        3: numberGame,
        4: riddleGame,
        5: logicGame,
        6: anagramGame
    }
    selectedPuzzle = challenges.get(roundNumber, riddleGame)

    print("\n🧩 Complete this challenge within **30 seconds**!")
    print("1️⃣ Choose to compete")
    print("2️⃣ Forfeit (Give up immunity)")

    choice = input("\n💡 Choose an option (1 or 2): ").strip()

    if choice == "2":  # Player forfeits
        healthPenalty = int(player["currentHealth"] * random.uniform(0.1, 0.3))
        socialPenalty = random.randint(5, 15)

        player["currentHealth"] -= healthPenalty
        player["socialStatus"] = max(0, player["socialStatus"] - socialPenalty)

        print("\n😞 You FORFEIT the challenge.")
        print(
            f"💔 Lost **{healthPenalty} health points** and **-{socialPenalty} "
            f"Social Status**.")
        return tribalCouncil(player, tribeMates)


    startTime = time.time()
    success = selectedPuzzle(player, tribeMates)

    endTime = time.time()

    if endTime - startTime > 30:
        print("\n⏰ Time's up! You failed the challenge!")
        success = False

    if success:
        print("\n🎉 **You WIN the immunity challenge!**")
    else:
        print("\n❌ **You LOST the challenge.**")

    print(f"🏥 Current Health: {player['currentHealth']}/{player['maxHealth']}")
    print(f"📊 Social Status: {player['socialStatus']}\n")

    print("🔥Grab your torch! It's time for Tribal Council...")
    input("Press Enter to continue...")

    updatedTribeMates, eliminated = tribalCouncil(player,
                                                  tribeMates)
    return updatedTribeMates, eliminated


# Section 5 - Tribal Council

def tribalCouncil(player, tribeMates):
    """
    Initializes tribal council, where one tribe member is eliminated by majority vote.
    Simulates a Survivor-style voting process where each tribe
    member votes to eliminate someone. The player's vote influences the outcome,
    with a higher social status increasing their voting power. Players with low
    social status are more likely to be eliminated.

    Parameters:
        player (dict): The player's characte details and status.
        tribeMates (list): List of remaining tribe members.

    Returns:
        tuple: Updated list of tribe members and a boolean indicating if the
        player was eliminated (True or False).
    """
    print("\n🔥 Tribal Council 🔥")
    print("Welcome to tribal council! Who will be voted out tonight?\n")

    print("Tribe members who can be voted out (excluding yourself):")
    for mate in tribeMates:
        print(f"🔹 {mate['name']}\n")

    print(f"⚡️{player['name']}'s Social Status: {player['socialStatus']}")
    print(f"🔅{player['name']}'s Health: {player['currentHealth']}\n")

    # Risk of automatic elimination if the player's social status and health are <10.
    if player["socialStatus"] <= 10 and player["currentHealth"] <= 10:
        if random.choice([True, False]):  # 50% elimination chance
            print(f"🚨 {player['name']} has been eliminated! The tribe has spoken.")
            return None, True

    validNames = [mate["name"] for mate in tribeMates]
    while True:
        playerVote = input(f"📜 Enter the name of a tribe member to vote out  "
                            f"({', '.join(validNames)}): ").strip()
        if playerVote in validNames:
            break
        print("❌ Invalid choice. Please enter a valid name from the list.")

    votes = {name: 0 for name in validNames + [player["name"]]}

    # Player's vote is counted, with higher weight if social status is high.
    voteWeight = 2 if player["socialStatus"] > 75 else 1
    votes[playerVote] += voteWeight

    # Tribe members cast their votes for each other (randomly).
    for mate in tribeMates:
        otherCandidates = [name for name in validNames if name != mate["name"]]
        votes[random.choice(otherCandidates)] += 1

    # If the player's social status is low (< 30), they are more vulnerable.
    if player["socialStatus"] < 30:
        extraVotes = random.randint(1, 3)
        votes[player["name"]] += extraVotes

    maxVotes = max(votes.values())
    eliminatedCandidates = [name for name, count in votes.items() if
                             count == maxVotes]

    # If there's a tie, randomly eliminate one tribe mate from the highest votes.
    eliminated = random.choice(eliminatedCandidates)

    for name, count in sorted(votes.items(), key=lambda item: -item[1]):
        print(f"   {name}: {count} vote(s)")

    if eliminated == player["name"]:
        print(f"☠️ {player['name']} was eliminated! The tribe has spoken.")
        print("\n💀 **GAME OVER. You have been voted out.** 💀")
        print("🏝️ Thank you for playing Survivor: Python Edition! 🏝️")
        return None, True

    else:
        print(f"❌ {eliminated} was voted out of the tribe.")
        return [mate for mate in tribeMates if mate["name"] != eliminated], False


# Section 6 - Final Tribal Council and Ending the Game
def finalTribalCouncil(player, opponent, jury):
    """
    Launches Final Tribal Council where the jury votes for the Sole Survivor. There
    will be a random outcome initiated by the user's argumentation to the jury.

    :param player: dict. The player's character.
    :param opponent: dict. The final opponent.
    :param jury: list. List of eliminated tribe members who will vote.

    :return: str. The name of the Sole Survivor.
    """
    print("\n🏆 **FINAL TRIBAL COUNCIL** 🏆")
    print("Make your case to the jury to vote you to be Sole Survivor.")

    print("\n❓ The jury asks you: \"What will you do with the money?\"")
    print("1️⃣ I will use it to support my family.")
    print("2️⃣ I will use it to chase a dream.")
    print("3️⃣ I will use it for whatever I want - it's my money.")

    while True:
        finalCase = input("\n💡 Select your answer (1, 2, or 3): ").strip()
        if finalCase in ["1", "2", "3"]:
            break
        print("❌ Invalid choice! Please enter 1, 2, or 3.")

    arguments = {
        "1": "I will use it to support my family.",
        "2": "I will use it to chase a dream.",
        "3": "I will use it for whatever I want - it's my money."
    }

    userResponse = arguments[finalCase]
    print(f"\n💬 You respond: \"{userResponse}\"")

    print("\n🤔 The jury is deliberating...")
    time.sleep(3)
    print("🗳️ The votes are being cast...")
    time.sleep(2)

    # Jury randomly determines if they approve or not.
    juryApproval = random.choice(["approve", "disapprove"])

    print("\n📜 The final vote result is being revealed...")
    time.sleep(3)

    if juryApproval == "approve":
        print("\n🌟 The jury nods and says: \"Have a beautiful life.\"")
        winner = player["name"]
    else:
        print(
            "\n❌ The jury shakes their heads and says: \"You don’t deserve the "
            "money!\"")
        winner = opponent["name"]

    time.sleep(2)
    if winner == player["name"]:
        print(f"\n🥇**CONGRATULATIONS! You earned every jury vote!** 🎉")
        print(
            "🎇 You have outwitted, outplayed, and outlasted everyone to win "
            "Survivor!")
    else:
        print(f"\n💔 **{opponent['name']} won the majority of the jury votes.**")
        print("😞 The jury has spoken. You are not the Sole Survivor.")

    print("\n🏝️ **GAME OVER. Thank you for playing Survivor: Python Edition!** 🏝️")
    return winner


# Section 7 - Main Game Loop
def mainGameLoop():
    """
    Runs the main Survivor RPG game loop - the "game brain".

    Players choose a character, make daily decisions, compete in challenges,
    and face eliminations. The game ends after player is voted out or wins.

    Characters can only perform one action per day (status and exit excluded).

    @return: str. The final game outcome (game over or winning).
    """
    print("\n🌴 Welcome to Survivor: Python Edition! 🌴\n")
    input("Press Enter to start your journey!")

    print("Choose your Survivor contestant:")
    # Display of available characters with their attributes and flaws.
    for name, details in CHARACTERS.items():
        print(f"\n🔹 {name}")
        print(f"   🏅 Attributes: {', '.join(details['attributes'])}")
        print(f"   😈️ Flaws: {', '.join(details['flaws'])}")

    # User input for character selection.
    while True:
        playerName = input("\nEnter the name of your Survivor contestant: ").strip()
        if playerName in CHARACTERS:
            break
        print("❌ Invalid choice. Please enter a valid name.")

    # Assign chosen character.
    player = CHARACTERS[playerName]
    player["name"] = playerName
    initializeStats(player)
    tribeMates = generateTribe()
    eliminatedTribeMates = []  # Tracks eliminated players

    # Display tribe members.
    print(f"\n🌟 You're playing as {playerName}! Meet your tribe members:\n")
    input("Press Enter to continue...")

    for mate in tribeMates:
        print(f"🔹 {mate['name']}")
        print(f"😇 Attributes: {', '.join(mate['attributes'])}")
        print(f"😈 Flaws: {', '.join(mate['flaws'])}\n")

    input("Press Enter to continue...")

    # Display Player Stats.
    print("\n📊 Your Stats:")
    print(f"🏥 Health: {player['currentHealth']} / {player['maxHealth']}")
    print(f"📈 Social Status: {player['socialStatus']}")
    print(f"📝 Attributes: {', '.join(player['attributes'])}")
    print(f"😈️ Flaws: {', '.join(player['flaws'])}\n")
    print("\n🎉 Let's see if you can outwit, outplay, and outlast!\n")

    day = 1
    while len(tribeMates) > 1:
        print(f"\n--- Day {day} ---")
        print('Type "help" to see menu.')

        # Limits daily actions.
        actionsPerformed = {"rest": False, "explore": False, "challenge": False}

        while True:
            action = input(
                "Enter an action (rest, explore, challenge, status, exit): "
                "").strip().lower()

            if action == "help":
                print("\n📜 Menu:")
                print("- 💤 rest: Recover health.")
                print("- 🔍 explore: Search for the Hidden Immunity Idol.")
                print("- ⚔️ challenge: Compete in an immunity challenge.")
                print("- 📊 status: View your current health and social status.")
                print("- 🚪 exit: Quit the game.")

            elif action == "exit":
                print("\n👋 You have exited the game. Thanks for playing!")
                return "Game Over: You didn't survive!"

            elif action == "rest":
                if actionsPerformed["rest"]:
                    print("You've already rested today. Choose another action")
                else:
                    print("😴 You take time to rest and recover health.")
                    player["currentHealth"] = min(player["currentHealth"] + 5, player
                    ["maxHealth"])
                    player["socialStatus"] = max(0, player["socialStatus"] - 25)
                    print(
                        f"📉 Your social status has decreased to "
                        f"{player['socialStatus']}.")
                    print(f"🥱 Your health is now {player['currentHealth']}/"
                          f"{player['maxHealth']}.\n")
                    actionsPerformed["rest"] = True
                break

            elif action == "explore":
                if actionsPerformed["explore"]:
                    print("You've already explored today. Choose another action")
                else:
                    exploreIsland(player)
                    actionsPerformed["explore"] = True
                break

            elif action == "challenge":
                tribeMates, eliminated = dailyChallenge(player, tribeMates,
                                                        eliminatedTribeMates, day)

                if eliminated:
                    return "Game Over: You've been voted off the Island!"

                break

            elif action == "status":
                print("\n📊 Current Status:")
                print(f"⚡️ Health: {player['currentHealth']} / {player['maxHealth']}")
                print(f"📈 Social Status: {player['socialStatus']}\n")

            else:
                print("❌ Invalid command. Type 'help' for options.")

        day += 1

    winner = finalTribalCouncil(player, tribeMates[0], eliminatedTribeMates)
    return f"\n🏆 Sole Survivor: {winner} 🏆"


def exploreIsland(player):
    """
    Allows the player to explore and potentially find a Hidden Immunity Idol,
    get caught searching, find nothing, or build an alliance. Each action has a
    positive or negative affect on their status/health.

    Parameters:
        player (dict): The player's character.

    Returns:
        None
    """

    print("\n🏝️ You venture off into the jungle to explore the island and "
          "possibly find a hidden immunity idol...")
    input("Press Enter to continue...")

    outcome = random.choice(["findIdol", "caught", "nothing", "buildAlliance"])

    if outcome == "findIdol":
        print("🎉 Congratulations! You found a Hidden Immunity Idol.")
        player["inventory"].append("Hidden Immunity Idol")
        player["currentHealth"] = player["maxHealth"]
        print("💪 Your health is fully restored!")

    elif outcome == "caught":
        print("😳Oh no! You were caught searching for an idol.")
        player["socialStatus"] -= 20
        print("📉 Your social status decreases by 20.")

    elif outcome == "buildAlliance":
        print("🤝 You encounter another tribe member while exploring.")
        print("After spending time together, you decide to form an alliance!")
        player["socialStatus"] += 10
        print("📈Your social status increases by 10.")

    else:
        print("🕵 You searched for hours, got sunburned, and found nothing.")
        player["currentHealth"] -= 10
        print(
            f"👎 You lost 10 health points. Current health: "
            f"{player['currentHealth']}/{player['maxHealth']}\n")

    input("Press Enter to continue...")


if __name__ == "__main__":
    result = mainGameLoop()
    print(result)
