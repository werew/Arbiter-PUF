import random

class Stage:
    _delay_out_a = 0.
    _delay_out_b = 0.
    _selector = 0

    def __init__(self,delay_a,delay_b):
        self._delay_out_a = delay_a
        self._delay_out_b = delay_b

    def set_selector(self,s):
        self._selector = s

    def get_output(self,delay_in_a, delay_in_b):
        if self._selector == 0:
            return (delay_in_a  + self._delay_out_a, 
                    delay_in_b  + self._delay_out_b)
        else:
            return (delay_in_b  + self._delay_out_a, 
                    delay_in_a  + self._delay_out_b)

class ArbiterPUF:
    _stages = []

    def __init__(self,n):
        for _ in range(n):
            self._stages.append(
                  Stage(random.random(),
                        random.random())
            )

    def get_output(self,chall):
        # Set challenge
        for stage,bit in zip(self._stages,chall):
            stage.set_selector(bit)

        # Compute output
        delay = (0,0)
        for s in self._stages:
            delay = s.get_output(delay[0],delay[1])

        if delay[0] < delay[1]:
            return 0
        else:
            return 1
        
    
