import json
import os
import struct

class Character:
    def __init__(self, id, alias, prompt, audio_data):
        self.id = id
        self.alias = alias
        self.prompt = prompt
        self.audio_data = audio_data

class CharacterList:
    def __init__(self, characters):
        self.characters = characters

def main():
    generate_from_json("characters.json")

def generate_from_json(json_file_path):
    # Load the JSON file
    with open(json_file_path, 'r') as file:
        json_content = file.read()
        character_list_data = json.loads(json_content)
        
    characters = [Character(**character) for character in character_list_data['characters']]
    
    for character in characters:
        generate_luc_file(character)

def generate_luc_file(character):
    filename = f"./LUX/{character.id}.lux"  # Name of the file based on the character ID
    
    try:
        with open(f"./voices/{character.id}.wav", 'rb') as audio_file:
            audio_data = audio_file.read()  # Load audio data
    except FileNotFoundError:
        return
    
    # Write binary file
    with open(filename, 'wb') as writer:
        # Header
        writer.write(b'LUX1')  # Magic Number
        writer.write(bytes([1]))  # Version
        
        # JSON string
        json_data = json.dumps(character.__dict__).encode('utf-8')
        
        # Write length and JSON data
        writer.write(struct.pack('I', len(json_data)))  # Write length as unsigned int
        writer.write(json_data)
        
        # Write length and audio data
        writer.write(struct.pack('I', len(audio_data)))  # Write length as unsigned int
        writer.write(audio_data)
    
    print(f"The file was successfully created: {filename}")

if __name__ == "__main__":
    main()