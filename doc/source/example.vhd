library ieee;
use ieee.numeric_std.all;

-- This package provides basic mathematic functions utilised all through
-- the design
package math_pack is
    -- This function calculates the base 2 logarithm of a number.
    --
    -- .. vhdl:parameters:: log2
    --
    --     a : in unsigned
    --         The number of which to calculate the logarithm
    function log2 parameter (a : unsigned) return integer;
end package math_pack;

library ieee;
use work.math_pack.all;
use ieee.std_logic_1164.all;

-- This is a simple counter entity that counts the amount of passed input
-- clock cycles up to :vhdl:genconstant:`max_value <counter.max_value>`.
entity counter is
generic (
    -- Determines how many clock cycles must pass before the buffer
    -- overflowing.
    constant max_value : integer := 16
);
port (
    IN_EN  : in std_logic;                                       -- The input clock
    OUT_EN : out std_logic_vector(log2(max_value) - 1 downto 0)  -- The output signal
);
end entity counter;