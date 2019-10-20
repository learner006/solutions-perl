use strict;
use 5.010;

my $in = '00101010100000000010001011101000101110100000111111**********00001011110000111111000010111000101110100000111010';

if (length($in) % 10)
{
	die 'length($in) % 10 != 0';
}

my @morse_chars = $in =~ /.{10}/g;

my %str_morse_char_map = ( 10 => '.', 11 => '-', '**' => ' ');

for(@morse_chars)
{
	my @morse_code = /.{2}/g;
	for(@morse_code)
	{
		if (exists($str_morse_char_map{$_}))
		{
			my $morse_char = $str_morse_char_map{$_};
			print "$morse_char";
			last if ($_ eq '**');
		}
	}
#	print "\n";
	print " ";
}
