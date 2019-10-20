use strict;
use 5.010;
use POSIX;
use Data::Dumper;

=pod
it('should multiply 2 numbers and return product 25101298695270351557618164676932440113017170708232756964483490927393235787759886048', () => {
  assert.strictEqual(multiply('760954769047694567984358934658793465783', '32986584375683268326478346587346582436583456'), '25101298695270351557618164676932440113017170708232756964483490927393235787759886048');
});

'760954769047694567984358934658793465783'
'32986584375683268326478346587346582436583456'

product:
'25101298695270351557618164676932440113017170708232756964483490927393235787759886048'
#############################
this script product:
 25101298695270351557618164676932440113017170708232756964483490927393235787759886048
###############################

it('should multiply 2 numbers and return product 8039478803562301312945731536636937786946145622033671701077185622708260023194452833705836798934954757818601850586548267694783898227720224627622563294226313567463000537341441969561807100657519886048', () => {
  assert.strictEqual(multiply('3467598346538256487395689342653498563412312376095476904769456798433934759347589346587346578342658346285963489253465783', '2318457329865843872563478658342756873375683268326583435452342347346582436583456'), '8039478803562301312945731536636937786946145622033671701077185622708260023194452833705836798934954757818601850586548267694783898227720224627622563294226313567463000537341441969561807100657519886048');
});

'3467598346538256487395689342653498563412312376095476904769456798433934759347589346587346578342658346285963489253465783'
'2318457329865843872563478658342756873375683268326583435452342347346582436583456'

product
'8039478803562301312945731536636937786946145622033671701077185622708260023194452833705836798934954757818601850586548267694783898227720224627622563294226313567463000537341441969561807100657519886048');

#############################
this script product:

3467598346538256487395689342653498563412312376095476904769456798433934759347589346587346578342658346285963489253465783
2318457329865843872563478658342756873375683268326583435452342347346582436583456
 8039478803562301312945731536636937786946145622033671701077185622708260023194452833705836798934954757818601850586548267694783898227720224627622563294226313567463000537341441969561807100657519886048
##############################





=cut

my @num_to_test = (
[
	'985621',
	'2492'
], 
[
	'985621',
	'002492'
], 
[
	'24568395411',
	'00000010455'
],
[
	'2',
	'3'
],
[
	'9',
	'9'
],
[
	'10',
	'05'
],
[
	'129',
	'024'
],
[
	'29403',
	'00012'
],
[
	'12',
	'29403'
],
[
	'760954769047694567984358934658793465783',
	'32986584375683268326478346587346582436583456'
],
[
	'3467598346538256487395689342653498563412312376095476904769456798433934759347589346587346578342658346285963489253465783',
	'2318457329865843872563478658342756873375683268326583435452342347346582436583456'
]
);

=pod
my $n1_str = $num_to_test[0]->[0];
my $n2_str = $num_to_test[0]->[1];

say $n1_str;
say $n2_str;

my @n1_arr = split(//,$n1_str);
my @n2_arr = split(//,$n2_str);

AdjustSizesLeftPadding(\@n1_arr,\@n2_arr);
say join('',@n1_arr);
say join('',@n2_arr);
die;
=cut

=pod





#print Dumper @n1_arr;
#print Dumper @n2_arr;

my $sum_arr = AddBigNum(\@n1_arr,\@n2_arr);


my $digit_to_multiply = 5;

my @mul_arr1 = MultiplyNumByDigit(\@n1_arr,$digit_to_multiply);

=cut
#-----------
my $n1_str = $num_to_test[10]->[0];
my $n2_str = $num_to_test[10]->[1];

say $n1_str;
say $n2_str;

my @n1_arr = split(//,$n1_str);
my @n2_arr = split(//,$n2_str);

my $mul_arr = MultiplyBigNum(\@n1_arr,\@n2_arr);

say join('',@$mul_arr);
say "Perl multiplication ($n1_str * $n2_str): ", $n1_str * $n2_str;
#-----------


###########################################################################
#
# my $sum_arr = AddBigNum(\@n1_arr,\@n2_arr);
#
sub AddBigNum
{       
	my ($p_arr1,$p_arr2) = @_;

	my ($a1,$a2) = ($p_arr1,$p_arr2);

	AdjustSizesLeftPadding($a1,$a2);

=pod

	unless (scalar(@$p_arr1) == scalar(@$p_arr2))
	{
		die '[AddBigNum] Numbers are no right padded by zeros';
	}
=cut

	my @out_res = ();
	my $extra_digit = 0;

	for(1..scalar(@$a1))
	{
		# we are going backward! (negative indexes)
		my $digit_sum_wide = $a1->[-$_] + $a2->[-$_] + $extra_digit;

		$extra_digit = floor( $digit_sum_wide / 10 );
		my $digit_sum = $digit_sum_wide % 10;

		unshift(@out_res, $digit_sum);
	}

	if ($extra_digit)
	{
		unshift(@out_res, $extra_digit);
	}

	return @out_res;
}
###########################################################################
#
# 	AdjustSizesLeftPadding($a1,$a2);
#
sub AdjustSizesLeftPadding
{
	my ($p_a1,$p_a2) = @_;

	my $size1 = @$p_a1;
	my $size2 = @$p_a2;

	return if ($size1 == $size2);

	my ($a1,$a2) = ($p_a1,$p_a2);

	# swap references to easy code! :-)
	if ($size1 < $size2)
	{
		($a1,$a2) = ($a2,$a1);
		($size1,$size2) = ($size2,$size1);
	}

	# $size1 > $size2 for now
	my @zeros = (0) x ($size1 - $size2);
	unshift(@$a2,@zeros);
}
###########################################################################
#
# my @mul_arr1 = MultiplyNumByDigit(\@n1_arr,$digit_to_multiply);
#
sub MultiplyNumByDigit
{
	my ($p_arr1,$p_digit) = @_;

	my ($arr,$n) = ($p_arr1,$p_digit);
	my $extra_digit = 0;

	my @out_res = ();

	for(1..scalar(@$arr))
	{
		# going backward
		my $m_wide = $arr->[-$_] * $n + $extra_digit;

		$extra_digit = floor( $m_wide / 10 );
		my $m = $m_wide % 10;

		unshift(@out_res, $m);
	}

	if ($extra_digit)
	{
		unshift(@out_res, $extra_digit);
	}

	return @out_res;
}
###########################################################################
#
# my $mul_arr = MultiplyBigNum(\@n1_arr,\@n2_arr);
#
sub MultiplyBigNum
{
	my ($p_arr1,$p_arr2) = @_;

	my ($a1,$a2) = ($p_arr1,$p_arr2);

	# Set $a2 reference to the smallest number
	if (@$a2 > @$a1)
	{
		($a1,$a2) = ($a2,$a1);
	}

	my @out_res;

	for(1..scalar(@$a2))
	{
		# moving back! (negative indexes)
		my @mul = MultiplyNumByDigit($a1,$a2->[-$_]);

		my @zeros_on_the_right = (0) x ($_-1);
		push(@mul,@zeros_on_the_right);

		AdjustSizesLeftPadding(\@out_res,\@mul);

		@out_res = AddBigNum(\@out_res,\@mul);
	}

	return \@out_res;
}



















