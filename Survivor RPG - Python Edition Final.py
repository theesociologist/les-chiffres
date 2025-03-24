"""

This is a text-based role-playing game based on the reality series, "Survivor".
Players compete in immunity challenges, explore the Island, interact with tribe
mates and attempt to avoid elimination at a daily Tribal Council. If
you outwit, outplay, and outlast the other castaways, you are the Sole Survivor and
the winner of one million dollars!
"""

import random
import time
import json
import os

validTraits = [
    "Extrovert", "Disarming", "Smart", "Confident", "Athletic",
    "Resourceful", "Sneaky", "Sweet", "Charismatic", "Strategic",
    "Cerebral", "Naive", "Unathletic", "Moody", "Insecure",
    "Follower", "Delusionally Confident", "Self-Indulgent", "Jealous", "Blunt"
]

# Attribute scores and flaw penalties

ATTRIBUTE_SCORES = {
    "Extrovert": 5, "Disarming": 10, "Smart": 7, "Confident": 8,
    "Athletic": 6, "Resourceful": 4, "Sneaky": 2, "Sweet": 3, "Charismatic": 9,
    "Strategic": 5,
}

FLAW_PENALTIES = {
    "Cerebral": -5, "Naive": -2, "Unathletic": -5, "Moody": -8,
    "Insecure": -7, "Follower": -3, "Delusionally Confident": -6,
    "Self-Indulgent": -4, "Jealous": -9, "Blunt": -10
}


#CHALLENGE CLASS
class Challenge:
    """
    Superclass for all challenges in the game. Each challenge must implement
    its own version of `startChallenge`.

    @param name: str. The name of the challenge.
    """
    def __init__(self, name):
        self.name = name

    def startChallenge(self, hero, tribeMates):
        raise NotImplementedError("Each challenge must have its own method.")

    def handleResult(self, player, success):
        """
         Adjusts the player's social status and health based on the outcome
         of the challenge.

         @param player: Character. The player participating in the challenge.
         @param success: bool. Indicates whether the player won the challenge.
        """
        if success:
            print("\n🎉 You WIN the challenge!")
            player.modifySocialStatus(25)
            player.modifyHealth(25)
        else:
            print("\n❌ You LOST the challenge.")
            player.modifySocialStatus(-10)
            player.modifyHealth(-10)

        print(f"🏥 Current Health: {player.currentHealth}/{player.maxHealth}")
        print(f"📊 Social Status: {player.socialStatus}\n")

    def checkTimer(self, startTime, limit=30):
        """
        Checks whether the challenge response time is within the allowed limit.

        @param startTime: float. The starting time of the challenge.
        @param limit: int. Optional. Default is 30 seconds. Maximum time allowed.

        @return: bool. True if within time, False otherwise.
        """
        return (time.time() - startTime) <= limit


#Trait Challenge SubClass
class TraitChallenge(Challenge):
    """Player must recall an attribute or flaw. Inherits from Challenge."""

    def __init__(self):
        super().__init__("Trait Challenge")

    def startChallenge(self, player, tribeMates):
        """
          Prompts the player to recall and enter a valid attribute or flaw.

          @param player: Character. The player attempting the challenge.
          @param tribeMates: list. List of Enemy tribe mates.

          @return: bool. True if successful, False otherwise.
        """
        print("\n🔍 Trait Challenge: Recall an Attribute or Flaw!")
        print("You must name one attribute or flaw of any character in the game!")
        print("⏳ You have 30 seconds to enter a valid response.")

        startTime = time.time()
        userInput = input("\n💡 Enter an attribute or flaw: ").strip().title()
        endTime = time.time()

        if endTime - startTime > 30:
            print("\n⏰ Time's up! You failed to respond in time.")
            player.modifySocialStatus(-10)
            player.modifyHealth(-10)
            return False

        if userInput in validTraits:
            print(f"\n✅ Correct! {userInput} is a valid trait.")
            player.modifySocialStatus(25)
            player.modifyHealth(25)
            return True
        else:
            print(f"\n❌ Incorrect! {userInput} is not a valid trait.")
            player.modifySocialStatus(-10)
            player.modifyHealth(-10)
            return False

#Memory Challenge Subclass
class TribeMemoryChallenge(Challenge):
    """A challenge where the player orders tribe mates in alphabetical order.
    Inherits from Challenge."""

    def __init__(self):
        super().__init__("Tribe Memory Challenge")

    def startChallenge(self, player, tribeMates):
        """
         Prompts the player to input tribe mates' names in alphabetical order.

         @param player: Character. The player attempting the challenge.
         @param tribeMates: list. List of Enemy tribe mates.

         @return: bool. True if order is correct, False otherwise.
        """
        correctOrder = sorted([mate.name for mate in tribeMates])
        scrambledNames = random.sample(correctOrder,
                                       len(correctOrder))  # randomize display order

        print("\n🧠 Tribe Memory Challenge: Alphabetical Order!")
        print("List your tribe mates in **alphabetical order**, separated by commas.")
        print(f"🌿 Your current tribe mates: {', '.join(scrambledNames)}")

        userInput = input("\n💡 Enter tribe mates in alphabetical order: ").strip().lower()
        userList = [name.strip().title() for name in userInput.split(",") if name.strip()]

        if userList == correctOrder:
            print("\n✅ Correct! You placed your tribe mates' names in perfect order!")
            player.modifySocialStatus(25)
            player.modifyHealth(25)
            return True
        else:
            print("\n❌ Incorrect order!")
            print(f"📜 The correct order was: {', '.join(correctOrder)}")
            player.modifySocialStatus(-10)
            player.modifyHealth(-10)
            return False

#Number Challenge Subclass
class NumberGuessChallenge(Challenge):
    """
    A challenge where the player attempts to guess a random number between 1 and 10.
    Inherits from Challenge.
    """
    def __init__(self):
        super().__init__("Number Guessing Challenge")

    def startChallenge(self, player, tribeMates):
        """
        Prompts the player to guess a number between 1 and 10.

        @param player: Character. The player attempting the challenge.
        @param tribeMates: list. List of Enemy tribe mates.

        @return: bool. True if the guess is correct, False otherwise.
        """
        correctNumber = random.randint(1, 10)

        print("\n🔢 Number Guessing Challenge!")
        print("Try to guess the correct number between 1 and 10.")

        try:
            userGuess = int(input("\n💡 Enter your guess: ").strip())
        except ValueError:
            print("\n❌ Invalid input! You must enter a number.")
            player.modifySocialStatus(-10)
            player.modifyHealth(-10)
            return False

        if userGuess == correctNumber:
            print(f"\n✅ Correct! The number was {correctNumber}.")
            player.modifySocialStatus(25)
            player.modifyHealth(25)
            return True
        else:
            print(f"\n❌ Incorrect! The number was {correctNumber}.")
            player.modifySocialStatus(-10)
            player.modifyHealth(-10)
            return False

#Riddle Challenge SubClass
class RiddleChallenge(Challenge):
    """
    A challenge where the player solves a Survivor-themed riddle.
    Inherits from Challenge.
    """
    def __init__(self):
        super().__init__("Survivor Riddle Challenge")

    def startChallenge(self, player, tribeMates):
        """
        Prompts the player with a riddle and checks their answer.

        @param player: Character. The player attempting the challenge.
        @param tribeMates: list. List of Enemy tribe mates.

        @return: bool. True if the riddle is answered correctly, False otherwise.
        """
        riddles = {
            "I grant safety, but remain hidden unless found. What am I?": "idol",
            "With fire and parchment, I speak for the tribe. What am I?": "tribal council",
            "The more you win me, the longer you stay in the game. What am I?": "immunity"
        }

        riddle, answer = random.choice(list(riddles.items()))
        print("\n🧠 **Survivor Riddle Challenge!**")
        print(f"❓ **Riddle:** {riddle}")

        startTime = time.time()
        userGuess = input("\n💡 Enter your answer: ").strip().lower()

        if not self.checkTimer(startTime):
            print("\n⏰ Time's up! You failed to respond in time.")
            return self.handleResult(player, success=False)

        if userGuess == answer:
            print("\n✅ Correct! You solved the riddle.")
            player.modifySocialStatus(25)
            player.modifyHealth(25)
            return True
        else:
            print(f"\n❌ Incorrect. The correct answer was: {answer}.")
            player.modifySocialStatus(-10)
            player.modifyHealth(-10)
            return False

#Logic Challenge SubClass
class LogicChallenge(Challenge):
    """
    A logic-based challenge that presents a puzzle or scenario.
    Inherits from Challenge.
    """
    def __init__(self):
        super().__init__("Logic Challenge")

    def startChallenge(self, player, tribeMates):
        """
        Prompts the player with a logic puzzle and checks their response.

        @param player: Character. The player attempting the challenge.
        @param tribeMates: list. List of Enemy tribe mates.

        @return: bool. True if correct, False otherwise.
        """
        puzzles = {
            "There are three players left: Jerri, Rupert, and Cirie. Jerri and Rupert both voted for Cirie. Cirie didn't vote for Jerri. Who was eliminated?": "cirie",
            "You find a Hidden Immunity Idol. Do you play it before or after the votes are read?": "before",
            "On an island, I help you live / boil me first before I give": "water"
        }

        puzzle, answer = random.choice(list(puzzles.items()))

        print("\n🧩 Logic Challenge!")
        print(f"❓ Puzzle: {puzzle}")

        userGuess = input("\n💡 Enter your answer: ").strip().lower()

        if userGuess == answer:
            print("\n✅ Correct! You solved the puzzle.")
            player.modifySocialStatus(25)
            player.modifyHealth(25)
            return True
        else:
            print(f"\n❌ Incorrect! The correct answer was: {answer}.")
            player.modifySocialStatus(-10)
            player.modifyHealth(-10)
            return False

#Anagram Challenge Sub Class
class AnagramChallenge(Challenge):
    """
    A word challenge where the player unscrambles a Survivor-themed phrase.
    Inherits from Challenge.
    """
    def __init__(self):
        super().__init__("Anagram Challenge")

    def startChallenge(self, player, tribeMates):
        """
       Prompts the player with an anagram and checks the correct solution.

       @param player: Character. The player attempting the challenge.
       @param tribeMates: list. List of Enemy tribe mates.

       @return: bool. True if anagram is solved, False otherwise.
       """
        phrases = {
            "fire represents life": "perresents file rife",
            "the tribe has spoken": "sah nopesk brite the",
            "final three": "treeh nifla"
        }

        phrase, anagram = random.choice(list(phrases.items()))

        print("\n🔀 Anagram Challenge!")
        print(f"🔄 Unscramble this Survivor phrase: {anagram}")

        userInput = input("\n💡 Enter the correct phrase: ").strip().lower()

        if userInput == phrase.lower():
            print("\n✅ Correct! You solved the anagram.")
            player.modifySocialStatus(25)
            player.modifyHealth(25)
            return True
        else:
            print(f"\n❌ Incorrect! The correct phrase was: {phrase}.")
            player.modifySocialStatus(-10)
            player.modifyHealth(-10)
            return False

def dailyChallenge(player, tribeMates):
    """
    Launches a challenge where the player competes against tribe mates to gain
    immunity. Tribal Council is automatically triggered after the challenge.

    Parameters:
        player (Hero): The player's character.
        tribeMates (list): List of Enemy objects representing the current tribe.

    Returns:
        tuple: (updated tribeMates list, boolean indicating if player was eliminated)
    """

    print("\n🏆 ⚔️ It's time for the immunity challenge!")

    challengeClasses = [
        TraitChallenge,
        TribeMemoryChallenge,
        NumberGuessChallenge,
        RiddleChallenge,
        LogicChallenge,
        AnagramChallenge
    ]
    challenge = random.choice(challengeClasses)()

    print(f"\n🧩 Today's challenge: {challenge.name}")
    print("1️⃣ Choose to compete")
    print("2️⃣ Forfeit (Give up immunity)")

    choice = input("\n💡 Choose an option (1 or 2): ").strip()

    if choice == "2":
        healthPenalty = int(player.currentHealth * random.uniform(0.1, 0.3))
        socialPenalty = random.randint(5, 15)
        player.modifyHealth(-healthPenalty)
        player.modifySocialStatus(-socialPenalty)

        print("\n😞 You FORFEIT the challenge.")
        print(f"💔 Lost {healthPenalty} health and -{socialPenalty} Social Status.")
        return tribalCouncil(player, tribeMates)

    success = challenge.startChallenge(player, tribeMates)

    if success:
        print("\n🎉 You WIN the immunity challenge!")
    else:
        print("\n❌ You LOST the challenge.")

    print(f"🏥 Health: {player.currentHealth}/{player.maxHealth}")
    print(f"📊 Social Status: {player.socialStatus}")

    print("\n🔥 Grab your torch! It's time for Tribal Council...")
    input("Press Enter to continue...")

    return tribalCouncil(player, tribeMates)

#CHARACTER CLASS
class Character:
    """
    Represents the Hero character in the game with core stats such as health,
    social status, attributes, and flaws.

    @param name: str. The character's name.
    @param attributes: list[str]. Positive traits that boost stats.
    @param flaws: list[str]. Negative traits that reduce stats.
    @param currentHealth: int. Optional. The character's current health level.
    @param maxHealth: int. Optional. The character's maximum health.
    @param socialStatus: int. Optional. The character's current social standing.
    """
    def __init__(self, name, attributes, flaws, currentHealth=None, maxHealth=None, socialStatus=None ):
        self.name = name
        self.attributes = attributes
        self.flaws = flaws
        self.maxHealth = 100
        self.inventory = []

        # Only calculate stats if currentHealth/socialStatus not provided
        if currentHealth is None or socialStatus is None:
            self.currentHealth = 70  # Base before adjustment
            self.socialStatus = 50  # Base before adjustment
            self.initializeStats()
        else:
            self.currentHealth = currentHealth
            self.socialStatus = socialStatus

    def isAlive(self):
        """
        Checks if the character is still alive.

        @return: bool. True if health is greater than zero, otherwise False.
        """
        return self.currentHealth > 0

    def modifyHealth(self, amount):
        """
        Modifies the character’s health by a specified amount.

        @param amount: int. The amount to adjust health (can be positive or negative).
        """
        self.currentHealth = max(0,
                                 min(self.maxHealth, self.currentHealth + amount))

    def modifySocialStatus(self, amount):
        """
        Modifies the character’s social status.

        @param amount: int. Amount to adjust social status (can be positive or negative).
        """
        self.socialStatus = max(0, self.socialStatus + amount)

    def initializeStats(self):
        """
        Initializes and adjusts the character's health and social status
        based on their attributes and flaws.
        """
        for attr in self.attributes:
            self.socialStatus += ATTRIBUTE_SCORES.get(attr, 0)
            self.currentHealth += ATTRIBUTE_SCORES.get(attr, 0) // 2

        for flaw in self.flaws:
            self.socialStatus += FLAW_PENALTIES.get(flaw, 0)
            self.currentHealth += FLAW_PENALTIES.get(flaw, 0) // 2

        self.currentHealth = min(self.currentHealth, self.maxHealth)
        self.socialStatus = max(0, self.socialStatus)

    def toDict(self):
        """
        Converts the character's current state into a dictionary for saving.

        @return: dict. Serialized character attributes for saving/loading.
        """
        return {
            "name": self.name,
            "attributes": self.attributes,
            "flaws": self.flaws,
            "currentHealth": self.currentHealth,
            "maxHealth": self.maxHealth,
            "socialStatus": self.socialStatus,
            "inventory": self.inventory if hasattr(self, "inventory") else []
        }

#HERO SUBCLASS AND CHARACTERS
class Hero(Character):
    """
    Represents the Hero character in the game. Inherits from Character
    and includes additional behavior such as exploration and voting.

    @param name: str. The player's name.
    @param attributes: list[str]. Positive traits that boost stats.
    @param flaws: list[str]. Negative traits that reduce stats.
    @param currentHealth: int. Optional. The player's current health.
    @param maxHealth: int. Optional. The player's max health.
    @param socialStatus: int. Optional. The player's social standing.
    """
    def __init__(self, name, attributes, flaws, currentHealth=100, maxHealth=100, socialStatus=50):
        super().__init__(name, attributes, flaws, currentHealth, maxHealth,
        socialStatus)
        self.isPlayer = True
        self.inventory = []
        self.hasIdol = False

    def castVote(self, choices):
        """
        Prompts the player to manually vote for a tribe member to eliminate.

        @param choices: list[str]. Names of eligible tribe members.

        @return: str. The name of the selected vote recipient.
        """
        while True:
            vote = input(f"📜 Enter the name of a tribe member to vote out ({', '.join(choices)}): ").strip()
            if vote in choices:
                return vote
            print("❌ Invalid choice. Please enter a valid name from the list.")

    def toDict(self):
        """
        Converts the Hero's stats to a dictionary to include all attributes and
        properties to save the game.

        @return: A dictionary containing all the attributes of the current object.
        """
        return super().toDict()

    def explore(self):
        """
        Allows the player to explore the island to find idols or build
        alliances. Outcomes affect health and social status.
        """
        print("\n🏝️ You venture off into the jungle to explore the island and "
              "possibly find a hidden immunity idol...")
        input("Press Enter to continue...")

        outcome = random.choice(["findIdol", "caught", "nothing", "buildAlliance"])

        if outcome == "findIdol":
            if self.hasIdol:
                print(" You found another idol...but you already have one.")
            else:
                self.hasIdol = True
                print("🎉 Congratulations! You found a Hidden Immunity Idol.")
                self.inventory.append("Hidden Immunity Idol")
                self.currentHealth = self.maxHealth
                print("💪 Your health is fully restored!")

        elif outcome == "caught":
            print("😳 Oh no! You were caught searching for an idol.")
            self.modifySocialStatus(-20)
            print("📉 Your social status decreases by 20.")

        elif outcome == "buildAlliance":
            print("🤝 You encounter another tribe member while exploring.")
            print("After spending time together, you decide to form an alliance!")
            self.modifySocialStatus(10)
            print("📈 Your social status increases by 10.")

        else:
            print("🕵 You searched for hours, got sunburned, and found nothing.")
            self.modifyHealth(-10)
            print(f"👎 You lost 10 health points. Current health: {self.currentHealth}/{self.maxHealth}")

        input("Press Enter to continue...")

    def rest(self):
        """
        Allows the player to rest and recover some health at the cost
        of social status.
        """
        print(f"\n🛌 {self.name} finds a quiet spot to rest and recover...")
        input("Press Enter to continue...")

        restoredHealth = min(20, self.maxHealth - self.currentHealth)
        self.modifyHealth(restoredHealth)
        self.modifySocialStatus(-25)

        print(f"💤 You recovered {restoredHealth} health.")
        print(f"📉 But your social status dropped by 25 for being less active.")
        print(f"🏥 Current Health: {self.currentHealth}/{self.maxHealth}")
        print(f"📊 Social Status: {self.socialStatus}")

        input("Press Enter to continue...")


#ENEMY SUBCLASS
class Enemy(Character):
    """
    Represents a non-playable tribe member. Votes randomly during Tribal Council.
    Inherits from Character.

    @param name: str. The character's name.
    @param attributes: list[str]. Positive traits that boost stats.
    @param flaws: list[str]. Negative traits that reduce stats.
    @param currentHealth: int. Optional. The character's current health.
    @param maxHealth: int. Optional. The character's max health.
    @param socialStatus: int. Optional. The character's social standing.
    """
    def __init__(self, name, attributes, flaws, currentHealth=None, maxHealth=100,
                 socialStatus=None):
        super().__init__(name, attributes, flaws, currentHealth, maxHealth, socialStatus)
        self.isPlayer = False
        self.hasIdol = False #tracks immunity idol

    def castVote(self, choices):
        """
        Randomly selects a name from the list of available tribe mates to vote out.

        @param choices: list[str]. Names of tribe mates eligible for elimination.

        @return: str. The name of the tribe mate voted against.
        """

        return random.choice(choices)

    def toDict(self):
        """
        Saves the Tribe Mate's state to save the game.

        @return: dict. Dictionary of the enemy’s game data.
        """
        return super().toDict()

#Character dictionary updated with Hero instances
CHARACTERS = {
    "Evvie": Hero(
        name="Evvie",
        attributes=["Extrovert", "Disarming", "Smart"],
        flaws=["Cerebral", "Naive", "Unathletic"]
    ),
    "Teeny": Hero(
        name="Teeny",
        attributes=["Disarming", "Sneaky", "Sweet"],
        flaws=["Moody", "Insecure", "Follower"]
    ),
    "Parvati": Hero(
        name="Parvati",
        attributes=["Confident", "Athletic", "Resourceful"],
        flaws=["Delusionally Confident", "Self-Indulgent", "Jealous"]
    )
}

#SAVE GAME
import json
import os

# File path for saved data
saveFile = os.path.join(os.getcwd(), "survivorRpgSave.json")
print(f"📂 Saving file at: {saveFile}")

def saveGame(player, tribeMates, eliminatedTribeMates, day):
    """
    Saves the current game state to a JSON file including the player,
    tribe mates, eliminated tribe mates, and day count.

    @param player: Hero. The player character.
    @param tribeMates: list[Enemy]. Current tribe mates.
    @param eliminatedTribeMates: list[Enemy]. Eliminated tribe members.
    @param day: int. Current day in the game.
    """
    print("\n💾 Attempting to save game...")

    gameState = {
        "player": player.toDict(),
        "tribeMates": [mate.toDict() for mate in tribeMates],
        "eliminatedTribeMates": [mate.toDict() for mate in eliminatedTribeMates],
        "day": day
    }

    try:
        with open(saveFile, "w") as file:
            json.dump(gameState, file, indent=4)
        print("✅ Game saved successfully!")
        print(f"📂 The file is located here: {saveFile}")
    except Exception as e:
        print(f"⚠️ Error saving game: {e}")

def loadGame():
    """
   Loads the saved game from a JSON file and reconstructs the player,
   tribe mates, and eliminated tribe mates.

   @return: dict or None. Game state including player, tribeMates,
            eliminatedTribeMates, and day if successful. Returns None
            if loading fails or save file does not exist.
   """
    if not os.path.exists(saveFile):
        print("\n⚠️ No saved game found.")
        return None

    try:
        with open(saveFile, "r") as file:
            gameState = json.load(file)

        print(f"\n📂 Loaded Game Data: {json.dumps(gameState, indent=4)}")

        playerDict = gameState["player"]
        player = Hero(
            name=playerDict["name"],
            attributes=playerDict["attributes"],
            flaws=playerDict["flaws"],
            currentHealth=playerDict["currentHealth"],
            maxHealth=playerDict["maxHealth"],
            socialStatus=playerDict["socialStatus"]
        )
        player.inventory = playerDict.get("inventory", [])

        tribeMates = []
        for tribeMateDict in gameState["tribeMates"]:
            tribeMate = Enemy(
                name=tribeMateDict["name"],
                attributes=tribeMateDict["attributes"],
                flaws=tribeMateDict["flaws"],
                currentHealth=tribeMateDict["currentHealth"],
                maxHealth=tribeMateDict["maxHealth"],
                socialStatus=tribeMateDict["socialStatus"]
            )
            tribeMates.append(tribeMate)

        eliminatedTribeMates = []
        for tribeMateDict in gameState["eliminatedTribeMates"]:
            tribeMate = Enemy(
                name=tribeMateDict["name"],
                attributes=tribeMateDict["attributes"],
                flaws=tribeMateDict["flaws"],
                currentHealth=tribeMateDict["currentHealth"],
                maxHealth=tribeMateDict["maxHealth"],
                socialStatus=tribeMateDict["socialStatus"]
            )
            eliminatedTribeMates.append(tribeMate)

        day = gameState.get("day", 1)

        print("✅ Game loaded successfully!")
        return {
            "player": player,
            "tribeMates": tribeMates,
            "eliminatedTribeMates": eliminatedTribeMates,
            "day": gameState.get("day", 1)
        }
    except Exception as e:
        print(f"\n⚠️ Error loading game: {e}")
        return None


# GAME SETUP

"""
This determines player characters, attributes, and flaws. Each Survivor contestant
has unique skills, weaknesses, and statistics that affects performance. Each 
character is based on a real Survivor player. 
"""

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


#TRIBE MATES
def generateTribe():
    """
    Generates 5 random tribe members with randomized attributes, flaws, and health.

    Returns:
        list of Enemy objects (tribe mates).
    """
    tribe = []
    names = [
        "Brice", "Cirie", "Zeke", "Boston Rob", "Tasha", "Spencer",
        "Jaison", "Fabio", "Kass", "Ozzy", "Shan", "Adam", "Franny", "Q", "Donathan",
        "Desi", "Katurah", "Shambo", "Wendell", "Rachel", "Hunter", "Venus"
    ]
    for name in random.sample(names, 5):
        attributes = random.sample(list(ATTRIBUTE_SCORES.keys()), 3)
        flaws = random.sample(list(FLAW_PENALTIES.keys()), 3)
        tribeMate = Enemy(name, attributes, flaws)
        tribe.append(tribeMate)

    return tribe

def displayTribe(tribeMates):
    """
    Displays the tribe mates' names, attributes, flaws, and stats.

    Parameters:
    tribeMates (list): List of Enemy objects to display.

    Returns: None
    """

    print("\n🤼‍♀️ Your Tribe Mates:")
    for mate in tribeMates:
        print(f"   🔹 Name: {mate.name}")
        print(f"   🏅 Attributes: {', '.join(mate.attributes)}")
        print(f"   😈 Flaws: {', '.join(mate.flaws)}")
        print(f"   ❤️ Health: {mate.currentHealth}/{mate.maxHealth}")
        print(f"   📊 Social Status: {mate.socialStatus}")
        print("-" * 40)

# TRIBAL COUNCIL
def tribalCouncil(player, tribeMates):
    """
    Launches Tribal Council sequence. All tribe members vote to eliminate
    one player. Handles vote tallying, tie-breaker revote, and final decision.

    @param player: Hero. The player character.
    @param tribeMates: list[Enemy]. List of current tribe members.

    @return: tuple. Updated tribe mates list and a bool indicating if
             the player was eliminated.
    """

    print("\n🔥 Tribal Council 🔥")
    print("Welcome to tribal council! Who will be voted out tonight?\n")

    print("Tribe members who can be voted out (excluding yourself):")
    for mate in tribeMates:
        print(f"🔹 {mate.name}")
    print("\n")

    print(f"⚡️{player.name}'s Social Status: {player.socialStatus}")
    print(f"🔅{player.name}'s Health: {player.currentHealth}/{player.maxHealth}\n")

    validNames = [mate.name for mate in tribeMates]
    playerVote = player.castVote(validNames)# Player vote

    # Initialize vote tally
    votes = {name: 0 for name in validNames + [player.name]}
    voteWeight = 2 if player.socialStatus > 75 else 1
    votes[playerVote] += voteWeight

    # Tribe members cast their votes randomly
    for mate in tribeMates:
        otherCandidates = [name for name in validNames if name != mate.name]
        vote = mate.castVote(otherCandidates)
        votes[vote] += 1

    print("\n🗳️The votes have been tallied:")
    for name, count in sorted(votes.items(), key=lambda item: -item[1]):
        print(f"   {name}: {count} vote(s)")

    maxVotes = max(votes.values())
    eliminatedCandidates = [name for name, count in votes.items() if count ==
                            maxVotes]

    # If there's a tie, trigger a revote
    if len(eliminatedCandidates) > 1:
        print("\n⚠️ There is a tie! A revote will take place.")
        votes = {name: 0 for name in eliminatedCandidates}

        playerVote = player.castVote(eliminatedCandidates)
        votes[playerVote] += voteWeight

        # Tribe revotes for the tied contestants
        for mate in tribeMates:
            vote = mate.castVote(eliminatedCandidates)
            votes[vote] += 1

        maxVotes = max(votes.values())
        eliminatedCandidates = [name for name, count in votes.items() if count == maxVotes]

        # If there's another tie, eliminate at random
        if len(eliminatedCandidates) > 1:
            print("\n⚠️ The revote resulted in another tie! The elimination will be determined randomly.")
            eliminated = random.choice(eliminatedCandidates)
        else:
            eliminated = eliminatedCandidates[0]
    else:
        eliminated = eliminatedCandidates[0]

    print("\n📜 Final vote tally:")
    for name, count in sorted(votes.items(), key=lambda item: -item[1]):
        print(f"   {name}: {count} vote(s)")

    if eliminated == player.name:
        print(f"☠️ {player.name} was eliminated! The tribe has spoken.")
        print("\n💀 **GAME OVER. You have been voted out.** 💀")
        print("🏝️ Thank you for playing Survivor: Python Edition! 🏝️")
        return None, True

    else:
        print(f"❌ {eliminated} was voted out of the tribe.")
        updatedTribe = [mate for mate in tribeMates if mate.name != eliminated]
        return updatedTribe, False

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
        winner = player.name
    else:
        print(
            "\n❌ The jury shakes their heads and says: \"You don’t deserve the "
            "money!\"")
        winner = opponent.name

    time.sleep(2)
    if winner == player.name:
        print(f"\n🥇**CONGRATULATIONS! You earned every jury vote!** 🎉")
        print(
            "🎇 You have outwitted, outplayed, and outlasted everyone to win "
            "Survivor!")
    else:
        print(f"\n💔 **{opponent.name} won the majority of the jury votes.**")
        print("😞 The jury has spoken. You are not the Sole Survivor.")

    print("\n🏝️ **GAME OVER. Thank you for playing Survivor: Python Edition!** 🏝️")
    return winner


#Main Game Loop
def mainGameLoop(player=None, tribeMates=None, eliminatedTribeMates=None, day=1,
                 isNewGame=False):
    """
    Runs the main Survivor RPG game loop - the "game brain".

    @param player: Hero or None. Optional. The player character. If not provided,
                   the user will select a new one.
    @param tribeMates: list[Enemy] or None. Optional. The current tribe members.
    @param eliminatedTribeMates: list[Enemy] or None. Optional. The eliminated tribe members.
    @param day: int. The current day in the game.
    @param isNewGame: bool. Indicates whether the session is a new game.

    @return: str. Final outcome message ("Game Over" or "Sole Survivor").

    Returns:
        str: Final result message from the game.
    """
    print("\n🌴 Welcome to Survivor: Python Edition! 🌴\n")
    input("Press Enter to start your journey!")

    # Main menu
    while True:
        print("\n Main Menu:")
        print("1. Start New Game")
        print("2. Load Saved Game")
        if player:
            print("3. Save Game")
            print("4. Return to Game")
            print("5. Exit")
            maxChoice = 5
        else:
            print("3. Exit")
            maxChoice = 3

        choice = input(f"Enter your choice (1-{maxChoice}): ").strip()

        if choice == "1":
            isNewGame = True
            break  # Exit menu loop and start a new game

        elif choice == "2":
            gameState = loadGame()
            if gameState:
                player = gameState["player"]
                tribeMates = gameState["tribeMates"]
                eliminatedTribeMates = gameState["eliminatedTribeMates"]
                day = gameState.get("day", 1)
                print(
                    f"\n✅ Game loaded successfully! Welcome back. It's now Day {day}.")
                isNewGame = False
                break  # ✅ Continue the game loop with loaded data
            else:
                print("\n⚠️ No saved game found. Starting a new game.")
                isNewGame = True
                break

        elif choice == "3" and player:
            saveGame(player, tribeMates, eliminatedTribeMates, day)
            print("\n💾 Game saved!")

        elif choice == "4" and player:
            break  # Return to game

        elif choice == "3" and not player or choice == "5":
            print("\n👋 Thanks for playing! Goodbye!")
            return

        else:
            print("❌ Invalid choice. Please enter a valid option.")

    # Starting a new game
    if isNewGame:
        day = 1
        print("\n🌟 Starting a new game...")

        # Survivor character selection
        print("Choose your Survivor contestant:")
        for name, details in CHARACTERS.items():
            # Safeguard to ensure `details` is a dictionary
            if not isinstance(details, Hero):
                raise TypeError()
                raise TypeError(f"Invalid character data for {name}. Expected a Hero object, got {type(details).__name__}")
            print(f"\n🔹 {name}")
            print(f"   🏅 Attributes: {', '.join(details.attributes)}")
            print(f"   😈️ Flaws: {', '.join(details.flaws)}")

        while True:
            playerName = input(
                "\nEnter the name of your Survivor contestant: ").strip()
            if playerName in CHARACTERS:
                break
            print("❌ Invalid choice. Please enter a valid name.")

        # Create the player as a Hero object
        player = Hero(
            name=playerName,
            attributes=CHARACTERS[playerName].attributes,
            flaws=CHARACTERS[playerName].flaws,
            currentHealth=CHARACTERS[playerName].currentHealth,
            maxHealth=CHARACTERS[playerName].maxHealth
        )

        tribeMates = generateTribe()  # Should return Enemy instances
        eliminatedTribeMates = []
        displayTribe(tribeMates)

    # Verify `tribeMates` is not None before starting the main game loop
    if tribeMates is None:
        print(
            "\n⚠️ Warning: Tribe mates were not initialized. Generating new tribe...")
        tribeMates = generateTribe()

    # Verify `eliminatedTribeMates` is initialized
    if eliminatedTribeMates is None:
        eliminatedTribeMates = []

    # Main Game Loop
    while len(tribeMates) > 1:
        print(f"\n--- Day {day} ---")
        print('Type "help" to see menu.')

        actionsPerformed = {"rest": False, "explore": False, "challenge": False}

        while True:
            action = input(
                "Enter an action (rest, explore, challenge, status, help, save, exit): ").strip().lower()

            if action == "help":
                print("\n📜 Menu:")
                print("- 💤 rest: Recover health.")
                print("- 🔍 explore: Search for hidden advantages.")
                print("- ⚔️ challenge: Compete in an immunity challenge.")
                print("- 📊 status: View your current health and social status.")
                print("- 💾 save: Save your game.")
                print("- 🚪 exit: Quit the game.")

            elif action == "exit":
                print("\n👋 You have exited the game. Thanks for playing!")
                return

            elif action == "rest":
                if actionsPerformed["rest"]:
                    print("You've already rested today. Choose another action")
                else:
                    player.rest()
                    actionsPerformed["rest"] = True
                break

            elif action == "explore":
                if actionsPerformed["explore"]:
                    print("You've already explored today. Choose another action")
                else:
                    player.explore()
                    actionsPerformed["explore"] = True
                break

            elif action == "challenge":
                tribeMates, eliminated = dailyChallenge(player, tribeMates)
                if eliminated:
                    return "☠️Game Over: You've been voted off the Island."
                break

            elif action == "status":
                print("\n📊 Current Status:")
                print(f"⚡️ Health: {player.currentHealth} / {player.maxHealth}")
                print(f"📈 Social Status: {player.socialStatus}\n")
                if player.hasIdol:
                    print("   🗿 Holding a Hidden Immunity Idol!")

            elif action == "save":
                saveGame(player, tribeMates, eliminatedTribeMates, day)
                print("\n💾 Game saved!")
                break

        saveGame(player, tribeMates, eliminatedTribeMates, day)
        day += 1

    winner = finalTribalCouncil(player, tribeMates[0], eliminatedTribeMates)
    return f"\n🏆 Sole Survivor: {winner} 🏆"


if __name__ == "__main__":
    result = mainGameLoop()
    print(result)
