class MCU:
    def __init__(self):
        self.state = {}
    
    def get_mcu(self):
        return self.state

    def increment_mcu(self, incre, weight):
        for k1 in incre:
            k1_abbrevation = k1[0]
            
            if type(incre[k1]) == int:
                if not k1_abbrevation in self.state:
                    self.state[k1_abbrevation] = 0
                self.state[k1_abbrevation] += incre[k1] * weight
            else:
                if not k1_abbrevation in self.state:
                    self.state[k1_abbrevation] = {}
                for k2 in incre[k1]:
                    k2_abbrevation = k2[0]
                    if not k2_abbrevation in self.state[k1_abbrevation]:
                        self.state[k1_abbrevation][k2_abbrevation] = 0
                    self.state[k1_abbrevation][k2_abbrevation] += incre[k1][k2] * weight