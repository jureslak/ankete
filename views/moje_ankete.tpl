%rebase("okvir.tpl", loggedin=loggedin)

<table class="seznam_anket">
  <tr>
    <th>Naslov</th>
    <th>Uvod</th>
  </tr>
  %for i in data:
    %a = list(i)
    <tr>
      <td><a href="/moje_ankete/{{a[0]}}/">{{a[1]}}</a></td>
      <td>{{a[2]}}</td>
    </tr>
  %end
</table>
