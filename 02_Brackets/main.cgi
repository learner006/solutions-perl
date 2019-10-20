use strict;
use 5.010;
use POSIX;
use Data::Dumper;

# check('([{}])', [ ['(', ')'], ['[', ']'], ['{', '}']]) // -> true

#open F_LOG, '>F_LOG' or die $!;
open L, '>L' or die $!;

=pod
# Tests group 1
#my $input = '([{}])';
my $input = '([{}][)';
my @cfg = ( ['(', ')'], ['[', ']'], ['{', '}'] );
=cut

# Test group 2
=pod
const config7 = [['(', ')'], ['[', ']'], ['{', '}'], ['|', '|']];

it('should check if brackets sequence is not correct 18', () => {
  assert.equal(check('([[[[(({{{}}}(([](((((((())))||||||))))[[{{|{{}}|}}[[[[]]]]{{{{{}}}}}]]))))]]]]))()', config7), false);
});

it('should check if brackets sequence is correct 19', () => {
  assert.equal(check('([[[[(({{{}}}(([](((((((())))||||||))))[[{{|{{}}|}}[[[[]]]]{{{{{}}}}}]]))))]]]])(())', config7), true);
});
=cut
=pod
# false
my $input18 = '([[[[(({{{}}}(([](((((((())))||||||))))[[{{|{{}}|}}[[[[]]]]{{{{{}}}}}]]))))]]]]))()';
# true
my $input19 = '([[[[(({{{}}}(([](((((((())))||||||))))[[{{|{{}}|}}[[[[]]]]{{{{{}}}}}]]))))]]]])(())';

my $input = $input19;
my @cfg = (['(', ')'], ['[', ']'], ['{', '}'], ['|', '|']);
=cut
=pod
# Tests group 3. Similar brackets.
# :-) forgot to add an if statement for this case :-)
# The $input19 works now :-)
my $input = '||';
my @cfg = (['|', '|']);
=cut
=pod
const config6 = [['1', '2'], ['3', '4'], ['5', '6'], ['7', '7'], ['8', '8']];


it('should check if brackets sequence is correct 15', () => {
  assert.equal(check('111115611111111156111111112222888888222255778777787755556666777777777766222221111222288888822225577877778775555666677777777776622222', config6), true);
});
=cut
# Tests group 5
#true
my $input15 = '111115611111111156111111112222888888222255778777787755556666777777777766222221111222288888822225577877778775555666677777777776622222';
my $input = $input15;
my @cfg = ( ['1', '2'], ['3', '4'], ['5', '6'], ['7', '7'], ['8', '8'] );


if (checkStr(\$input,\@cfg))
{
	say 'true';
}
else
{
	say 'false';
}

###########################################################################
#
#
#
sub checkStr
{
	my ($p_s, $p_cfg) = @_;

	my @sarr = split(//,$$p_s);
	my %different_brackets = ();
	my %similar_brackets = ();

	for(1..scalar(@$p_cfg))
	{
		my ($b, $brackets_pair) = $p_cfg->[$_-1];
		
		my ($o_bracket,$c_bracket) = ($b->[0],$b->[1]);

		#my ($o_id,$c_id) = (2 * $_, 2 * ($_ + 1));

		# Each bracket is coded with 5 and -5 for example
		my ($o_id,$c_id) = ( $_, -$_);

		# The brackets are the same. ['|','|'] for example
		if ($o_bracket eq $c_bracket)
		{
			# Check whether a bracket is in the hash already
			unless (exists($similar_brackets{$o_bracket}))
			{
				$similar_brackets{$o_bracket} = $o_id;
			}
		}
		# The brackets are different. ['(',')'] for example
		else
		{
			# There was no similar brackets before
			unless (
				exists($different_brackets{$o_bracket}) and 
				exists($different_brackets{$c_bracket})
			)
			{
				$different_brackets{$o_bracket} = $o_id;
				$different_brackets{$c_bracket} = $c_id;
			}
		}
	}

	my @brackets_stack = ();

	for(@sarr)
	{
		my $curr_input_char = $_;

		my $isMatch = StackPopIfMatched(
			$curr_input_char,
			\@brackets_stack,
			\%different_brackets,
			\%similar_brackets
		);

		# There is no a similar bracket on the stack's top
		unless($isMatch)
		{
			my $h = GetHashRefForChar(
				$_,
				\%different_brackets,
				\%similar_brackets
			);

			if (defined)
			{
				my $char_code = $h->{$_};
				#push(@brackets_stack,$_);
				push(@brackets_stack,$char_code);
			}
		}
	}

	print L Dumper @brackets_stack;

	# There are no unmatched brackets
	if (scalar(@brackets_stack) == 0)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}
###########################################################################
#
#		StackPopIfMatched(
#			$curr_input_char,
#			\@brackets_stack,
#			\%different_brackets,
#			\%similar_brackets
#		);
#
sub StackPopIfMatched
{
	my $out_result = 0;

	my(
		$p_char,
		$pinout_brackets_stack,
		$p_different_brackets,
		$p_similar_brackets
	)
	=
	@_;

	my $hash_with_brackets = GetHashRefForChar(
		$p_char,
		$p_different_brackets,
		$p_similar_brackets
	);


	if (defined($hash_with_brackets))
	{
		my $stack_top = undef;

		# a stack is not empty
		if (scalar(@$pinout_brackets_stack))
		{
			$stack_top = @$pinout_brackets_stack[-1];

			my $stack_bracket_code = $stack_top;
			my $input_bracket_code = $hash_with_brackets->{$p_char};

			# The codes are like -5 and +5
			# It is a matched pair of brackets
			if ($stack_bracket_code + $input_bracket_code == 0)
			{
				# And there is an open bracket on the top of a stack
				if ($stack_bracket_code > 0)
				{
					# Let's remove an open bracket as we have a 'good' 
					# matched pair
					pop(@$pinout_brackets_stack);


					$out_result = 1;
				}
			}
			# If the brackets are similar
			# and their codes are equal
			# Let's remove a bracket from the top
			elsif (
				$hash_with_brackets == $p_similar_brackets and # it is a hack! :-)
				$stack_bracket_code == $input_bracket_code
			)
			{
					pop(@$pinout_brackets_stack);
					$out_result = 1;
			}
		}
	}
}
###########################################################################
#
#		my $h = GetHashRefForChar(
#			$_,
#			\%different_brackets,
#			\%similar_brackets
#		);
#
sub GetHashRefForChar
{
	my $lout_hash_ref = undef;

	my($p_char, $p_different_brackets, $p_similar_brackets) = @_;

	if (exists($p_different_brackets->{$p_char}))
	{
		$lout_hash_ref = $p_different_brackets;
	}
	elsif (exists($p_similar_brackets->{$p_char}))
	{
		$lout_hash_ref = $p_similar_brackets;
	}

	return $lout_hash_ref;
}