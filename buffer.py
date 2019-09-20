#!/usr/bin/env python3

class Buffer(bytearray):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = len(self)
        self._have_new_data = True
        self._asked_words = []

    def __str__(self):
        return self.decode()

    def _transform(self, buff):
        if type(buff) == str:
            buff = buff.encode()

        return buff

    def extend(self, buff):
        super().extend(buff)

        self.len = len(self)
        self._have_new_data = True

    def consume(self, n):
        # too lazy to avoid race condition
        if self.len < n:
            n = self.len

        consumed = self[:n].decode()
        del self[:n]

        self.len = len(self)

        return consumed

    def consume_until(self, s):
        s = self._transform(s)

        is_asked_word = s in self._asked_words
        if is_asked_word and not self._have_new_data:
            return None


        l = len(s)

        ind = super().find(s)

        if ind == -1:
            # Searched all the data
            self._have_new_data = False

            if not is_asked_word:
                self._asked_words.append(s)

            return None

        ind += l

        consumed = self[:ind].decode()
        del self[:ind]

        self.len = len(self)

        if is_asked_word:
            del self._asked_words[self._asked_words.index(s)]

        return consumed

    def get(self, n=0):
        if n == 0:
            n = self.len

        return self[:n].decode()
