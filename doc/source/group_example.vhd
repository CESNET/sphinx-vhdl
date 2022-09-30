library ieee;
use work.math_pack.all;
use ieee.std_logic_1164.all;

-- A universal asynchronous (dual clock) FIFO, suitable both for Xilinx and Intel
-- (Altera) FPGA. Can be parametrically implemented in BRAM or LUTRAM (MLAB on
-- Intel FPGA = 32 items, distributed memory in Xilinx FPGA = 64 items).
entity ASFIFOX is
generic (
    -- =====================================================================
    -- FIFO PARAMETERS
    --
    -- Base parameters of ASFIFOX memory.
    -- =====================================================================

    -- Data word width in bits.
    DATA_WIDTH          : natural := 512;
    -- FIFO depth in number of data words, must be a power of two!
    -- Minimum value is 2.
    ITEMS               : natural := 512;
    -- Select memory implementation. Options:
    --
    -- - "LUT"  - effective for shallow FIFO (approx. ITEMS <= 64),
    -- - "BRAM" - effective for deep FIFO (approx. ITEMS > 64).
    RAM_TYPE            : string  := "BRAM"; 
    -- First Word Fall Through mode. If FWFT_MODE=True, valid data will be
    -- ready at the ASFIFOX output without RD_EN requests.
    FWFT_MODE           : boolean := True;
    -- Enabled output registers allow better timing for a few flip-flops.
    OUTPUT_REG          : boolean := True;
    -- Determines how few data words must be left free for
    -- :vhdl:portsignal:`WR_AFULL <asfifox.wr_afull>` to be triggered.
    --
    -- (``currently_stored >= (`` :vhdl:gengeneric:`ITEMS <asfifox.items>` ``- ALMOST_FULL_OFFSET)``
    ALMOST_FULL_OFFSET  : natural := ITEMS/2;
    -- Determines how few data words must be stored for
    -- :vhdl:portsignal:`RD_AEMPTY <asfifox.rd_aempty>` to be triggered.
    --
    -- ( ``currently_stored <= ALMOST_EMPTY_OFFSET`` )
    ALMOST_EMPTY_OFFSET : natural := ITEMS/2;

    -- =====================================================================
    -- DEVICE PARAMETERS
    --
    -- The DEVICE parameter allows the correct selection of the RAM
    -- implementation according to the FPGA used.
    -- =====================================================================

    -- Supported values are:
    --
    -- - "7SERIES"
    -- - "ULTRASCALE"
    -- - "STRATIX10"
    -- - "ARRIA10"
    -- - "AGILEX"
    DEVICE              : string  := "ULTRASCALE"

);
port (
    -- =====================================================================
    -- WRITE INTERFACE
    --
    -- (This interface) Processes write transactions.
    -- =====================================================================

    -- Clock for write interface
    WR_CLK    : in  std_logic;
    -- Reset for write interface. Does not affect reset on read side
    WR_RST    : in  std_logic;
    -- Data to be written; must be valid when ``WR_EN = '1'``
    WR_DATA   : in  std_logic_vector(WR_DATA_WIDTH-1 downto 0);
    -- Indicates the validity of ``WR_DATA``. Can be connected as SRC_RDY.
    WR_EN     : in  std_logic;
    -- Writing is accepted only when WR_FULL=0, otherwise it is ignored.
    -- Can be connected as "not DST_RDY".
    WR_FULL   : out std_logic;
    -- Set to ``'1'`` when less than
    -- :vhdl:gengeneric:`ALMOST_FULL_OFFSET <asfifox.almost_full_offset>`
    -- space is left for writing items.
    WR_AFULL  : out std_logic;
    -- Indicates the number of items currently stored in the FIFO
    WR_STATUS : out std_logic_vector(log2(WR_ITEMS) downto 0);

    -- =====================================================================
    -- READ INTERFACE
    --
    -- (This interface) Processes read transactions.
    -- =====================================================================

    -- Clock for read interface
    RD_CLK    : in  std_logic;
    -- Reset for read interface. Does not affect reset on write side
    RD_RST    : in  std_logic;
    -- Data available for reading; valid when ``RD_EMPTY = '0'``
    RD_DATA   : out std_logic_vector(RD_DATA_WIDTH-1 downto 0);
    -- Set to ``'1'`` to request or accept valid data on RD_DATA.
    -- Can be connected as DST_RDY.
    RD_EN     : in  std_logic;
    -- When in ``'0'`` indicates valid data on ``RD_DATA``.
    -- Can be connected as "not SRC_RDY".
    RD_EMPTY  : out std_logic;
    -- Set to ``'1'`` when less than
    -- :vhdl:gengeneric:`ALMOST_EMPTY_OFFSET <asfifox.almost_empty_offset>`
    -- items are left for reading.
    RD_AEMPTY : out std_logic;
    -- Indicates the number of items currently stored in the FIFO. Items in
    -- output registers are also included in the calculation. There may be
    -- cases where ``RD_STATUS > 0`` and data are not yet available at the
    -- output (``RD_EMPTY = '1'``).
    RD_STATUS : out std_logic_vector(log2(RD_ITEMS) downto 0)

);
end entity ASFIFOX;

architecture FULL of ASFIFOX is

    -- Address width of memory
    constant MEM_ADDR_WIDTH : natural := log2(ITEMS);
    -- Address width
    constant ADDR_WIDTH     : natural := MEM_ADDR_WIDTH+1;
    -- Value that says, when FIFO is almost full
    constant AFULL_CAPACITY : natural := ITEMS - ALMOST_FULL_OFFSET; 

end architecture;