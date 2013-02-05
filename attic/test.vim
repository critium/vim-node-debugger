perl << EOF
sub mySub
{
  my $anArg=VIM::Eval("a:anArg");
  # some useful Perl stuff
  VIM::Msg('hellow');

  use IO::Socket;
  my $sock = new IO::Socket::INET (
  PeerAddr => 'localhost',
  PeerPort => '5858',
  Proto => 'tcp',
  );
  die "Could not create socket: $!\n" unless $sock;
  #my jsonString = '{\"seq\":1,\"type\":\"request\",\"command\":\"continue\"}'
  my $jsonString = '{hellow}';

  print $sock $jsonString;
  close($sock);
}
EOF

function! MyFunction(anArg)
  :/function
  perl mySub
endfunction
