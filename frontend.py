import os
import json
import requests

# Lists all JSON files in the current working directory.
def list_json_files():
    cwd = os.getcwd()
    return [file for file in os.listdir(cwd) if file.endswith('.json')]

#Reads a JSON file and returns its content.
def read_json_file(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading {filename}: {e}")
        return None

#Sends the JSON data to the Flask app and retrieves the response.
def make_request(json_data):
    url = "http://127.0.0.1:5000/select_game"  
    try:
        response = requests.post(url, json=json_data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the full JSON response
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None

#Main function for the CLI.
def main():
    json_files = list_json_files()
    if not json_files:
        print("No JSON files found in the current working directory.")
        return

    print("Available JSON files:")
    for idx, filename in enumerate(json_files, start=1):
        print(f"{idx}. {filename}")

    try:
        choice = int(input("\nSelect a JSON file by number: "))
        if choice < 1 or choice > len(json_files):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    selected_file = json_files[choice - 1]

    json_data = read_json_file(selected_file)

    print(f"Sending data from {selected_file} to the API...")
    response_data = make_request(json_data)
    print(response_data)
    if response_data:
        if "selected_game" in response_data:
            # Single game selected
            selected_game = response_data["selected_game"]
            if selected_game:
                print(f"\nSelected Game: {selected_game}")
            else:
                print("\nNo game selected.")
        elif "selected_games" in response_data:
            # Multiple games selected
            selected_games = response_data["selected_games"]
            print("\nSelected Games:")
            for user_id, game_name in selected_games.items():
                if game_name:
                    print(f"User {user_id}: {game_name}")
                else:
                    print(f"User {user_id}: No game selected.")
        else:
            print("\nUnexpected response format:", response_data)
    else:
        print("\nNo game selected or an error occurred.")

if __name__ == "__main__":
    main()
