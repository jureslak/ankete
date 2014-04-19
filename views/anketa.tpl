%rebase("okvir.tpl", loggedin=loggedin)

%for i in data:
  <div class="vprasanje">
    <form>      
      %i=list(i)
      %if i[2] == "text":
        {{!i[1]}} <input type="text" />
      %end
    </form>
    <div class="vprasanje_moznosti">
      <button onclick="uredi({{i[0]}})">Uredi</button>
      <button>Izbrisi</button>
    </div>
  </div>
%end
<div id="urejanje_ozadje" style="display:none;">
  <div id="urejanje">
    Vprasanje {{i[0]}}
    <div>
      Tip:
      <select>
        <option>test</option>
      </select>
    </div>
    <div>
      <button onclick="">Shrani</button>
      <button onclick="zapri()">Zapri</button>
    </div>
  </div>
</div>
