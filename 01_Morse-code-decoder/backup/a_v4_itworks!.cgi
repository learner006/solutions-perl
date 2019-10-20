use strict;
use 5.010;

my %G_MORSE_CODE_TO_CHAR_MAP = {};

init_morse_map(\%G_MORSE_CODE_TO_CHAR_MAP);

my $in = '00101010100000000010001011101000101110100000111111**********00001011110000111111000010111000101110100000111010';

if (length($in) % 10)
{
	die 'length($in) % 10 != 0';
}

my @morse_chars = $in =~ /.{10}/g;

my %str_morse_char_map = ( 10 => '.', 11 => '-', '**' => ' ');

for(@morse_chars)
{
	my $morse_character_encoded_with_dashes_and_dots = '';

	my @morse_code = /.{2}/g;
	for(@morse_code)
	{
		if (exists($str_morse_char_map{$_}))
		{
			my $morse_char = $str_morse_char_map{$_};

			$morse_character_encoded_with_dashes_and_dots .= $morse_char;
			
			# print "$morse_char";

			last if ($_ eq '**');
		}
	}
	# Let's look up a table for a char!

	{
		my $c = $morse_character_encoded_with_dashes_and_dots;

		if ($c eq ' ')
		{
			print ' ';
		}
		elsif ( exists($G_MORSE_CODE_TO_CHAR_MAP{$c}) )
		{
			print $G_MORSE_CODE_TO_CHAR_MAP{$c};
		}
	}
}

sub init_morse_map
{
	my ($p_map_ref) = @_;

	open F, 'morse_table.txt';
	my @lines=<F>;
	close F;

	for(@lines)
	{
		chomp;
		if (/(.)\t(.+)/)
		{
			my $char = lc($1);
			my $dots_and_dashes = $2;

			$p_map_ref->{$dots_and_dashes} = $char;
		}
	}
}









