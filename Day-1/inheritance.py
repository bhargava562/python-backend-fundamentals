class User:                          # PARENT class
    def __init__(self, name: str, email: str) -> None:
        self.name  = name
        self.email = email

    def get_role(self) -> str:
        return "Regular User"

    def describe(self) -> str:
        return f"[{self.get_role()}] {self.name} — {self.email}"


class AdminUser(User):              # CHILD class — inherits User
    def __init__(self, name: str, email: str,
                 permissions: list[str]) -> None:
        super().__init__(name, email)    # run parent's __init__ first
        self.permissions = permissions

    def get_role(self) -> str:          # OVERRIDE parent method
        return "Admin"

    def can_do(self, action: str) -> bool:
        return action in self.permissions


class GuestUser(User):              # Another CHILD class
    def get_role(self) -> str:
        return "Guest (read-only)"


# ── Polymorphism: same method, different output ──
users = [
    User("Ravi", "ravi@mail.com"),
    AdminUser("Meena", "meena@mail.com", ["delete", "ban"]),
    GuestUser("Kumar", "kumar@mail.com"),
]

for u in users:
    print(u.describe())          # same call, different results

admin = users[1]
print(admin.can_do("delete"))  # True
print(admin.can_do("refund"))  # False
print(isinstance(admin, User))  # True — Admin IS-A User