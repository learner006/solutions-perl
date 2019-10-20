use strict;
use 5.010;


my $re = qr/simple/;
 ;;
 my $string = 'This is a simple string, just a simple simple thing.';
 my @captures = $string =~ /$re/g;
 say @captures;