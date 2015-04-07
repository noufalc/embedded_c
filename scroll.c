#include <stdio.h>


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
	unsigned int data = 0x7e;
	send_data(data);
	return 0;
}
