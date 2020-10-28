library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_misc.all;
use ieee.numeric_std.all;

library work;
use work.pat_pkg.all;
use work.patterns.all;

entity pat_unit is
  generic(
    PATLIST  : pat_list_t := pat_list;
    LY0_SPAN : natural    := 11;        -- TODO: get span from patlist w/ function
    LY1_SPAN : natural    := 11;        -- TODO: get span from patlist w/ function
    LY2_SPAN : natural    := 11;        -- TODO: get span from patlist w/ function
    LY3_SPAN : natural    := 11;        -- TODO: get span from patlist w/ function
    LY4_SPAN : natural    := 11;        -- TODO: get span from patlist w/ function
    LY5_SPAN : natural    := 11         -- TODO: get span from patlist w/ function
    );
  port(

    clock : in std_logic;

    ly0 : in std_logic_vector (LY0_SPAN-1 downto 0);
    ly1 : in std_logic_vector (LY1_SPAN-1 downto 0);
    ly2 : in std_logic_vector (LY2_SPAN-1 downto 0);
    ly3 : in std_logic_vector (LY3_SPAN-1 downto 0);
    ly4 : in std_logic_vector (LY4_SPAN-1 downto 0);
    ly5 : in std_logic_vector (LY5_SPAN-1 downto 0);

    pat_o : out candidate_t

    );
end pat_unit;

architecture behavioral of pat_unit is


  signal pat_candidates : candidate_list_t (patlist'range);

  function count_ones(slv : std_logic_vector) return natural is
    variable n_ones : natural := 0;
  begin
    for i in slv'range loop
      if slv(i) = '1' then
        n_ones := n_ones + 1;
      end if;
    end loop;
    return n_ones;
  end function count_ones;

begin

  assert (LY0_SPAN mod 2 = 1) report "Layer Span Must be Odd" severity error;
  assert (LY1_SPAN mod 2 = 1) report "Layer Span Must be Odd" severity error;
  assert (LY2_SPAN mod 2 = 1) report "Layer Span Must be Odd" severity error;
  assert (LY3_SPAN mod 2 = 1) report "Layer Span Must be Odd" severity error;
  assert (LY4_SPAN mod 2 = 1) report "Layer Span Must be Odd" severity error;
  assert (LY5_SPAN mod 2 = 1) report "Layer Span Must be Odd" severity error;

  patgen : for I in patlist'range generate

    function get_ly_size (ly     : natural;
                          ly_pat : hi_lo_t)
      return natural is
    begin
      return (ly_pat.hi-ly_pat.lo+1);
    end;

    function get_ly_mask (size   : natural;
                          ly     : std_logic_vector;
                          ly_pat : hi_lo_t)
      return std_logic_vector is
      variable result : std_logic_vector(size-1 downto 0);
      variable center : natural := ly'length / 2;  -- FIXME: check the rounding on this
    begin
      result := ly (center + ly_pat.hi downto center + ly_pat.lo);
      return result;
    end;

    constant ly0_size : natural := get_ly_size (0, patlist(I).ly0);
    constant ly1_size : natural := get_ly_size (1, patlist(I).ly1);
    constant ly2_size : natural := get_ly_size (2, patlist(I).ly2);
    constant ly3_size : natural := get_ly_size (3, patlist(I).ly3);
    constant ly4_size : natural := get_ly_size (4, patlist(I).ly4);
    constant ly5_size : natural := get_ly_size (5, patlist(I).ly5);

    signal ly0_mask : std_logic_vector (ly0_size-1 downto 0);
    signal ly1_mask : std_logic_vector (ly1_size-1 downto 0);
    signal ly2_mask : std_logic_vector (ly2_size-1 downto 0);
    signal ly3_mask : std_logic_vector (ly3_size-1 downto 0);
    signal ly4_mask : std_logic_vector (ly4_size-1 downto 0);
    signal ly5_mask : std_logic_vector (ly5_size-1 downto 0);

  begin

    assert false report "ly0_size=" & integer'image(ly0_size) severity note;
    assert false report "ly1_size=" & integer'image(ly1_size) severity note;
    assert false report "ly2_size=" & integer'image(ly2_size) severity note;
    assert false report "ly3_size=" & integer'image(ly3_size) severity note;
    assert false report "ly4_size=" & integer'image(ly4_size) severity note;
    assert false report "ly5_size=" & integer'image(ly5_size) severity note;

    ly0_mask <= get_ly_mask (ly0_size, ly0, patlist(I).ly0);
    ly1_mask <= get_ly_mask (ly1_size, ly1, patlist(I).ly1);
    ly2_mask <= get_ly_mask (ly2_size, ly2, patlist(I).ly2);
    ly3_mask <= get_ly_mask (ly3_size, ly3, patlist(I).ly3);
    ly4_mask <= get_ly_mask (ly4_size, ly4, patlist(I).ly4);
    ly5_mask <= get_ly_mask (ly5_size, ly5, patlist(I).ly5);

    process (clock) is
    begin
      if (rising_edge(clock)) then
        pat_candidates(I).cnt <= to_unsigned(count_ones(
          or_reduce(ly0_mask) &
          or_reduce(ly1_mask) &
          or_reduce(ly2_mask) &
          or_reduce(ly3_mask) &
          or_reduce(ly4_mask) &
          or_reduce(ly5_mask)),
                                             CNT_BITS);
        pat_candidates(I).id   <= to_unsigned(patlist(I).id, PAT_BITS);
        pat_candidates(I).hash <= (others => '0');  --mask_to_code (ly0_mask, ly1_mask, ly2_mask, ly3_mask, ly4_mask, ly5_mask);
      end if;
    end process;
  end generate;


  -- need flexible N to 1 sorter... recursive..?
  process (clock) is
    variable best : candidate_t;
  begin
    if (rising_edge(clock)) then

      best.cnt  := (others => '0');
      best.hash := (others => '0');
      best.id   := (others => '0');

      for I in pat_candidates'length-1 downto 0 loop
        if (pat_candidates(I).cnt & pat_candidates(I).hash) > (best.cnt & best.hash) then
          best := pat_candidates(I);
        end if;
      end loop;

    end if;

    pat_o <= best;
  end process;


end behavioral;
