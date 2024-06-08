import sqlite3


class database():
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    def check_user(self, user_id) -> bool:
        with self.connection:
            result = self.cursor.execute('SELECT `user_id` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id: int) -> None:
        with self.connection:
            self.cursor.execute('INSERT INTO `users` (`user_id`) VALUES (?)', (user_id,))
            print('success add user')

    def add_deeplink(self, user_id, deeplink: str) -> None:
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `deeplink` = ? WHERE `user_id` = ?', (deeplink, user_id,))

    def add_referral(self, user_id, referral: int) -> None:
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `referral` = ? WHERE `user_id` = ?', (referral, user_id,))

    def add_referrals(self, user_id, refferals):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `referrals` = `referrals` + ? WHERE `user_id` = ?', (refferals, user_id,))

    def get_users(self) -> list[tuple[int]]:
        with self.connection:
            result = self.cursor.execute('SELECT `user_id` FROM `users`').fetchall()
            print(result)
            print(type(result[0]))
        return result

    def get_data(self, user_id: int) -> str | bool:
        with self.connection:
            result = self.cursor.execute('SELECT `datetime` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchmany(1)
            return str(result[0][0]) if bool(result[0][0]) else False

    def get_deeplink(self, user_id: int) -> str:
        with self.connection:
            result = self.cursor.execute('SELECT `deeplink` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchmany(1)
            return result[0][0]

    def get_referral(self, user_id) -> int:
        with self.connection:
            result = self.cursor.execute('SELECT `referral` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchmany(1)
            return int(result[0][0])

    def get_referrals(self, user_id) -> int:
        with self.connection:
            result = self.cursor.execute('SELECT `referrals` FROM `users` WHERE `user_id` = ?', (user_id, )).fetchmany(1)
            return int(result[0][0])

    def get_paid_users(self) -> int:
        with self.connection:
            result = self.cursor.execute('SELECT COUNT(`user_id`) FROM `users` WHERE `generation` > 0').fetchmany(1)
        return int(result[0][0])

    def get_free_users(self) -> int:
        with self.connection:
            result = self.cursor.execute('SELECT COUNT(`user_id`) FROM `users` WHERE `generation` = 0').fetchmany(1)
        return int(result[0][0])

    def update_data(self, data: str | None, user_id: int):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `datetime` = ? WHERE `user_id` = ?', (data, user_id,))

    def get_generates(self, user_id: int) -> int:
        with self.connection:
            result = self.cursor.execute('SELECT `generation` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchmany(1)
            return int(result[0][0])

    def update_generates(self, user_id, generates: int) -> None:
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `generation` = `generation` + ? WHERE `user_id` = ?', (generates, user_id,))

    def delete_data(self):
        with self.connection:
            self.cursor.execute('DELETE FROM `users`')

