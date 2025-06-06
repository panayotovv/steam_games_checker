import requests


def get_game_appids(api_key, steam_id):
        games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
        games_response = requests.get(games_url)

        if games_response.status_code == 200:
            data = games_response.json()
            if 'games' in data['response']:
                return {game['appid']: round(game['playtime_forever'] / 60, 2) for game in data['response']['games']}
            else:
                print("No games found or profile is private.")
                return []
        else:
            print(f"Error fetching games: {games_response.status_code}")
            return []

def get_game_names(appids):
    game_names = []

    for game_id, playtime in appids.items():
        url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            appid = str(game_id)
            if appid in data and 'data' in data[appid]:
                game_name = data[appid]['data'].get('name')
                if game_name:
                     game_names.append(f"{game_name} with {playtime} hours on the game")
        else:
            print(f"Error fetching game details for {game_id}: {response.status_code}")

    return game_names



def main():
    api_key = "1B6F7DB79C1DD8E93E8D251F1B3E1B1E"

    while True:
        profile_input = input("Enter SteamID64 or vanity URL/name: ").strip()

        if profile_input.isdigit() and len(profile_input) == 17:
            steam_id = profile_input
        else:
            resolve_url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={api_key}&vanityurl={profile_input}"
            response = requests.get(resolve_url).json()
            if response["response"]["success"] == 1:
                steam_id = response["response"]["steamid"]
            else:
                print("Error resolving vanity URL.")
                return

        game_ids = get_game_appids(api_key, steam_id)

        if game_ids:
            game_names = get_game_names(game_ids)

            print("\nOwned Games:")
            print('\n'.join(game_names))
        else:
            print("No games to display.")

        choice = input("\n1. Check another user\n2. Exit\nChoose an option: ")
        if choice == "1":
            continue
        elif choice == "2":
            break

if __name__ == "__main__":
    main()
