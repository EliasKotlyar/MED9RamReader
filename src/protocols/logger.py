class Logger:
    LOG_KWP = 0x01
    LOG_TP20 = 0x02
    LOG_CAN = 0x03
    def log(self,*args):
        print(args)
        pass
    