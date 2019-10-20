use strict;
use 5.010;

=pod
my $re = qr/simple/;
 ;;
 my $string = 'This is a simple string, just a simple simple thing.';
 my @captures = $string =~ /$re/g;
 say @captures;
=cut

my $in = '00101010100000000010001011101000101110100000111111**********00001011110000111111000010111000101110100000111010';
#my $in = '00101010100000000010';

#my @chars = $in =~ /........../g;
my @chars = $in =~ /.{10}/g;

say for(@chars);
