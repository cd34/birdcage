class Phrase(object):
    def __init__(self, *args):
        self.args = args

    def generate(self, **kwargs):
        delim = kwargs.get('delimiter', ' ')
        phrase_length = kwargs.get('length', None)
        
        max_message = delim.join([x.maxlen for x in self.args])
        if not phrase_length or len(max_message) <= phrase_length:
            return max_message

        lens = filter(None, [None if x.trim else x.lens for x in self.args])
        len_trims = filter(None, [x.min_length if x.trim else None \
            for x in self.args])

        #trim_length = sum(len_trims) / len(len_trims)
        max_length = phrase_length - len(delim) * len(self.args) - \
            sum(len_trims)

        if max_length < 0:
            raise ValueError
            #raise Exception(ValueError, \
            #    'Can\'t squeeze, length too short')

        current_len = self.non_trim_length(self.args)
        num_lens = len(lens)
        len_count = 0

        while current_len < max_length and len_count < num_lens:
            for x in self.args:
                try:
                     if x.next_len - x.cur_len + current_len < max_length:
                         x.select_next()
                         current_len = self.non_trim_length(self.args)
                         len_count = 0
                except:
                     len_count += 1

        final_lens = sum([0 if x.trim else x.cur_len for x in self.args])
        trim_length = (phrase_length - len(delim) * len(self.args) - \
            final_lens + 1) / len(len_trims)
        return delim.join([x.cur_text(trim_length=trim_length) \
            for x in self.args])

    def non_trim_length(self, phrase):
        length = 0
        for x in phrase:
            if not x.trim:
                length += len(x.items[x.selected])    
        return length

class Text(object):
    # trim should only allow one item

    def __init__(self, *args, **kwargs):
        #self.priority = kwargs.get('priority', 1)

        self.items = sorted(map(unicode, args), key=len)
        self.trim = kwargs.get('trim', False)
        self.trim_delim = kwargs.get('trim_delim', '...')
        self.min_length = kwargs.get('min_length', 10)
        if self.trim:
            self.min_length += len(self.trim_delim)
        self.maxlen = max(self.items, key=len)
        self.selected = 0

    @property
    def lens(self):
        return map(len, self.items)

    def select(self, selected):
        if selected < len(self.items) and selected >= 0:
            self.selected = selected
        else:
            raise IndexError

    def cur_text(self, **kwargs):
        trim_length = kwargs.get('trim_length', None)

        if trim_length and self.trim:
            append_elipses = ''
            if trim_length <= len(self.items[self.selected]):
                trim_length -= 3
                append_elipses = '...'
            return self.items[self.selected][:trim_length] + append_elipses
        return self.items[self.selected]

    @property
    def cur_len(self):
        return len(self.items[self.selected])

    @property
    def next_len(self):
        if self.selected < len(self.items) - 1:
            return len(self.items[self.selected+1])
        else:
            return None

    def select_next(self):
        if self.selected < len(self.items) - 1:
            self.selected += 1
        else:
            raise IndexError
