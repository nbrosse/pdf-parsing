# PRODUCT OBSOLETE / UNDER OBSOLESCENCE

# XC9500 In-System Programmable CPLD Family

DS063 (v6.0) May 17, 2013

# Features

- Advanced CMOS 5V FastFLASH™ technology
- Supports parallel programming of multiple XC9500 devices
- High-performance
- 5 ns pin-to-pin logic delays on all pins
- fCNT to 125 MHz
- Large density range
- 36 to 288 macrocells with 800 to 6,400 usable gates
- 5V in-system programmable
- Endurance of 10,000 program/erase cycles
- Program/erase over full commercial voltage and temperature range
- Enhanced pin-locking architecture
- Flexible 36V18 Function Block
- 90 product terms drive any or all of 18 macrocells within Function Block
- Global and product term clocks, output enables, set and reset signals
- Extensive IEEE Std 1149.1 boundary-scan (JTAG) support
- Programmable power reduction mode in each macrocell
- Slew rate control on individual outputs
- User programmable ground pin capability
- Extended pattern security features for design protection
- High-drive 24 mA outputs
- 3.3V or 5V I/O capability

# Family Overview

The XC9500 CPLD family provides advanced in-system programming and test capabilities for high performance, general purpose logic integration. All devices are in-system programmable for a minimum of 10,000 program/erase cycles. Extensive IEEE 1149.1 (JTAG) boundary-scan support is also included on all family members.

As shown in Table 1, logic density of the XC9500 devices ranges from 800 to over 6,400 usable gates with 36 to 288 registers, respectively. Multiple package options and associated I/O capacity are shown in Table 2. The XC9500 family is fully pin-compatible allowing easy design migration across multiple density options in a given package footprint.

# Table 1: XC9500 Device Family

| |XC9536|XC9572|XC95108|XC95144|XC95216|XC95288|
|---|---|---|---|---|---|---|
|Macrocells|36|72|108|144|216|288|
|Usable Gates|800|1,600|2,400|3,200|4,800|6,400|
|Registers|36|72|108|144|216|288|
|T PD (ns)|5|7.5|7.5|7.5|10|15|
|T SU (ns)|3.5|4.5|4.5|4.5|6.0|8.0|
|T CO (ns)|4.0|4.5|4.5|4.5|6.0|8.0|
|fCNT (MHz)(1)|100|125|125|125|111.1|92.2|
|fSYSTEM (MHz)(2)|100|83.3|83.3|83.3|66.7|56.6|

1. fCNT = Operating frequency for 16-bit counters.

2. SYSTEM = Internal operating frequency for general purpose system designs spanning multiple FBs.

© 1998–2007, 2013 Xilinx, Inc. All rights reserved. All Xilinx trademarks, registered trademarks, patents, and disclaimers are as listed at http://www.xilinx.com/legal.htm. All other trademarks and registered trademarks are the property of their respective owners. All specifications are subject to change without notice.

DS063 (v6.0) May 17, 2013

www.xilinx.com
---
# – PRODUCT OBSOLETE / UNDER OBSOLESCENCE –

# XC9500 In-System Programmable CPLD Family

# Table 2: Available Packages and Device I/O Pins (not including dedicated JTAG pins)

| |XC9536|XC9572|XC95108|XC95144|XC95216|XC95288|
|---|---|---|---|---|---|---|
|44-Pin VQFP|34|-|-|-|-|-|
|44-Pin PLCC|34|34|-|-|-|-|
|48-Pin CSP|34|-|-|-|-|-|
|84-Pin PLCC|-|69|69|-|-|-|
|100-Pin TQFP|-|72|81|81|-|-|
|100-Pin PQFP|-|72|81|81|-|-|
|160-Pin PQFP|-|-|108|133|133|-|
|208-Pin HQFP|-|-|-|-|166|168|
|352-Pin BGA|-|-|-|-|166(2)|192|

1. Most packages available in Pb-Free option. See individual data sheets for more details.

2. 352-pin BGA package is being discontinued for the XC95216. See XCN07010 for details.

# Architecture Description

Each XC9500 device is a subsystem consisting of multiple Function Blocks (FBs) and I/O Blocks (IOBs) fully interconnected by the Fast CONNECT™ switch matrix. The IOB provides buffering for device inputs and outputs. Each FB provides programmable logic capability with 36 inputs and 12 to 18 outputs (depending on package pin-count) and associated output enable signals drive directly to the IOBs. See Figure 1.

2 www.xilinx.com DS063 (v6.0) May 17, 2013 Product Specification
---
# – PRODUCT OBSOLETE / UNDER OBSOLESCENCE –

# XC9500 In-System Programmable CPLD Family

# 3 JTAG

JTAG Port
Controller
In-System Programming Controller

# Function Blocks

|I/O|36|Function|18|Block 1|Macrocells|1 to 18|
|---|---|---|---|---|---|---|
|I/O|36|Function|18|Block 2|Macrocells|1 to 18|
|I/O|36|Function|18|Block 3|Macrocells|1 to 18|
|I/O/GCK|3|36|Function|1|I/O/GSR|2 or 4|
|I/O/GTS| | | | | |1 to 18|

# Figure 1: XC9500 Architecture

Note: Function block outputs (indicated by the bold lines) drive the I/O blocks directly.

# Function Block

Each Function Block, as shown in Figure 2, is comprised of 90 product terms. Any number of these product terms, up to 18 independent macrocells, each capable of implementing the 90 available, can be allocated to each macrocell by the product term allocator. The FB also receives global clock, output enable, and set/reset signals. The FB generates 18 outputs that drive the Fast CONNECT switch matrix. These 18 outputs and their corresponding output enable signals also drive the IOB.

Logic within the FB is implemented using a sum-of-products representation. Thirty-six inputs provide 72 true and complement signals into the programmable AND-array to form.

DS063 (v6.0) May 17, 2013

www.xilinx.com
---
# – PRODUCT OBSOLETE / UNDER OBSOLESCENCE –

# XC9500 In-System Programmable CPLD Family

# Macrocell 1

Programmable AND-Array Term Allocators

|From|Fast CONNECT II|Switch Matrix|To Fast CONNECT II|
|---|---|---|---|
|36|18|OUT|18|
|To I/O Blocks|To I/O Blocks|PTOE| |

# Macrocell 18

1

Global Set/Reset Clocks

DS063_02_110501

# Figure 2: XC9500 Function Block

4

www.xilinx.com

DS063 (v6.0) May 17, 2013

# Product Specification