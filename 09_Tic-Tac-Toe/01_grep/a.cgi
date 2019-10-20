my @arr=(10,20,30,1,2,3);

print 'OK' if (grep {$_==11} @arr);
print 'false' unless (grep {$_==11} @arr);

print grep {$_==11} @arr;
