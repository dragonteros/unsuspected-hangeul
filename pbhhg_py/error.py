
class UnsuspectedHangeulError(Exception):
    def __init__(self, argv) -> None:
        super().__init__('평범한 한글 예외')
        self.argv = argv
