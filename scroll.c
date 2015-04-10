#include <stdio.h>
#include <stdlib.h>

unsigned char charecterA[][8] = {{0x0e, 0x11, 0x11, 0x11, 0x1f, 0x11, 0x11, 0x11}, {0x0e, 0x09, 0x09, 0x0e, 0x09, 0x09, 0x09, 0x0e}, {0x11, 0x19, 0x15, 0x13}};

int send_data(unsigned int data)
{
	unsigned int mask = 0x0001, flag;
	int i, output_data;
	for (i = 15; i >= 0; i--)
	{
		if ((data & (mask << i)) == 0)
			output_data = 0;
		else
			output_data = 1;
		printf("%d ", output_data);
	}
	printf("\n");
	return 0;
}

int main (int argc, char **argv)
{
	int i, a, b, c, n = 10;
	unsigned char temp;
	unsigned short int scroll, shift_amount, display_buffer[8];
	system("clear");
	for (i = 0; i < 8; i++)
		display_buffer[i] = 0x0000;
	for (i = 0; i < 2; i++)
	for (scroll = 4; scroll < 9; scroll++)
	{
		for (shift_amount = 0; shift_amount < 8; shift_amount++)
		{
			temp = charecterA[i][shift_amount];
			display_buffer[shift_amount] = (display_buffer[shift_amount] << 1) | (temp >> (8 - scroll));
			send_data(display_buffer[shift_amount]);
		}
	system("sleep 0.6");
	system("clear");
	}
	for (i = 0; i < 16; i++)
	{
		for (shift_amount = 0; shift_amount < 8; shift_amount++)
		{
			display_buffer[shift_amount] = display_buffer[shift_amount] << 1;
			send_data(display_buffer[shift_amount]);
		}
		system("sleep 0.6");
		system("clear");
	}	
	return 0;
}
