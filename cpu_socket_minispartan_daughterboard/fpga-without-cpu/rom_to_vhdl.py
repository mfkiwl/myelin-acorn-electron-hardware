# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import time


def rom_to_vhdl(name, infile, data):

    # convert binary data to a bunch of VHDL lines
    data_lines = "\n".join(
        '                when x"%04x" => Di <= x"%02x";' % (
            i, ord(data[i])
        ) for i in range(len(data))
        if data[i] != '\xff'
    )

    # wrap it in an entity specifier
    return """-- generated by rom_to_vhdl.py from %(infile)s at %(date)s
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

-- 16 kB ROM image
entity %(romname)s is
    port (
        CLK : in std_logic;
        A : in std_logic_vector(13 downto 0);
        D : out std_logic_vector(7 downto 0);
        CS : in std_logic
    );
end;

architecture Behavioural of %(romname)s is

    signal Di : std_logic_vector(7 downto 0);

begin

    process(CLK)
    begin
        if rising_edge(CLK) then
            case "00" & A is
%(data_lines)s
                when others => Di <= x"ff";
            end case;
        end if;
    end process;

    D <= "ZZZZZZZZ" when CS = '0' else Di;

end Behavioural;
""" % {
        'data_lines': data_lines,
        'date': time.strftime("%F %T %Z"),
        'infile': infile,
        'romname': name,
    }

if __name__ == '__main__':
    infile, outfile, name = sys.argv[1:]
    open(outfile, 'w').write(rom_to_vhdl(name, infile, open(infile).read()))
