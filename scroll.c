#include <stdio.h>
#include <stdlib.h>
unsigned short int charecterA[8] = {0x0e, 0x11, 0x11, 0x11, 0x1f, 0x11, 0x11, 0x11};

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
		printf("%d\t", output_data);
	}
	printf("\n");
	return 0;
}

int main (int argc, char **argv)
{
	int i, a, b, c, n = 10;
	system("clear");
	for (i = 0; i < 8; i++)
	{
		send_data(charecterA[i]);
	}
	return 0;
}
