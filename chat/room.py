import dotenv

ROOMS = []
ROOM_NAMES = ["Red", "Blue", "Green", "Yellow", "Black"]

env = dotenv.dotenv_values("../dev.env")
PASSPHRASE = env["SECRET"]
MAX_GUESTS_PER_ROOM = int(env["MAX_GUESTS_PER_ROOM"])


class Room:
    def __init__(self, passphrase=PASSPHRASE):
        self.passphrase = passphrase  # TODO validate passphrase, add hash
        self.users = set()
        self.name = self._get_available_name()

    def add_user(self, user_id):
        if len(self.users) >= MAX_GUESTS_PER_ROOM:
            raise Exception("Room is full")
        self.users.add(user_id)

    def remove_user(self, user_id):
        try:
            self.users.remove(user_id)
        except KeyError:
            print(f"User {user_id} not in room")

    def __repr__(self):
        return f"Room(name={self.name}, passphrase={self.passphrase}, users={self.users})"

    def _get_available_name(self):
        available_names = set(ROOM_NAMES) - {room.name for room in ROOMS}
        if len(available_names) > 0:
            return available_names.pop()
        raise Exception("No rooms available")

    @classmethod
    def create_room(cls, passphrase):
        room = cls(passphrase)
        ROOMS.append(room)
        return room

    @classmethod
    def destroy_room(cls, instance):
        for room in ROOMS:
            if room.name == instance.name:
                ROOMS.remove(room)
                del instance
                return


