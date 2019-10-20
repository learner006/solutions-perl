use strict;
use 5.010;
use POSIX;
use Data::Dumper;

GetHashRefForChar();


sub GetHashRefForChar
{
	my $lout_hash_ref = '';

	if (1 > 0)
	{
		$lout_hash_ref = 1;
	}
	elsif (1 < 0)
	{
		$lout_hash_ref = 2;
	}

	print  'GetHashRefForChar::';
	print  Dumper $lout_hash_ref;

	return $lout_hash_ref;
}