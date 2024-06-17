import threading
import queue
from LCD import LCD

# Bluez gatt uart service (SERVER)
from bluetooth_uart_server.bluetooth_uart_server import ble_gatt_uart_loop

def main(lcd: LCD):
    # Initialise display
    lcd.init()

    i = 0
    rx_q = queue.Queue()
    tx_q = queue.Queue()
    device_name = "mykyta-rapsi" # TODO: replace with your own (unique) device name
    threading.Thread(target=ble_gatt_uart_loop, args=(rx_q, tx_q, device_name), daemon=True).start()

    def get_spaces(string):
      spaces = ' ' * len(string)
         
      return spaces
    
    def split_string(input_string):
        # Ensure the string is at most 32 characters long
        trimmed_string = input_string[:32]
        
        # Get the first 16 symbols
        first_part = trimmed_string[:16]
        
        # Get the second 16 symbols
        second_part = trimmed_string[16:32]
        
        return first_part, second_part

    def lcd_print(string):
        if len(string) > 32:
            print(f'String {string} is too big: {len(string)}')

        if len(string) <= 16:
            lcd.send_string(f"{string}{get_spaces(string)}",1)
            lcd.send_string(" " * 16,2)
        else:
            first_part, second_part = split_string(string)
            lcd.send_string(first_part,1)
            lcd.send_string(f'{second_part}{get_spaces(second_part)}',2)

    while True:
        try:
            incoming = rx_q.get(timeout=1) # Wait for up to 1 second 
            if incoming:
                print("In main loop: ({})".format(incoming))
                lcd_print(incoming)
        except Exception as e:
            pass # nothing in Q
        
if __name__ == '__main__':
    lcd = LCD()
    try:
      main(lcd)
    except KeyboardInterrupt:
        pass
    finally:
        lcd.send_instruction(0x01) # Clear display & cursor home