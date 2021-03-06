#!/usr/bin/env python

import os

import Pyro.core # Pyro 3.8.1

fakeIO = True

if fakeIO:
    from pwm import FakeOmapPwm as Pwm
    from adc import FakeAdc as Adc
    from gpio import FakeGpio as Gpio
else:
    from pwm import OmapPwm as Pwm
    from adc import Adc as Adc
    from gpio import Gpio as Gpio

class Remote(Pyro.core.ObjBase): 
    """Creates a pretty useless class that just contains an adc (self.adc) and pwm (self.pwm)"""
    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
        self.adc = Adc()#adc.Adc()
        self.pwm = Pwm()#pwm.OmapPwm()
        self.gpio = Gpio()#gpio.Gpio()
    def ping(self):
        return 1
    # pwm
    def pwm_enable(self):
        self.pwm.enable()
    def pwm_disable(self):
        self.pwm.disable()
    def pwm_set_load(self, value):
        self.pwm.set_load(value)
    def pwm_set_match(self, value):
        self.pwm.set_match(value)
    def pwm_set_duty(self, duty):
        self.pwm.set_duty(duty)
    # adc
    def adc_read(self):
        return self.adc.read()
    def adc_set_pin(self, pin, average):
        self.adc.set_pin(pin, average)
    def adc_raw_read(self):
        return self.adc.raw_read()
    def adc_read_pin(pin, average):
        return self.adc.read_pin(pin, average)
    # gpio
    def gpio_set_level(self, level):
        self.gpio.set_level(level)
    def gpio_set_high(self):
        self.gpio.set_high()
    def gpio_set_low(self):
        self.gpio.set_low()

if __name__ == "__main__":
    Pyro.core.initServer()
    #daemon=Pyro.core.Daemon(host=sys.argv[1])
    daemon=Pyro.core.Daemon(host=os.uname()[1])
    uri=daemon.connect(Remote(),"remote")
    
    print "The daemon runs on port:",daemon.port
    print "The object's uri is:",uri
    
    daemon.requestLoop()
