from arbiterPUF import ArbiterPUF


class XorPUF:
    _pufs = []

    def __init__(self,n,npufs):
        self._pufs = [ ArbiterPUF(n) for _ in range(npufs)]

    def get_output(self,chall):
        outputs = [p.get_output(chall) for p in self._pufs]
        return reduce((lambda x, y: x ^ y),outputs)
