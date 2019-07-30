"""Converts String and Number objects from and to Bytes objects."""
from pbhhg_py import abstract_syntax as AS
from pbhhg_py import check

Bytes = namedtuple('Bytes', 'value')


class Codec:  # import ???.???하면 `Codec`(생성자)을 저장해두기
    def __init__(self, scheme, num_bytes, endianness=AS.Number(0)):
        check.check_type([scheme, num_bytes, endianness], AS.Number)
        _codec_tbl = ['utf', 'signed', 'unsigned', 'float']
        self.scheme = _codec_tbl[scheme.value]
        self.num_bytes = num_bytes.value
        self.endianness = {-1: 'little', 0: '', 1: 'big'}[endianness.value]
        self._codec = self._get_codec()

    def __call__(self, argument):
        return self._codec(argument)

    def _get_codec(self):
        return {'utf': self._unicode_codec,
                'signed': self._integer_codec,
                'unsigned': self._integer_codec,
                'float': self._floating_point_codec}[self.scheme]

    def _unicode_codec(self, argument):
        encoding = 'utf-{}'.format(self.num_bytes * 8)
        if self.endianness:
            encoding = '{}-{}e'.format(encoding, self.endianness[0])
        if isinstance(argument, AS.String):
            return argument.value.encode(encoding)
        if isinstance(argument, AS.Bytes):
            return argument.value.decode(encoding)
        raise ValueError('Unicode Converter Expected String or Bytes '
                         'but received: ' + argument)

    def _integer_codec(self, argument):  # TODO: Allow for multiple numbers
        if isinstance(argument, AS.Number):
            fn = int.to_bytes
        elif isinstance(argument, AS.Bytes):
            fn = int.from_bytes
        else:
            raise ValueError('Integer Converter Expected Number or Bytes '
                             'but received: ' + argument)
        endianness = self.endianness or 'little'
        signed = (self.scheme == 'signed')
        return fn(argument.value, self.num_bytes, endianness, signed=signed)

    def _floating_point_codec(self, argument):
        raise NotImplementedError()


if __name__ == '__main__':
    c = Codec('utf', 1)
    print(c(AS.String('A가')))
