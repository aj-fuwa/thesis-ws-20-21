---------------------------------------------------------------------------------------------------
-- Name: voltage_select.vhd
-- Task: To implement the logic for the selecting the correct voltage level for the Piezo-amplifier
-- Language: VHDL
-- Date: (Revised) 23.Jan 2021
-- Src: https://youtube.com/playlist?list=PLZv8x7uxq5XY-IQfQFb6mC6OXzz0h8ceF
---------------------------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;

-- defines the input and the outputs of the Logic ckt
-- pin_a, pin_b, pin_c are the pins from the Raspberry Pi to the FPGA
-- out4a, out4b, out4c are the pins that will switch on the relays
entity Voltage_select is 
	port(
	pin_a, pin_b, pin_c: in std_logic;
	out4a, out4b, out4c: out std_logic
	);
end Voltage_select;

architecture Dataflow of Voltage_select is
begin 
	out4a <= pin_a AND NOT pin_b AND NOT pin_c;
	out4b <= NOT pin_a AND pin_b AND NOT pin_c;
	out4c <= NOT pin_a AND NOT pin_b AND pin_c;

end Dataflow;
