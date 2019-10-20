use 5.010;

my @a1 = (1,2,3);
my @a2 = (1,1,1,1,1,1,1);

say scalar(@a2);

my $t = @a2;
say $t;

die;
for(0..scalar(@a2)-1)
{
	say $_;
}