% example from Marianne Huchard

:-
arancini : [ arancini, dish, hasMainCereal arborioRice ],
gardiane : [ gardiane, dish, hasMainCereal arborioRice & redRice ],
khaoManKai : [ khaoManKai, dish, hasMainCereal thaiRice ],
biryani : [ biryani, dish, hasMainCereal basmatiRice ],

redRice : [ redRice, cereal, rice, isProducedIn France ],
arborioRice : [ arborioRice, cereal, rice, isProducedIn Italy ],
basmatiRice : [ basmatiRice, cereal, rice, isProducedIn Pakistan ],
thaiRice : [ thaiRice, cereal, rice, isProducedIn Thailand ],

Italy : [ Italy, Europe, country ],
France : [ France, Europe, country ],
Thailand : [ Thailand, Asia, country, eatLotOf khaoManKai ],
Pakistan : [ Pakistan, Asia, country, eatLotOf biryani ]
.