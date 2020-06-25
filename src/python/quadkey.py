import numpy

class Quadkey:
    def __init__(self, key):
        self._key = key
        self._base = int(key, 4)
        self._level = len(key)
        self._odd_bits, self._even_bits = self._parse_bit(self._base, self._level)

    @property
    def key(self):
        return self._key

    @property
    def level(self):
        return self._level

    def to_binstr(self):
        digits = self._level * 2 + 2
        fstr = r'{:#0%2db}' % digits  # e.g. '{:010b}'
        return fstr.format(self._base)

    def offset(self, h, v):
        o = self._odd_bits  + h
        e = self._even_bits + v
        ret = self._combine_bit(o, e, self._level)
        fstr = r'{:0>%ds}' % self._level  # e.g. '{:0>4s}'
        return fstr.format(numpy.base_repr(ret, base=4))

    @staticmethod
    def _parse_bit(target, level):
        """偶数ビットと奇数ビットに分ける"""
        odd = even = 0
        for i in range(level):
            odd  |= ((target>>(2 * i)) & 1) << i
            even |= ((target>>(2 * i + 1)) & 1) << i

        odd  &= (1<<level)-1
        even &= (1<<level)-1
        return odd, even

    @staticmethod
    def _combine_bit(odd, even, level):
        """分割された偶数ビットと奇数ビットを統合する"""
        target = 0

        for i in range(level):
            target |= ((odd>>i) & 1) << (2 * i)
            target |= ((even>>i) & 1) << (2 * i + 1)

        target &= (1<<(level<<1))-1
        return target

if __name__ == '__main__':
    qh = [
        ( (0,  0), '1010' ),
        ( (0,  1), '1012' ),
        ( (0,  2), '1030' ),
        ( (0,  3), '1032' ),
        ( (0,  4), '1210' ),
        ( (0,  5), '1212' ),
        ( (0,  6), '1230' ),
        ( (0,  7), '1232' ),
        ( (0,  8), '3010' ),
        ( (0,  9), '3012' ),
        ( (0, 10), '3030' ),
        ( (0, 11), '3032' ),
        ( (0, 12), '3210' ),
        ( (0, 13), '3212' ),
        ( (0, 14), '3230' ),
        ( (0, 15), '3232' ),
    ]

    base = qh[0][1]
    for offs, q in qh:
        c = Quadkey(base)
        q2 = Quadkey(c.offset(*offs))
        print(q2.key, q2.to_binstr())
