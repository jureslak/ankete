% rebase("menu.tpl")
<ul>
% for v in vprasanja:
% v = list(v)
<li>{{!v}}</li>
% end
</ul>
