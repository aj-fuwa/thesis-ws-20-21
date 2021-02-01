---------------------------------------------------------------------------------------------------
-- Name: voltage_select_tb.vhd
-- Task: To implement testbench for voltage_select.vhd
-- Language: VHDL
-- Date: (Revised) 24.Jan 2021
-- Src:	https://vhdlguide.readthedocs.io/en/latest/vhdl/testbench.html#simple-testbench
--	https://youtube.com/playlist?list=PLZv8x7uxq5XY-IQfQFb6mC6OXzz0h8ceF
---------------------------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;

entity voltage_select_tb is
end voltage_select_tb;

architecture behave of voltage_select_tb is
	signal pin_a, pin_b, pin_c: std_logic;
	signal out4a, out4b, out4c: std_logic;
begin
	UUT: entity work.Voltage_select port map (pin_a => pin_a, pin_b => pin_b, pin_c => pin_c, out4a => out4a, out4b => out4b, out4c => out4c);
	
	pin_a <= '0', '1' after 20 ns, '0' after 40 ns, '1' after 80 ns, '0' after 120 ns, '1' after 140 ns;
	pin_b <= '0', '1' after 40 ns, '0' after 60 ns, '1' after 80 ns, '0' after 100 ns, '1' after 120 ns;
	pin_c <= '0', '1' after 60 ns, '0' after 80 ns, '1' after 100 ns;
	
end behave;
