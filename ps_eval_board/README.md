Simple evaluation board for raspberry pi (zero) with lib and schematics

Library for ps_eval_board 
Buttons on GPIO 26, 19, 13, 6
Leds on GPIO 4, 17, 27, 22
methods:
button1_pressed() -> returns 0 or 1 ... checks button1
button2_pressed() -> returns 0 or 1 ... checks button2 
button3_pressed() -> returns 0 or 1 ... checks button3
button4_pressed() -> returns 0 or 1 ... checks button4
get_key_pressed() -> returns 0 or 1 ... checks all buttons at once
get_which_key_pressed() -> returns 1, 2, 3, 4 ... indicates which button is pressed (0 for none)
set_led(x) -> x is 1 to 4 to turn on one specific led
set_led_bits(x) -> 4 bits of x will be used to display binary number
set_display_text(text) -> text will be split into lines of 20 characters
set_display_lines(lines) -> lines array will be displayed 
get_device() -> returns oled device 

![ps_eval_board_Main](https://user-images.githubusercontent.com/80522869/150007262-9ea80cc1-ee29-4a51-9909-382d6093ace2.gif)

And a possible board design

![ps_eval_board](https://user-images.githubusercontent.com/80522869/150007057-a8622906-360c-49f8-9bcb-9226eacd2ee6.png)


