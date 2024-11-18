
# randomGameMicroservice

# How To Send Data
1. Install dependiences, if needed.
```pip install flask```
2. Run the program
```python api.py```
4. POST api call to http://127.0.0.1:5000/select_game
5. Send JSON File, like ```requests.post("http://127.0.0.1:5000/select_game", json=json_data)```

Example JSON:
```
{
    "users": [
      {
        "user_id": "user_1",
        "library": [
          {
            "appid": 101,
            "name": "Game A",
            "tags": ["Action", "Multiplayer"]
          },
          {
            "appid": 102,
            "name": "Game B",
            "tags": ["Adventure", "Singleplayer"]
          }
        ]
      },
      {
        "user_id": "user_2",
        "library": [
          {
            "appid": 101,
            "name": "Game A",
            "tags": ["Action", "Multiplayer"]
          },
          {
            "appid": 103,
            "name": "Game C",
            "tags": ["Puzzle", "Singleplayer"]
          },
          {
            "appid": 102,
            "name": "Game B",
            "tags": ["Adventure", "Singleplayer"]
          }
        ]
      }
    ],
    "filters": {
      "tags": ["Singleplayer"]
    },
    "options": {
      "no_filter": false,
      "find_common_games": true
    }
  }
```

Paramters:
* tags: Filter based on genre
* no_filter: Whether to filter random games by tags
* find_common_games: If true, responds back one matching game. If false, two selected games will be returned. 


# How to Recieve Data

1. Return the responses JSON, like ```response.json()```
2. Parse Response data : 
	* When a single game is selected, it will return a single game.
	```{'selected_game': 'Game B'}```
	* When find_common_games is false, multiple games will be returned.
	```{'selected_games': {'user_1': 'Game B', 'user_2': 'Game C'}}```
	
# UML Diagram

![UML Diagram](https://github.com/Mrepp/randomGameMicroservice/blob/main/uml.png)
