use strict;
use 5.010;
use POSIX;
use Data::Dumper;

my @range_test;
my $num_test;
GetTestData(\@range_test,\$num_test);

my ($LEFT_BOUND,$RIGHT_BOUND) = @range_test;
my $CENTER = undef;

for(1..100)
{
	my $num = Guess();

	my $temp = "Lower";
	if ($num_test > $num)
	{
		$temp = "Greater";
	}

	my $msg2 = "[$LEFT_BOUND,$RIGHT_BOUND] $\CENTER + 1 = " . ($CENTER + 1);

	say "Step $_: $num ($num_test) $msg2 [$temp]";

	last if ($num == $num_test);

	if ($num_test > $num)
	{
		Greater();
	}
	else
	{
		Lower();
	}
}

###########################################################################
#
# GetTestData(\@range_test,\$num_test);
#
sub GetTestData
{
	my($pout_range,$pout_num) = @_;

=pod
# Test group 1
	@$pout_range = (1,1000);
	#$$pout_num = 64;
	$$pout_num = 2;
=cut
=pod
# Test group 2
	@$pout_range = (1,1000000);
	$$pout_num = 2;
=cut
=pod
# Test group 3
	@$pout_range = (1,100000000);
	#$$pout_num = 2;
	$$pout_num = 999999999;
=cut
=pod
# Test group 4
	@$pout_range = (1,100000001);
	#$$pout_num = 2;
	$$pout_num = 999999999;
=cut
=pod
# Test group 5
	@$pout_range = (1,11);
	#$$pout_num = 1;
	$$pout_num = 11;
=cut
=pod
# Test group 6
	@$pout_range = (1,2);
	$$pout_num = 1;
=cut
=pod
# Test group 7
	@$pout_range = (0,4048);
	$$pout_num = 409;
=cut
=pod
# Test group 8
	@$pout_range = (0,3445);
	$$pout_num = 279;
=cut
# Test group 9
	@$pout_range = (1,2);
	$$pout_num = 2;








}
###########################################################################
#
# Guess()
#
sub Guess
{

	my $distance = GetDistance();

	die '$RIGHT_BOUND - $LEFT_BOUND < 0' if($distance < 0);

	# The algo is converged! We found a number!
	if ($distance == 0)
	{
		return $RIGHT_BOUND;
	}
	else
	{
		# Let's split a segment one more time! :-)
		$CENTER = floor( ($LEFT_BOUND + $RIGHT_BOUND) / 2 );

		# return a start of the right segment
		return $CENTER + 1; 
	}
}
###########################################################################
#
#
#
sub Lower
{
	# Nothing to do
	if (GetDistance() <= 0)
	{
		return;
	}

	# A number is inside the 'lower' segment
	# Let's use it further!

	$RIGHT_BOUND = $CENTER;
}
###########################################################################
#
#
#
sub Greater
{
	# Nothing to do
	if (GetDistance() <= 0)
	{
		return;
	}

	# A number is inside the 'greater' segment
	# Let's use it further!

	$LEFT_BOUND = $CENTER + 1;
}
###########################################################################
#
#
#
sub GetDistance
{
	return $RIGHT_BOUND - $LEFT_BOUND;
}
###########################################################################