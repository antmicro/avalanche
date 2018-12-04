INCLUDE generated/output_format.ld
ENTRY(_start)

INCLUDE generated/regions.ld

SECTIONS
{
	.text :
	{
		_ftext = .;
		*(.text .stub .text.* .gnu.linkonce.t.*)
		_etext = .;
	} > main_ram

	.rodata :
	{
		. = ALIGN(4);
		_frodata = .;
		*(.rodata .rodata.* .gnu.linkonce.r.*)
		*(.rodata1)

		/* Make sure the file is aligned on disk as well
		   as in memory; CRC calculation requires that. */
		FILL(0);
		. = ALIGN(4);
		_erodata = .;
	} > main_ram

	.bss :
	{
		. = ALIGN(4);
		_fbss = .;
		*(.dynsbss)
		*(.sbss .sbss.* .gnu.linkonce.sb.*)
		*(.scommon)
		*(.dynbss)
		*(.bss .bss.* .gnu.linkonce.b.*)
		*(COMMON)
		. = ALIGN(4);
		_ebss = .;
		_end = .;
	} > sram

	/DISCARD/ :
	{
		*(.eh_frame)
		*(.comment)
		*(.data .data.* .gnu.linkonce.d.*)
		*(.data1)
		*(.sdata .sdata.* .gnu.linkonce.s.*)
	}
}

PROVIDE(_fstack = ORIGIN(sram) + LENGTH(sram) - 4);
