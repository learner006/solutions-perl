use strict;
use 5.010;
use POSIX;
use Data::Dumper;

my $s = '93 - 42 / (  -80.2 * 45 + 46 + (  66 * 45 - 26 * 0 * 84  )  ) - (  (  20 - 59 - 18 - 62  ) / (  9 / 90 * 16 - 6  ) * 3  )';

$s =~ s/\s//g;

say $s;

my @lines = ($s =~ /(\d\d)/g);

#print Dumper @lines;

my @lines2 = ($s =~ /([^\d]*)(\d*[.]?\d*)/g);
#my @lines2 = ($s =~ /(?<not_number>[^\d]*)(?<number>\d*[.]?\d*)/g);

print Dumper @lines2;
# Что-то не сработало ;-)
#print Dumper %+;