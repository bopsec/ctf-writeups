import socket
import re
from collections import deque
from itertools import permutations

HOST = "legend-of-vexillum.ctf.cybertalent.no"
PORT = 2000
START_ROOM = "dungeon_prison"

GO_WORDS = [
    "door", "front", "back", "behind",
    "left", "right", "forward",
    "hall", "hallway", "corridor",
    "path", "room", "gate",
    "up", "down", "stairs", "ladder", "hatch",
    "north", "south", "east", "west",
    "eye opening", "opening", "hole", "passage", "passageway",
    "platform", "window", "trapdoor"
]

def send(room: str, items: list, command: str) -> str:
    items_str = ",".join(items) if items else ""
    msg = f"ROOM:{room};ITEMS:{items_str};COMMAND:{command};\n".encode()
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            s.sendall(msg)
            s.shutdown(socket.SHUT_WR)
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
        return data.decode("utf-8", errors="replace").strip()
    except Exception as e:
        return f"[ERROR: {e}]"


def extract_room(response: str):
    for part in response.split(";"):
        if part.startswith("ROOM:"):
            return part.split("ROOM:")[1]
    return None


def extract_secrets(text: str):
    hidden_rooms = {}
    hidden_items = []
    
    # The format is: SECRET:{'rooms': {...}, 'items': {...}};
    # Items format: 'items': {'coiled rod': <__main__.Item object at 0x...>}
    
    # Extract rooms
    rooms_match = re.search(r"'rooms':\s*\{([^}]*)\}", text)
    if rooms_match:
        room_content = rooms_match.group(1)
        room_pairs = re.findall(r"'([^']+)':\s*'([^']+)'", room_content)
        for name, room_id in room_pairs:
            hidden_rooms[name] = room_id
    
    # Extract items - look for item names before the colon
    items_match = re.search(r"'items':\s*\{([^}]*)\}", text)
    if items_match:
        items_content = items_match.group(1)
        # Match 'item name': <
        item_names = re.findall(r"'([^']+)':\s*<", items_content)
        hidden_items.extend(item_names)
    
    return hidden_rooms, hidden_items

def extract_items_from_description(text: str) -> list:
    items = []
    pattern = r"[Ii]n the room there is (?:a |an )?(.+?)\."
    match = re.search(pattern, text)
    if match:
        item_text = match.group(1)
        parts = re.split(r',\s*(?:and\s+)?|\s+and\s+', item_text)
        for part in parts:
            part = part.strip()
            part = re.sub(r'^(?:a|an)\s+', '', part)
            if part and len(part) > 1:
                items.append(part)
    return items

class GameExplorer:
    def __init__(self):
        self.rooms = {}
        self.room_exits = {}
        self.room_items = {}
        self.hidden_rooms = {}
        self.hidden_items = {}  # room -> [hidden items]
        self.inventory = []
        self.secrets = []
        self.all_known_items = set()  # All items we've discovered
    
    def explore_all_rooms(self):
        print(f"BFS Room Discovery")
        
        queue = deque([START_ROOM])
        visited = set([START_ROOM])
        
        while queue:
            room = queue.popleft()
            print(f"\n[.] Exploring: {room}")
            
            look = send(room, [], "look room")
            self.rooms[room] = look
            print(f"    Response: {look}...")
            
            # Check for SECRET leaks
            if "SECRET:" in look:
                print(f"	SECRET !!!!")
                h_rooms, h_items = extract_secrets(look)
                if h_rooms:
                    print(f"    [!] Hidden rooms: {h_rooms}")
                    self.hidden_rooms.update(h_rooms)
                    for exit_name, room_id in h_rooms.items():
                        if room_id not in visited:
                            visited.add(room_id)
                            queue.append(room_id)
                if h_items:
                    print(f"    [!] Hidden items in {room}: {h_items}")
                    self.hidden_items[room] = h_items
                    self.all_known_items.update(h_items)
            
            # Check for vexillum/flag
            if "vexillum" in look.lower() or "FLAG{" in look:
                print(f"\n{'!'*60}")
                print(f"[!!!] VEXILLUM/FLAG FOUND IN: {room}")
                print(look)
                print(f"{'!'*60}")
                self.secrets.append(("VEXILLUM", room, [], look))
            
            # Extract visible items
            items = extract_items_from_description(look)
            self.room_items[room] = items
            self.all_known_items.update(items)
            if items:
                print(f"    Visible items: {items}")
            
            # Find exits
            self.room_exits[room] = {}
            all_exits = GO_WORDS.copy()
            for exit_name in self.hidden_rooms.keys():
                if exit_name not in all_exits:
                    all_exits.append(exit_name)
            
            for word in all_exits:
                resp = send(room, [], f"go {word}")
                new_room = extract_room(resp)
                if new_room and new_room != room:
                    self.room_exits[room][word] = new_room
                    print(f"    [+] go {word} -> {new_room}")
                    if new_room not in visited:
                        visited.add(new_room)
                        queue.append(new_room)
        
        print(f"\n[+] Found {len(self.rooms)} rooms")
        print(f"[+] All known items: {self.all_known_items}")
    
    
    def run(self):
        self.explore_all_rooms()

if __name__ == "__main__":
    explorer = GameExplorer()
    explorer.run()