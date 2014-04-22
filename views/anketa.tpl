%rebase("okvir.tpl", loggedin=loggedin)

%for i in data:
  %i = { ("id", "naslov", "vprasanja", "tip", "vrstni_red")[j]:k for j,k in enumerate(list(i))}
  %print(i)
  <div class="vprasanje" id="vprasanje{{i['id']}}" data-tip="{{i['tip']}}" data-vprasanja="{{!i['vprasanja']}}">
    <div style="min-height:125px;">
      <form>  
        <span id="vprasanje{{i['id']}}_text">{{!i["naslov"]}} </span> <br/>
        %if i["tip"] == "text":
          <input type="text" />
        %elif i["tip"] == "radiobutton":
          %selected_first=True
          %for j in i["vprasanja"].split('\n'):
            <input name="vpr{{i['id']}}" type="radio" 
            %if selected_first: 
              checked='checked'
              %selected_first=False
            %end
            />{{!j}}<br/>
          %end
        %end
      </form>
    </div>
    <div class="vprasanje_moznosti">
      <button onclick="uredi({{i['id']}})">Uredi</button>
      <button>Izbrisi</button>
    </div>
  </div>
%end
<div id="urejanje_ozadje" style="display:none;">
  <div id="urejanje">
    Vprasanje <span id="id_vprasanje"></span>
    <div>
      <form>
        Tip:
        <select id="tip">
          %for i in tipi:
            <option>{{i}}</option>
          %end
        </select>
        <br/>
        Naslov: <input type="text" id="naslov" value=""/>
        <br/>
        <textarea style="display:none" id="seznam"></textarea>
      </form>
    </div>
    <div id="urejanje_placeholder">
    </div>
    <div>
      <button onclick="">Shrani</button>
      <button onclick="zapri()">Zapri</button>
    </div>
  </div>
</div>
