use strict;
use 5.010;
use POSIX;
use Data::Dumper;

#my $input = '93 - 42 / (  -80.2 * 45 + 46 + (  66 * 45 - 26 * 0 * 84.5  )  ) - (  (  20 - 59 - 18 - 62  ) / (  9 / 90 * 16 - 6  ) * 3  )';
#my $input = '(2+3)*(4+5)-6';
my $input = '93 - 42 / (  80 * 45 + 46 + (  66 * 45 - 26 * 0 * 84  )  ) - (  (  20 - 59 - 18 - 62  ) / (  9 / 90 * 16 - 6  ) * 3  )';

my $tokens_arr = GetTokens(\$input);
my $RPNExpr_arr = ConvertToRPN($tokens_arr);

# Assume there are left associative operators! :-)
my %BINARY_OPERATORS = (
	'+' => 5,
	'-' => 5,
	'*' => 10,
	'/' => 10
);

print CalcRPNExpression($RPNExpr_arr);

###########################################################################
#
#
#
sub CalcRPNExpression
{
	my ($p_rpn) = @_;

	my @stack = ();

	for my $item (@$p_rpn)
	{
		#say $item;
		# an item is NOT an operator (it is a number, a function for example)
		unless(exists($BINARY_OPERATORS{$item})) 
		{
			push(@stack,$item);
		}
		else
		{
			# an item IS an operator
			my $top = pop(@stack);
			my $top_under = pop(@stack);

			my $res = ApplyBinaryOperatorToArguments($item, $top_under, $top);
			push(@stack,$res);
		}
	}

	return $stack[0];
}
###########################################################################
#
#
#
sub ApplyBinaryOperatorToArguments
{
	my($p_op,$p_arg1,$p_arg2) = @_;
	return eval("$p_arg1 $p_op $p_arg2");
}
###########################################################################
#
# my $tokens_arr = GetTokens(\$input);
#
sub GetTokens
{
	my($p_input) = @_;

	$$p_input =~ s/\s//g;

	my @pre_tokens = ($$p_input =~ /([^\d]*)(\d*[.]?\d*)/g);
	
	# ^^^
	# Array items with odd indexes are numbers
	# Array items with even indexes are brackets and operators
	# Amount of items is an ODD number

	my @out_tokens = ();

	# Let's convert even elements into single chars! :-)
	for(0..$#pre_tokens/2)
	{
		my $even_item = $pre_tokens[2*$_];
		my $odd_item = $pre_tokens[2*$_ + 1];

		my @temp_arr = split(//,$even_item);

		my $isFirstPreToken = ($_ == 0);
		MarkUnaryOperators(\@temp_arr,$isFirstPreToken);

	   	# google: perl how to join two arrays
	   	# url: https://www.oreilly.com/library/view/perl-cookbook/1565922433/ch04s10.html

	   	push(@out_tokens, @temp_arr) if (scalar(@temp_arr) > 0);
	   	push(@out_tokens, $odd_item) if ($odd_item ne '');
	   	
	}

	return \@out_tokens;
}
###########################################################################
#
#	MarkUnaryOperators(\@temp_arr);
#
sub MarkUnaryOperators
{
=pod
	# implement it later

	my ($p_operators_arr,$p_isFirstPreToken) = @_;

	my $p = p_operators_arr;

	my $size = scalar(@$p);

	# Let's check a unary sign in the start of an input string
	if (size == 1 and $p_isFirstPreToken)
	{
	}

	if (scalar(@$p)>2)
	{
		my $last = $p->[-1];
		if ($last eq '+' or $last eq '-')
		{
			my ($char_before_sign,$c) = $p->[-2];

			if ($c eq )
		}
	}
=cut
}
###########################################################################
#
# my $RPNExpr_test = ConvertToRPN($tokens_arr);
#
sub ConvertToRPN
{
	# url: http://algolist.manual.ru/syntax/revpn.php
	# АЛГОРИТМ (БЕЗ УНАРНЫХ + И -)
=pod
<p>Во-втоpых,  получение обpатной польской записи из исходного
выpажения может осуществляться весьма пpосто на основе
пpостого алгоpитма, пpедложенного Дейкстpой. Для этого
вводится понятие стекового пpиоpитета опеpаций(табл. 1):</p>
<pre>        Таблица 1
|----------|-----------|
| Опеpация | Пpиоpитет |
|----------|-----------|
|    (     |     0     |
|    )     |     1     |
|   +|-    |     2     |
|   *|/    |     3     |
|   **     |     4     |
|----------|-----------|
</pre>                            
<p>   Пpосматpивается исходная стpока символов слева напpаво, 
опеpанды пеpеписываются в выходную стpоку,  а знаки опеpаций
заносятся в стек на основе следующих сообpажений:</p>

<p>  а) если стек пуст,  то опеpация из входной стpоки
     пеpеписывается в стек;</p>
<p>  б) опеpация выталкивает из стека все опеpации с большим
     или pавным пpиоpитетом в выходную стpоку;</p>
<IMPORTANT>
	 И САМА ОПЕРАЦИЯ ПОМЕЩАЕТСЯ В СТЕК!
	 (АВТОР ПРЯМО НЕ НАПИСАЛ ОБ ЭТОМ)
</IMPORTANT>
<p>  в) если очеpедной символ из исходной стpоки есть
     откpывающая скобка,  то он пpоталкивается в стек;</p>
<p>  г) закpывающая кpуглая скобка выталкивает все опеpации из
     стека до ближайшей откpывающей скобки,  сами скобки в
     выходную стpоку не пеpеписываются,  а уничтожают
     дpуг дpуга. </p>
<IMPORTANT>
	В КОНЦЕ РАБОТЫ ВСЕ ОПЕРАЦИИ, ЧТО ЕСТЬ В СТЕКЕ ВЫТАЛКИВАЮТСЯ
	В ВЫХОДНУЮ СТРОКУ!
</IMPORTANT>

=cut
	my ($p_tokens_arr) = @_;
	my @out_RPN;

	my %PRIORITY = (
		'(' => 0,
		')' => 1,
		'+' => 2,
		'-' => 2,
		'*' => 3,
		'/' => 3
	);


	my @operators_stack = ();
	for my $token (@$p_tokens_arr)
	{
		my $isLeftBracket = ( $token eq '(' );
		my $isRightBracket = ( $token eq ')' );

		my $isOperator = ( $token =~ /[-+\*\/]/ );


		my $isNumber = ( $token =~ /\d/);
		my $isStackEmpty = ( scalar(@operators_stack) == 0 );

		if ($isNumber)
		{
			push(@out_RPN,$token);
		}

		if($isLeftBracket)
		{
			push(@operators_stack,$token);
		}


		if ($isStackEmpty and $isOperator)
		{
			push(@operators_stack,$token)
		}
		elsif($isOperator)
		{
			unless (exists($PRIORITY{$token}))
			{
				die '[ConvertToRPN] An uknown operator!';
			}

			# Let's pop all the operators with >= priority
			my $stack = \@operators_stack;
			while(scalar(@$stack))
			{
				my $top = $stack->[-1];
				if ( $PRIORITY{$top} >= $PRIORITY{$token} )
				{
					push(@out_RPN,pop(@$stack));
				}
				else
				{
					last;
				}

			}

			# Let's push an operator in the stack now.
			push(@operators_stack,$token);

		
		}
		elsif($isRightBracket)
		{
			my $stack = \@operators_stack;

			# Check the stack's size just in case ;-)
			while(scalar(@$stack))
			{
				my $top = $stack->[-1];
				if ($top eq '(')
				{
					# Let's remove the left bracket! :-)
					pop(@$stack);
					last;
				}
				else
				{
					push(@out_RPN,pop(@$stack));
					#push(@out_RPN,'x');
				}
			}
		}
	}

	# Let's empty the stack! :-)
	@operators_stack = reverse(@operators_stack);
	push(@out_RPN,@operators_stack);


	return \@out_RPN;
}