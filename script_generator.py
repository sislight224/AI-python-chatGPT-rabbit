import openai
import json
import os
import re
import random
import time
from voice_generator import *

def format_for_chatgpt(data, topic, characters):
    character_specific_data = {i: data[i] for i in data if i in characters}
    character_traits = "\n".join(
        [f"{character}: - " + " - ".join([f"{key}: {', '.join(val)}" for key, val in attributes.items()]) for
         character, attributes in character_specific_data.items()])

    return f"{character_traits}"

def involved_characters(prompt, json_data):
    characters = json_data.keys()
    involved = []

    for character in characters:
        # Split character names into first and last names (if they exist)
        names = character.split()

        # Look for any of the names in the prompt
        if any(re.search(r'\b' + re.escape(name) + r'\b', prompt, re.IGNORECASE) for name in names):
            involved.append(character)

    return involved

def add_characters_based_on_weight(selected_chars, json_data, target_count):
    # If there are already enough characters, short-circuit
    if len(selected_chars) >= target_count:
        return selected_chars

    # Define weighted probabilities based on the popularity of characters
    weights = {
        'Homer Simpson': 10,
        'Marge Simpson': 10,
        'Bart Simpson': 10,
        'Lisa Simpson': 10,
        'Maggie Simpson': 9,
        'Mr. Burns': 9,
        'Ned Flanders': 9,
        'Principal Seymour': 8,
        'Moe Szyslak': 8,
        'Krusty the Clown': 8,
        'Chief Wiggum': 7,
        'Apu Nahasapeemapetilon': 7,
        'Milhouse Van Houten': 7,
        'Nelson Muntz': 7,
        'Barney Gumble': 6,
        'Comic Book Guy': 6,
        'Abraham Simpson': 6,
        'Sideshow Bob': 5,
        'Nelson': 5,
        'Apu': 5,
        'Barney': 5,
        'Principal Seymour Skinner': 5
    }
    # Filter out already selected characters
    available_characters = [char for char in json_data.keys() if char not in selected_chars]
    available_weights = [weights[char] for char in available_characters]

    while len(selected_chars) < target_count:
        new_char = random.choices(available_characters, weights=available_weights, k=1)[0]
        selected_chars.append(new_char)
        # Remove the newly added character from the available characters and weights lists
        idx = available_characters.index(new_char)
        del available_characters[idx]
        del available_weights[idx]

    return selected_chars

def generate_prompt(topic_prompt: str = "Homer accidentally spills a drink on Mr. Burns at Moe's Tavern."):
    start_time = time.time()


    openai.api_key = os.environ.get('OPENAI_API_KEY')
    if not openai.api_key:
        raise ValueError("Environment variable OPENAI_API_KEY is not set.")

    with open('resources/simpsons/characters_and_characteristics.json', 'r') as f:
        data = json.load(f)

    characters_in_prompt = involved_characters(prompt=topic_prompt, json_data=data)
    characters_to_use = add_characters_based_on_weight(characters_in_prompt, data, target_count = random.randint(5, 7))

    characters_to_use_prompt = '\n-'.join(characters_to_use)
    dialogue_prompt = f"""Generate a conversation between the following 'The Simpsons' characters {characters_to_use_prompt}, where {topic_prompt}. """


    messages = [
        {"role": "system", "content": "You are a creator of dialogues between popular characters, being able to showcase their intricacies perfectly. The dialogues should be funny, outrageous and can be politically incorrect sometimes. The response should only have the dialogue, in the format: character_name: text. Do not generate any stage directions, Scene Headings, Action, Transitions, Character Name, Dialogue, Parentheticals, Shot, Subheaders or anything outside what the characters say. Only one character can talk at a time. Do not use any disclaimers or anything other than pure dialogue."},
        {"role": "user", "content": f"{dialogue_prompt}"}
    ]
    open_ai_call_time = time.time()
    dialogue_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2000,
        temperature=0.75,
    )
    open_ai_end_call_time = time.time()
    open_ai_elapsed_time = open_ai_end_call_time - open_ai_call_time

    dialogue = dialogue_response.choices[0].message.content.strip()


    end_time = time.time()
    elapsed_time = end_time - start_time



    return characters_to_use, dialogue


async def get_dialogue(prompt: str):
    s = time.time()

    characters_to_use, dialogue = generate_prompt(topic_prompt=prompt)

    lines = dialogue.split("\n\n")  # Split based on double newline to get individual dialogues
    result = []

    for line in lines:
        speaker, text = line.split(': ', 1)
        result.append({speaker: text})
        print({speaker: text})
    result = generate_voice_files(lines_result=result, characters_to_use=characters_to_use, prompt=prompt)

    return result

if __name__ == "__main__":
    get_dialogue("halo")