my $token = '2';
my $res = ( $token =~ /[-+\*\/]/ );
if ($res)
{
	print 1;
}
else
{
	print 2;
}


