import sys # noqa

'''
# number of drones
nb_drones: 4

# start and end
start_hub: base 0 0
end_hub: goal 10 10

# normal hubs
hub: A 1 1
hub: B 2 2
hub: C 3 3

# special hubs
hub: fastlane 4 4 [zone=priority]
hub: tunnel 5 5 [zone=restricted max_drones=2]
hub: danger 6 6 [zone=blocked]

# connections
connection: base-A
connection: A-B
connection: B-C
connection: C-fastlane
connection: fastlane-goal

# alternative path
connection: B-tunnel
connection: tunnel-goal

# blocked path (should never be used)
connection: C-danger
connection: danger-goal
'''
class Parsing:

    def __init__(self):
        pass

    def check_map(self):
        if len(sys.argv) != 2:
            print("[ERROR] : ADD MAPE FILE")
            exit(1)
        try:
            with open(sys.argv[1], 'r') as f:
                print(self.check_parameters(f.readlines()))
        except FileNotFoundError:
            print("[ERROR] : MAPE FILE NOT FOUND")
            exit(1)

    def check_parameters(self, data_lines: list[str]):
        data = {
            "hubs": [],
            "connections": []
        }

        for line in data_lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if not parts:
                continue

            command = parts[0].lower()

            if command == "nb_drones:":
                data["nb_drones"] = int(parts[1])

            elif command == "start_hub":
                if len(parts) < 4:
                    print("[ERROR] : MISSING ARGUMENTS FOR START HUB")
                    exit(1)
                hub_data = {
                    "type": "start",
                    "name": parts[1],
                    "x": int(parts[2]),
                    "y": int(parts[3])
                }
                # Parse optional zone parameters
                if len(parts) > 4:
                    self._parse_options(hub_data, parts[4:])
                data["start_hub"] = hub_data
                
            # elif command == "end_hub:":
            #     if len(parts) < 4:
            #         print("[ERROR] : MISSING ARGUMENTS FOR END HUB")
            #         exit(1)
            #     hub_data = {
            #         "type": "end",
            #         "name": parts[1],
            #         "x": int(parts[2]),
            #         "y": int(parts[3])
            #     }
            #     # Parse optional zone parameters
            #     if len(parts) > 4:
            #         self._parse_options(hub_data, parts[4:])
            #     data["end_hub"] = hub_data
                
            # elif command == "hub:":
            #     if len(parts) < 4:
            #         print("[ERROR] : MISSING ARGUMENTS FOR HUB")
            #         exit(1)
            #     hub_data = {
            #         "type": "normal",
            #         "name": parts[1],
            #         "x": int(parts[2]),
            #         "y": int(parts[3])
            #     }
            #     # Parse optional zone parameters
            #     if len(parts) > 4:
            #         self._parse_options(hub_data, parts[4:])
            #     data["hubs"].append(hub_data)
                
            # elif command == "connection:":
            #     if len(parts) < 2:
            #         print("[ERROR] : MISSING ARGUMENTS FOR CONNECTION")
            #         exit(1)
            #     connection = parts[1].split("-")
            #     if len(connection) != 2:
            #         print("[ERROR] : INVALID CONNECTION FORMAT")
            #         exit(1)
            #     data["connections"].append({
            #         "from": connection[0],
            #         "to": connection[1]
            #     })
                
        return data
    
    def _parse_options(self, hub_data: dict, options: list[str]):
        """Parse optional parameters in bracket notation."""
        for opt in options:
            opt = opt.strip("[]")
            if "=" in opt:
                key, value = opt.split("=", 1)
                hub_data[key.strip()] = value.strip()


if __name__ == "__main__":
    a = Parsing()
    a.check_map()
