use 5.010;

my @a = (1..100);
my $aref = \@a;

my @a2 = @a[0..2];
say @a2;

#my @a3 = $aref->[0..2];
my @a3 = @$aref[0..2];
say @a3;