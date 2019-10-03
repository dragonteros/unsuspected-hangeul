from test.test_base import TestBase


class TestParse(TestBase):
    def test_unicode(self):
        _test = self._assert_execute
        _test('나랏〮말〯ᄊᆞ미〮', '19737')
        _test('수〯ᄫᅵ〮니겨〮날〮로〮ᄡᅮ〮메〮', '81105006')
        _test('부ᇙ〮샤ᇰ류ᇢ통', '-1269')
        _test('ᅀᅵᆼ즁부ᇙ〮득〮신끵쪄ᇰ〮쟝〯', '-16541054')
        _test('신졩〮ᅀᅵᆼ〮씹〮바ᇙ〮ᄍᆞᆼ〮', '-253374')
        _test('ᄉᆡ〯미〮기픈〮므〮른〮ᄀᆞ〮ᄆᆞ래〮', '58837542')
        _test('ￓﾩￜﾤￂﾩￂﾡￂﾲￂﾪﾡￌﾡￌﾲﾧￂ', '2818691275')
