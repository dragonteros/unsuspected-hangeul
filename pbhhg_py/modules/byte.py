"""Converts String and Number objects from and to Bytes objects."""
from collections import namedtuple

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import check


class Codec(AS.Function):
    CODEC_TBL = ['utf', 'unsigned', 'signed', 'float']

    def __init__(self, _strict, scheme, num_bytes, big_endian=None):
        self._strict = _strict

        check.check_type([scheme, num_bytes], AS.Number)
        self.scheme = self.CODEC_TBL[scheme.value]
        self.num_bytes = num_bytes.value
        self.big_endian = big_endian and big_endian.value
        self._codec = self._get_codec()

        self.endianness = ''
        if big_endian is not None:
            check.check_type(big_endian, AS.Boolean)
            self.endianness = 'big' if big_endian.value else 'little'

    def __repr__(self):
        return '<Codec(scheme={}, num_bytes={}, big_endian={})>'.format(
            self.scheme, self.num_bytes, self.big_endian)

    def __call__(self, argv):
        argv = self._strict(argv)
        return self._codec(*argv)

    def _get_codec(self):
        return {'utf': self._unicode_codec,
                'signed': self._integer_codec,
                'unsigned': self._integer_codec,
                'float': self._floating_point_codec}[self.scheme]

    def _unicode_codec(self, argument):
        encoding = 'utf-{}'.format(self.num_bytes * 8)
        if self.endianness:
            encoding = '{}-{}e'.format(encoding, self.endianness[0])
        check.check_type(argument, [AS.String, AS.Bytes])
        if isinstance(argument, AS.String):
            return AS.Bytes(argument.value.encode(encoding))
        if isinstance(argument, AS.Bytes):
            return AS.String(argument.value.decode(encoding))

    def _integer_codec(self, argument):
        endianness = self.endianness or 'little'
        signed = (self.scheme == 'signed')
        check.check_type(argument, [AS.Number, AS.Bytes])
        if isinstance(argument, AS.Number):
            return AS.Bytes(int.to_bytes(argument.value, self.num_bytes,
                                         endianness, signed=signed))
        elif isinstance(argument, AS.Bytes):
            return AS.Number(int.from_bytes(argument.value,
                                            endianness, signed=signed))

    def _floating_point_codec(self, argument):
        raise NotImplementedError()


def build_tbl(proc_functional, _strict):
    def _codec(argv):
        check.check_arity(argv, [2, 3])
        argv = _strict(argv)
        return Codec(_strict, *argv)

    return ('ㅂ', {
        'ㅂ': _codec,  # 바꾸기
    })
