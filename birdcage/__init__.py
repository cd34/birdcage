class Phrase:
    def __init__(self, *args):
        self.args = args

    def generate(self, **kwargs):
        delim = kwargs.get('delimiter', ' ')
        phrase_length = kwargs.get('length', None)

        for x in self.args:
            x.selected = 0

        max_message = delim.join([x.maxlen for x in self.args])
        if not phrase_length or len(max_message) <= phrase_length:
            return max_message

        len_trims = [x.min_length for x in self.args if x.trim]
        num_non_trim = sum(1 for x in self.args if not x.trim)
        delim_count = max(len(self.args) - 1, 0)

        max_length = (phrase_length - len(delim) * delim_count
                      - sum(len_trims))
        current_len = self._non_trim_length()

        if max_length < 0 or current_len > max_length:
            raise ValueError(
                f"length {phrase_length} is too short to fit the phrase")
        len_count = 0

        while current_len < max_length and len_count < num_non_trim:
            for x in self.args:
                if x.next_len is None:
                    len_count += 1
                elif x.next_len - x.cur_len + current_len <= max_length:
                    x.select_next()
                    current_len = self._non_trim_length()
                    len_count = 0
                else:
                    len_count += 1

        if len_trims:
            final_lens = sum(0 if x.trim else x.cur_len for x in self.args)
            trim_length = ((phrase_length - len(delim) * delim_count
                            - final_lens) // len(len_trims))
        else:
            trim_length = None

        return delim.join([x.cur_text(trim_length=trim_length)
                           for x in self.args])

    def _non_trim_length(self):
        length = 0
        for x in self.args:
            if not x.trim:
                length += len(x.items[x.selected])
        return length


class Text:
    def __init__(self, *args, **kwargs):
        self.items = sorted(map(str, args), key=len)
        self.trim = kwargs.get('trim', False)
        self.trim_delim = kwargs.get('trim_delim', '...')
        self.min_length = kwargs.get('min_length', 10)
        if self.trim:
            self.min_length += len(self.trim_delim)
        self.maxlen = max(self.items, key=len)
        self.selected = 0

    @property
    def lens(self):
        return list(map(len, self.items))

    def select(self, selected):
        if 0 <= selected < len(self.items):
            self.selected = selected
        else:
            raise IndexError

    def cur_text(self, **kwargs):
        trim_length = kwargs.get('trim_length', None)

        if trim_length and self.trim:
            text = self.items[self.selected]
            if trim_length < len(text):
                trim_length -= len(self.trim_delim)
                return text[:trim_length] + self.trim_delim
            return text
        return self.items[self.selected]

    @property
    def cur_len(self):
        return len(self.items[self.selected])

    @property
    def next_len(self):
        if self.selected < len(self.items) - 1:
            return len(self.items[self.selected + 1])
        else:
            return None

    def select_next(self):
        if self.selected < len(self.items) - 1:
            self.selected += 1
        else:
            raise IndexError
