from time import sleep
from RPi import GPIO
import smbus

GPIO.setmode(GPIO.BCM)

i2c = smbus.SMBus(1)

class LCD:
   def __init__(self, i2c_addr = 0x27, lcd_width = 16, lcd_chr = 1, lcd_cmd = 0, lcd_lines = [0x80, 0xC0], lcd_backlight = 0b0000_1000, enable = 0b0000_0100, e_pulse = 0.0002, e_delay = 0.0002) -> None:
      self.__i2c_addr = i2c_addr
      self.__lcd_width = lcd_width
      self.__lcd_chr = lcd_chr
      self.__lcd_cmd = lcd_cmd
      self.__lcd_lines = lcd_lines
      self.__lcd_backlight = lcd_backlight
      self.__enable = enable
      self.__e_pulse = e_pulse
      self.__e_delay = e_delay

   @property
   def lcd_width(self):
      return self.__lcd_width

   def init(self):
      # spamming
      self.send_byte_with_e_toggle(0b0011_0000)
      self.send_byte_with_e_toggle(0b0011_0000)

      self.send_byte_with_e_toggle(0b0010_0000) # put into 4bit-mode

      self.send_instruction(0x28) # 0010_1000 Data length, number of lines, font size
      self.send_instruction(0x06) # 000110 Cursor move direction
      self.send_instruction(0x0C) # 0000_1100 Display On, Cursor Off, Blink Off

   def send_instruction(self, byte):
      self.set_data_bits(byte, self.__lcd_cmd)
      sleep(0.001)

   def send_character(self, byte):
      self.set_data_bits(byte, self.__lcd_chr)
   
   def set_data_bits(self, value, mode):
      MSNibble = value & 0xf0
      LSNibble = (value & 0x0f) << 4

      MSNibble_byte = MSNibble | self.__lcd_backlight | mode
      LSNibble_byte = LSNibble | self.__lcd_backlight | mode
   
      sleep(self.__e_delay)
      i2c.write_byte(self.__i2c_addr, MSNibble_byte | self.__enable) # send MSNibble with E bit high, BT bit high and RS bit according to # “mode” and little delay
      sleep(self.__e_pulse)
      i2c.write_byte(self.__i2c_addr, MSNibble_byte & ~self.__enable) # send MSNibble with E bit low, BT bit high and RS bit according to # “mode” and little delay
      sleep(self.__e_delay)
      i2c.write_byte(self.__i2c_addr, LSNibble_byte | self.__enable) # send LSNibble with E bit high, BT bit high and RS bit according to # “mode” and little delay
      sleep(self.__e_pulse)
      i2c.write_byte(self.__i2c_addr, LSNibble_byte & ~self.__enable) # send LSNibble with E bit low, BT bit high and RS bit according to # “mode” and little delay
      sleep(self.__e_delay)

   def clear(self):
      self.send_instruction(0x01) # 0000_0001 Clear display

   def send_byte_with_e_toggle(self, bits):
      # Toggle enable
      sleep(self.__e_delay)
      # write data to i2c with E bit HIGH
      # OR operator will turn all bits to 0 except our e bit that we put high
      bits_high = bits | self.__enable
      i2c.write_byte(self.__i2c_addr, bits_high)
      sleep(self.__e_pulse)
      # write data to i2c with E bit LOW
      # AND operator will turn all bits to 1 except our e bit that we put low
      # ~ bitwise negation
      bits_low = bits & ~self.__enable
      i2c.write_byte(self.__i2c_addr, bits_low)
      sleep(self.__e_delay)

   def send_string(self, message, line):
      # by default we print on line 1
      instruction = self.__lcd_lines[0]

      if line > 0 and line < 3:
         instruction = self.__lcd_lines[line-1]

      if len(message) != self.__lcd_width:
         print(f'The message ({message}) length is {len(message)} not {self.__lcd_width}!')


      self.send_instruction(instruction)

      for char in message:
         # get decimal of each symbol
         self.send_character(ord(char))