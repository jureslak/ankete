%rebase("okvir.tpl", loggedin=loggedin)
<b>CSSji tu ne delajo zaradi dodatnega slasha v URL-ju. Nekaj je treba narediti s funkcijo, ki vraca CSS fajle.</b>
%for i in data:
  {{list(i)}}
%end
