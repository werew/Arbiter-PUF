from arbiterPUF import ArbiterPUF


puf = ArbiterPUF(10)

puf.set_challenge([0,0,0,0,0,0,0,0,0,0])
print puf.get_output()

puf.set_challenge([0,0,1,0,1,0,0,0,0,0])
print puf.get_output()

puf.set_challenge([1,0,0,0,1,0,0,0,1,0])
print puf.get_output()
