from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Route to select a random game from user(s) library based on given filters
@app.route('/select_game', methods=['POST'])
def select_game():
    data = request.get_json()
    users = data.get("users", [])  # List of users with their game libraries
    filters = data.get("filters", {})  # Filters to apply on the game selection
    options = data.get("options", {})  # Additional options for game selection

    # Options
    no_filter = options.get("no_filter", False)  # If True, bypass all filters
    find_common_games = options.get("find_common_games", False)  # If True, find games common to all users
    tags_filter = filters.get("tags", [])  # Tags to filter games by

    # If only one user is provided
    if len(users) == 1:
        user_library = users[0].get("library", [])  # Get user's game library
        # Filter games based on tags or no_filter option
        filtered_games = [
            game for game in user_library
            if no_filter or not tags_filter or any(tag in game["tags"] for tag in tags_filter)
        ]
        # Select a random game from the filtered list
        selected_game = random.choice(filtered_games) if filtered_games else None
        return jsonify({"selected_game": selected_game["name"] if selected_game else None})
    
    # If multiple users are provided
    elif len(users) > 1:
        # If the option is to find games common to all users
        if find_common_games:
            # Find common games by appid across all users
            common_games = set(game["appid"] for game in users[0].get("library", []))
            for user in users[1:]:
                common_games.intersection_update(game["appid"] for game in user.get("library", []))
            # Filter the common games based on tags or no_filter option
            common_game_list = [
                game for game in users[0].get("library", [])
                if game["appid"] in common_games and (no_filter or not tags_filter or any(tag in game["tags"] for tag in tags_filter))
            ]
            # Select a random game from the common games
            if common_game_list:
                selected_game = random.choice(common_game_list)
                return jsonify({"selected_game": selected_game["name"]})
            else:
                return jsonify({"selected_game": None})
        # If not finding common games, select a game for each user individually
        else:
            selected_games = {}
            for user in users:
                user_library = user.get("library", [])  # Get user's game library
                # Filter games based on tags or no_filter option
                filtered_games = [
                    game for game in user_library
                    if no_filter or not tags_filter or any(tag in game["tags"] for tag in tags_filter)
                ]
                # Select a random game from the filtered list for the user
                if filtered_games:
                    selected_games[user["user_id"]] = random.choice(filtered_games)["name"]
                else:
                    selected_games[user["user_id"]] = None
            return jsonify({"selected_games": selected_games})

    # If no users 
    return jsonify({"selected_game": None})

if __name__ == '__main__':
    app.run(debug=True)
