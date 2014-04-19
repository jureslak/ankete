%rebase("okvir.tpl", loggedin=loggedin)

%for i in data:
  %i=list(i)
  <div class="vprasanje" id="vprasanje{{i[0]}}" data-tip="{{i[2]}}">
    <form>  
      <span id="vprasanje{{i[0]}}_text">{{!i[1]}} </span>
      %if i[2] == "text":
        <input type="text" />
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
    Vprasanje <span id="id_vprasanje"></span>
    <div>
      Tip:
      <select>
        %for i in tipi:
          <option>{{i}}</option>
        %end
      </select>
    </div>
    <div id="urejanje_placeholder">
    </div>
    <div>
      <button onclick="">Shrani</button>
      <button onclick="zapri()">Zapri</button>
    </div>
  </div>
</div>
