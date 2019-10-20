use strict;
use 5.010;
use Data::Dumper;

# a config
my %config;
init_config(\%config);

# an event transision rules hash
my %event_transition_rules;
{
	my $states_desc = $config{'states'};
	init_event_transition_rules($states_desc, \%event_transition_rules);
}

my $init_state = $config{'initial'};

# a transition table
my @transition_history;

# 
my $curr_tran_hist_index = undef;

clearHistory();

=pod
# Tests groud p 1
print getState();
trigger('study');
print getState();

#print Dumper getStates();
#print Dumper @transition_history;
=cut

=pod
# Tests group N 2
say getState();
changeState('busy');
say getState();
trigger('get_tired');
say getState();

changeState('busy');
trigger('get_hungry');
say getState();
=cut

=pod
# Tests group N 3
say join(', ' ,getStates('get_hungry'));
=cut

=pod
# Tests group N 4
trigger('study');
Undo();
Redo();
print getState(); # busy

trigger('get_tired');
trigger('get_hungry');

Undo();
Undo();

Redo();
Redo();

print getState(); # hungry
=cut

trigger('study');
Undo();
Redo();
say getState(); # busy

trigger('get_tired');
trigger('get_hungry');

Undo();
say getState();
say q(changeState('normal'));
changeState('normal');

say Redo();
say getState();

say Redo();
say getState();



###########################################################################
# 'Member' functions
###########################################################################
###########################################################################
#
#	my $isOK = CheckTranHistIndex;
#
sub CheckTranHistIndex
{
=pod
	say $curr_tran_hist_index;

	#my $v = ( defined($curr_tran_hist_index) );

	my $v = $curr_tran_hist_index;

#	and	$curr_tran_hist_index >= 0 );
#		and		$curr_tran_hist_index <= $#transition_history );

	my $a = $#transition_history;

	say "v = $v; tran_hist_index: $a";
=cut
	return ( defined($curr_tran_hist_index) and
		$curr_tran_hist_index >= 0 and
		$curr_tran_hist_index <= $#transition_history );



}
###########################################################################
#
#	my $isSuccess = undo();
#
sub Redo
{
	my $isSuccess = 0;

	my $last_index = $#transition_history;
	if ($curr_tran_hist_index < $last_index)
	{
		$curr_tran_hist_index++;
		$isSuccess = 1;
	}

	return $isSuccess;
}
###########################################################################
#
#	my $isSuccess = undo();
#
sub Undo
{
	my $isSuccess = 0;
	if (defined($curr_tran_hist_index) and $curr_tran_hist_index != 0)
	{
		$curr_tran_hist_index--;
		$isSuccess = 1;
	}

	return $isSuccess;
}
###########################################################################
#
sub getState
{
	unless ( CheckTranHistIndex() )
	{
		die '[getState] $curr_tran_hist_index is wrong';
	}

	my $state = $transition_history[$curr_tran_hist_index];

	return $state;
};
###########################################################################
#
sub clearHistory
{
	@transition_history = ();
	push(@transition_history,$init_state);
	$curr_tran_hist_index = 0;
}
###########################################################################
#
sub reset
{
	#push(@transition_history,$init_state);	
	$curr_tran_hist_index = 0;
}
###########################################################################
#
sub getStates()
{
	my ($p_transition_rule) = @_;
	

	unless (defined($p_transition_rule) and $p_transition_rule ne '')
	{
		my $states = $config{'states'};
		return keys(%$states);
    }
    else
    {
    	my $t = \%event_transition_rules;
    	if (exists($t->{$p_transition_rule}))
    	{
    		my $state_from = $t->{$p_transition_rule}->{'state_from'};

    		return keys(%$state_from);
    	}
    }
}
###########################################################################
# changeState('busy')
sub changeState
{
	unless ( CheckTranHistIndex() )
	{
		die '[changeState] $curr_tran_hist_index is wrong';
	}
	
	# The algo:
	# Set a new state and rewrite a transition table 
	# if we are during Redo or Undo

	my ($p_new_state) = @_;

	return if ($p_new_state eq getState());

	my @states_list = getStates();

	if (grep(/$p_new_state/, @states_list) )
	{
		# Let's modify a transition history table

		my $last_index = $#transition_history;

		# We are not in Redo/Undo
		if ($curr_tran_hist_index == $last_index)
		{
			push(@transition_history,$p_new_state);
			$curr_tran_hist_index++;

		}
		else
		{
			# remove the states from the transition history table
			# from the current index position

			# todo: refactor it later :-)

			print Dumper @transition_history;

			my $a = \@transition_history;
			my $t = ++$curr_tran_hist_index;

			$a->[$t] = $p_new_state;

			my @arr_temp = @$a[0..$t];

			@transition_history = @arr_temp;
		}

		
		#$curr_tran_hist_index;
	}
}
###########################################################################
sub trigger
{
	my ($p_event_name) = @_;
	if ( exists($event_transition_rules{$p_event_name}) )
	{
		my $event_transition_desc = $event_transition_rules{$p_event_name};
		my $h = $event_transition_desc;

		my $curr_machine_state = getState();

		# It is possible to do a transition _from_ the current state
		if ( exists($h->{'state_from'}->{$curr_machine_state}) )
		{
			changeState($h->{'state_to_transit'});
		}

	}
}
###########################################################################
# init_config(\%config);
sub init_config
{
	my ($pout_config) = @_;

	my %config = (
		initial => 'normal',
		states => {
			normal => {
				transitions => {
					study => 'busy'
				}
			},
            busy => {
                transitions => {
                    get_tired => 'sleeping',
                    get_hungry => 'hungry'
                }
            },
            hungry => {
                transitions => {
                    eat => 'normal'
                }
            },
            sleeping => {
                transitions => {
                    get_hungry => 'hungry',
                    get_up => 'normal'
                }
            }
		}
	);

	%$pout_config = %config;
}
###########################################################################
# init_event_transition_rules($states_desc, \%event_transition_rules);
sub init_event_transition_rules
{
	my ($pin_states_desc, $pout_event_transition_rules) = @_;

	for my $state_name (sort keys %$pin_states_desc)
	{
		# it is a helper line above ;-)		
		# say "state_from: $state_name";
		my $state_transitions = $pin_states_desc->{$state_name}->{'transitions'};
    
		for my $event_name (keys %$state_transitions)
		{
			my $state_to_transit = $state_transitions->{$event_name};
			# it is a helper line above ;-)
			# say "evet_name: $event_name state_to: $state_to_transit";
    
			# There is no $event_name in transition rules.
			# Let's add it! :-)
			unless ( exists $event_transition_rules{$event_name} )
			{
				my %event_desc = (
					state_to_transit => $state_to_transit,
					state_from => {$state_name => 1}
				);
    
				$event_transition_rules{$event_name} = \%event_desc;
			}
			else {
				# We've already added a from state
				# Let's add another from state for the event
				my $t = $event_transition_rules{$event_name}->{'state_from'};
				$t->{$state_name} = 1;
			}
		}
	}
}