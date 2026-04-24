from datetime import datetime

class User:
    """
    Blueprint for a User in our system.
    Every user has a name, email, and a joined date.
    """

    # Class attribute — shared across ALL User objects
    total_users: int = 0

    def __init__(self, name: str, email: str) -> None:
        # Instance attributes — unique to each user object
        self.name      = name
        self.email     = email
        self.joined_at = datetime.now()
        self.is_active = True
        User.total_users += 1   # increment shared counter

    def greet(self) -> str:
        # Instance method — acts on THIS specific user
        return f"Hi, I am {self.name}! Joined on {self.joined_at.strftime('%d %b %Y')}."

    def deactivate(self) -> None:
        self.is_active = False
        print(f"{self.name}'s account has been deactivated.")

    def __repr__(self) -> str:
        # Controls what print(user) shows — useful for debugging
        return f"User(name={self.name!r}, active={self.is_active})"


# ── Creating objects (instances) from the class ──
user1 = User("Aravind", "aravind@mail.com")
user2 = User("Priya",   "priya@mail.com")

print(user1.greet())
print(user2.greet())
print(f"Total users registered: {User.total_users}")

user1.deactivate()
print(user1)         # calls __repr__