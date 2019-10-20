use strict;
use 5.010;
use Data::Dumper;
use List::Util qw/sum/;

my $FIELD_SIZE = 3;
my @FIELD;
my $CHAR_X = -1;
my $CHAR_0 = 1;
my $CHAR_NULL = 0;

my @turns_to_test = (
	[0,1],
	[1,2],
	[0,2],
	[0,0],
	[1,1],
	[0,0],
	[2,1],
	[0,1],
	[2,1],
	[0,1],
	[1,1]
);

my @turns2 = (
	[0,0],
	[1,1],
	[2,2]
);

my @turns3 = (
[1, 0],
[1, 2],
[2, 1],
[1, 2],
[1, 1],
[0, 1],
[2, 0],
[0, 1],
[2, 2],
[0, 1],
[1, 1],
[2, 0],
[0, 2]
);


my $CURR_PLAYER_SYMBOL = -1;

open D, '>DEBUG' or die;

init_game_state();

say '==== init:';
PrintField();

#my $TURNS = \@turns2;
#my $TURNS = \@turns_to_test;
my $TURNS = \@turns3;

for(@$TURNS)
{
	say "nextTurn($_->[0],$_->[1])";
	nextTurn($_->[0],$_->[1]);
	PrintField();
}



###########################################################################
#
#	init_game_state()
#
sub init_game_state
{
	for(1..$FIELD_SIZE)
	{
		# todo: investigate this trick later ;-)
		# google: perl fill array with zeros
		# url: https://stackoverflow.com/questions/5323845/perl-how-to-create-an-array-with-n-empty-strings-or-zeros

		my @arr = ($CHAR_NULL) x $FIELD_SIZE;
		push(@FIELD,\@arr)
	}
}

###########################################################################
#
# TrChar($CHAR_NULL); TrChar($CHAR_X); TrChar($CHAR_0);
#
sub TrChar
{
	my ($p_char) = @_;
	#my $result = 'null';
	my $result = '-';
	$result = 'x' if ($p_char eq $CHAR_X);
	$result = '0' if ($p_char eq $CHAR_0);

	return $result;
}
###########################################################################
#
# CheckBoundsUnstrict([$a,$b],$val);
#
sub CheckBoundsUnstrict
{
	my $result = 0;
	my ($p_arr,$p_val) = @_;

	return (@$p_arr[0] <= $p_val and $p_val <= @$p_arr[1]);
}
###########################################################################
#
# getFieldValue($row,$col);
#
sub getFieldValue
{
	my ($p_row,$p_col) = @_;

	my $result = $CHAR_NULL;
	if (
		CheckBoundsUnstrict([0,$FIELD_SIZE-1],$p_row) and
		CheckBoundsUnstrict([0,$FIELD_SIZE-1],$p_col)
		)
	{
		#print Dumper $FIELD[$p_row]->[$p_col];
		return TrChar($FIELD[$p_row]->[$p_col]);
	}
}
###########################################################################
#
# getWinner
#
sub getWinner
{
	#my $out_winner_char = $CHAR_NULL;
	my $c = $CHAR_NULL;

	#CheckDiags(\$c) or CheckRows(\$c) or CheckCols(\$c);

	CheckRows(\$c) or CheckCols(\$c) or CheckDiags(\$c);


	return TrChar($c);

}
###########################################################################
#
# my $c; CheckRows(\$c) or CheckCols(\$c) or CheckDiags(\$c);
#
sub CheckRows
{
	my ($out_c) = @_;

	$$out_c = undef;

	for my $row (@FIELD)
	{
		my $row_sum = 0;

		for(@$row)
		{
			$row_sum+=$_;
		}

		say D 'CheckRows: ' . $row_sum;

		$$out_c = $CHAR_X if ($row_sum == -$FIELD_SIZE);
		$$out_c = $CHAR_0 if ($row_sum == $FIELD_SIZE);

		last() if (defined($$out_c));
	}

	return defined($$out_c); # there is a winner! :-)
}
###########################################################################
#
# my $c; CheckRows(\$c) or CheckCols(\$c) or CheckDiags(\$c);
#
sub CheckCols
{
	my ($out_c) = @_;

	$$out_c = undef;

	for my $col_idx (0..$FIELD_SIZE)
	{
		my $col_sum = 0;
		for my $row_idx (0..$FIELD_SIZE)
		{
			$col_sum += $FIELD[$row_idx]->[$col_idx];
		}

		say D 'CheckCols: ' . $col_sum;

		$$out_c = $CHAR_X if ($col_sum == -$FIELD_SIZE);
		$$out_c = $CHAR_0 if ($col_sum == $FIELD_SIZE);

		last() if (defined($$out_c));
	}

	return defined($$out_c); # there is a winner! :-)
}
###########################################################################
#
# my $c; CheckRows(\$c) or CheckCols(\$c) or CheckDiags(\$c);
#
sub CheckDiags
{
	my ($out_c) = @_;

	$$out_c = undef;

	my $sum_d1 = 0;
	my $sum_d2 = 0;

	for my $idx (0..$FIELD_SIZE-1)
	{
		$sum_d1 += $FIELD[$idx]->[$idx];
		$sum_d2 += $FIELD[-$idx]->[$idx];
	}

	say D 'CheckDiags(d1): ' . $sum_d1;

	# todo: refactor it later ;-)

	$$out_c = $CHAR_X if ($sum_d1 == -$FIELD_SIZE);
	$$out_c = $CHAR_0 if ($sum_d1 == $FIELD_SIZE);

	unless (defined($$out_c))
	{
		$$out_c = $CHAR_X if ($sum_d2 == -$FIELD_SIZE);
		$$out_c = $CHAR_0 if ($sum_d2 == $FIELD_SIZE);
	}

	return defined($$out_c); # there is a winner! :-)
}
###########################################################################
#
# 
#
sub PrintField
{
	say 'Current player: ' . getCurrentPlayerSymbol();
	say 'isDraw: ' . isDraw();
	say 'noMoreTurns: ' . noMoreTurns();
	say 'getWinner: ' . getWinner();

	for my $row (@FIELD)
	{
		say join(' ', DecodeRow($row));
	}
}
###########################################################################
#
# say 'noMoreTurns' if noMoreTurns();
#
sub noMoreTurns
{
	# noMoreTurns means that there are no empty cells
	my $out_NoEmptyCellsOnField = 1;

	# Let's find at least one $CHAR_NULL code! :-)
	for(@FIELD)
	{
		print D Dumper @_;
		if ( grep {$_ == $CHAR_NULL} @$_ )
		{
			# we found an empty cell! :-)
			# let's go out there! :-)
			$out_NoEmptyCellsOnField = 0;
			last;

			say D 'noMoreTurns: $CHAR_NULL';
		}
	}

	return $out_NoEmptyCellsOnField;
}
###########################################################################
#
# 
#
sub isDraw
{
	# Если игра не окончена, то isDraw false
	# Ну, вроде так и есть?
	my $fNoMoreEmptyCellsOnField = noMoreTurns();

	return not defined(getWinner()) and noMoreTurns();
}
###########################################################################
#
# internal ;-)
#
sub changePlayer
{
	$CURR_PLAYER_SYMBOL *= -1;
}
###########################################################################
#
# 
#
sub getCurrentPlayerSymbolCode
{
	return $CURR_PLAYER_SYMBOL;
}
###########################################################################
#
# 
#
sub getCurrentPlayerSymbol
{
	return TrChar(getCurrentPlayerSymbolCode());
}
###########################################################################
#
# 
#
sub nextTurn
{
	my ($p_row,$p_col) = @_;

	my $result = $CHAR_NULL;
	if (
		CheckBoundsUnstrict([0,$FIELD_SIZE-1],$p_row) and
		CheckBoundsUnstrict([0,$FIELD_SIZE-1],$p_col)
		)
	{
		my $cell_is_empty = ($FIELD[$p_row]->[$p_col] == $CHAR_NULL);

		if ($cell_is_empty)
		{
			$FIELD[$p_row]->[$p_col] = getCurrentPlayerSymbolCode();
			changePlayer();
		}
	}
}
###########################################################################
#
# internal
#
sub DecodeRow
{
	my($p_arr) = @_;

	my @out_arr = @$p_arr;

	for(@out_arr)
	{
		$_ = TrChar($_);
	}

	return @out_arr;
}