function update_captions(){
  if(window.innerWidth < 520){
    captions = [
    "<span style='display:inline-block;line-height:7px;vertical-align:middle'>Stranger</span>",
    "<span style='display:inline-block;line-height:7px;vertical-align:middle'>Classmate</span>",
    "<span style='display:inline-block;line-height:7px;vertical-align:middle'>Neighboring girl</span>",
    "<span style='display:inline-block;line-height:7px;vertical-align:middle'>SMS receiver</span>",
      "<span style='display:inline-block;line-height:7px;vertical-align:middle'>morning Morning</span>",
      "<span style='font-size:7px;display:inline-block;line-height:7px;vertical-align:middle'>Mengmeng</span>",
      "<span style='font-size:7px'>girl friend</span>", "Lover",
      "<span style='font-size:7px'>Cutie 18</span>", "Duoduo", "Babe",
      "<span style='font-size:smaller'>Duobao</span>",
      "<span style='font-size:smaller'>Wife</span>", "Lifelong", "Forever"];
    captions_rel = ["<span style='font-size:9px;'>Relationship</span>",
      "<span style='font-size:7px;'>Break-up</span>"];
  }
  else{
    captions = [
    "<span style='font-size:13px;display:inline-block;line-height:13px;vertical-align:middle'>Stranger</span>",
    "<span style='font-size:13px;display:inline-block;line-height:13px;vertical-align:middle'>Classmate</span>",
    "<span style='font-size:13px;display:inline-block;line-height:13px;vertical-align:middle'>Neighboring girl</span>",
    "<span style='font-size:13px;display:inline-block;line-height:13px;vertical-align:middle'>SMS receiver</span>",
      "<span style='font-size:13px;display:inline-block;line-height:13px;vertical-align:middle'>morning Morning</span>",
      "<span style='font-size:13px;display:inline-block;line-height:13px;vertical-align:middle'>Mengmeng</span>",
      "<span style='font-size:13px'>girl friend</span>", "Lover",
      "<span style='font-size:13px'>Cutie 18</span>", "Duoduo", "Babe",
      "<span style='font-size:smaller'>Duobao</span>",
      "<span style='font-size:smaller'>Wife</span>", "Lifelong", "Forever"];
    captions_rel = ["<span style='font-size:15px;'>Relationship</span>",
      "<span style='font-size:13px;'>Break-up</span>"];
  }
}

var span_en;

function create_switch_en(){
  span_en = document.createElement('div');
  span_en.style.position = "absolute";
  span_en.style.top = "0";
  if(window.innerWidth < 520)
    span_en.style.fontSize = "10px";
  else
    span_en.style.fontSize = "small";
  span_en.style.backgroundColor = "#8f7a66";
  span_en.style.borderRadius = "0 0 3px 3px";
  span_en.style.padding = "3px 10px";
  span_en.style.color = "white";
  span_en.style.cursor = "pointer";
  span_en.onclick = play_in_english;
  span_en.textContent = "🇬🇧 Switch to English";
  var container = document.querySelector('.container');
  container.insertBefore(span_en, container.firstChild);
}

var span_zh;

function create_switch_zh(){
  span_zh = document.createElement('div');
  span_zh.style.position = "absolute";
  span_zh.style.top = "0";
  if(window.innerWidth < 520)
    span_zh.style.fontSize = "10px";
  else
    span_zh.style.fontSize = "small";
  span_zh.style.backgroundColor = "#8f7a66";
  span_zh.style.borderRadius = "0 0 3px 3px";
  span_zh.style.padding = "3px 10px";
  span_zh.style.color = "white";
  span_zh.style.cursor = "pointer";
  span_zh.onclick = play_in_chinese;
  span_zh.textContent = "中文版";
  var container = document.querySelector('.container');
  container.insertBefore(span_zh, container.firstChild);
}

function play_in_english(){
  update_captions();
  window.addEventListener('resize', update_captions, true);

  caption_garbage = "<span style='font-size:smaller'>Air</span>";
  window.game.actuate();

  game_title = "Mengmeng";
  game_alt_title = "Love";
  result_msg = "You got a ";
  var titleElem = document.getElementById('title');
  if(titleElem.textContent != "Love") titleElem.textContent = game_title;
  document.querySelector('.restart-button').textContent = "Drop out";
  document.querySelector('.retry-button').textContent = "Try again";
  document.querySelector('.game-explanation').innerHTML = "<strong class='important'>How to play:</strong> Use your <strong>arrow keys</strong> to move the bricks. When two bricks of the same type touch, they <strong>merge into one!</strong><br>However, your action and work may not always work &mdash; they may produce the sticky <strong>air</strong>, which is resistant to moves. Two air bricks vanish when they touch. You will stop producing air after getting a <strong>girl friend</strong> (except for one more piece to help you eliminate any existing air).<br>A <strong>relationship</strong> upgrades any brick it touches for the first time. The brick shows the number of times you have benefited from it. When the 10-sec relationship ends, it will become a <strong>break-up</strong> (or garbage if you didn't use it), which downgrades bricks until you have repaid the benefits.";

  if(span_en) span_en.parentNode.removeChild(span_en);
  create_switch_zh();
  window.game.storageManager.storage.setItem('lang', 'en');
}

var zh_var = null;

function determine_zh_var(){
  if(zh_var) return zh_var;
  var hant_locales = ['zh-hant', 'zh-tw', 'zh-hk', 'zh-mo'];
  var nav_langs = navigator.languages;
  var hant_fallback = false;
  if(nav_langs){
    for(var i=0; i<nav_langs.length; i++){
      var nav_lang = nav_langs[i].toLowerCase();
      if(nav_lang.startsWith('zh-')){
        zh_var = hant_locales.indexOf(nav_lang) >= 0 ? "hant" : "hans";
        break;
      }
      else if(nav_lang.startsWith('ja-') || nav_lang.startsWith('ko-')) hant_fallback = true;
    }
  }
  else{
    var nav_lang = navigator.language || navigator.userLanguage;
    if(nav_lang){
      nav_lang = nav_lang.toLowerCase();
      if(nav_lang.startsWith('zh-'))
        zh_var = hant_locales.indexOf(nav_lang) >= 0 ? "hant" : "hans";
      else if(nav_lang.startsWith('ja-') || nav_lang.startsWith('ko-')) hant_fallback = true;
    }
  }
  if(!zh_var) zh_var = hant_fallback ? "hant" : "hans";
  return zh_var;
}

function use_simplified(){
  captions = ["陌生人", "同学",
  "邻班妹子", 
  "<span style='display:inline-block;line-height:25px;vertical-align:middle'>SMS另一端</span>",
  "<span style='display:inline-block;line-height:25px;vertical-align:middle'>情书收信人</span>",
  "<span style='display:inline-block;line-height:30px;vertical-align:middle'>早安<br>晨曦</span>",
   "孟孟","女朋友", "Lover", 
   "<span style='display:inline-block;line-height:22px;vertical-align:middle'>十八岁小可爱</span>",
    "朵朵", "宝贝",
"朵宝", "老婆", "一生一世", "forever"];
  captions_rel = ["恋爱", "分手"];
  caption_garbage = "空气";
  game_alt_title = "Love Rush";
  window.game.actuate();

  document.querySelector('.restart-button').textContent = "重新恋爱";
  document.querySelector('.retry-button').textContent = "再试一次";
  document.querySelector('.game-explanation').innerHTML = "<strong class='important'>玩法:</strong> 使用方向键谈恋爱. 当两块相同的爱心方块碰在一起时, <strong>它们会组成一块更好的方块</strong>! <br>但是, 你的行动和付出也可能只是产生<strong>空气</strong>. 连接的空气会阻碍方块的移动, 直到被别的空气击中而消失. 你得到 <strong>女朋友</strong> 以后便不会再产生空气, 最多再来一块帮你清除别的空气.<br><strong>恋爱</strong>砖触碰任何砖都能使其升级, 但一块砖只可享受一次. 恋爱砖上会显示你使用它的次数; 10 秒后它会变成<strong>分手</strong>砖, 触碰任何砖都能使其降级, 以此来偿还之前使用的次数.";
}

function use_traditional(){
  captions = ["陌生人", "同学",
  "邻班妹子", 
  "<span style='display:inline-block;line-height:25px;vertical-align:middle'>SMS另一端</span>",
  "<span style='display:inline-block;line-height:25px;vertical-align:middle'>情书收信人</span>",
  "<span style='display:inline-block;line-height:30px;vertical-align:middle'>早安<br>晨曦</span>",
   "孟孟","女朋友", "Lover", 
   "<span style='display:inline-block;line-height:22px;vertical-align:middle'>十八岁小可爱</span>",
    "朵朵", "宝贝",
"朵宝", "老婆", "一生一世", "forever"];
  captions_rel = ["戀愛", "分手"];
  caption_garbage = "空气";
  game_alt_title = "愛";
  window.game.actuate();

  document.querySelector('.restart-button').textContent = "重新恋爱";
  document.querySelector('.retry-button').textContent = "再试一次";
  document.querySelector('.game-explanation').innerHTML = "<strong class='important'>玩法:</strong> 使用方向键谈恋爱. 当两块相同的爱心方块碰在一起时, <strong>它们会组成一块更好的方块</strong>! <br>但是, 你的行动和付出也可能只是产生<strong>空气</strong>. 连接的空气会阻碍方块的移动, 直到被别的空气击中而消失. 你得到 <strong>女朋友</strong> 以后便不会再产生空气, 最多再来一块帮你清除别的空气.<br><strong>恋爱</strong>砖触碰任何砖都能使其升级, 但一块砖只可享受一次. 恋爱砖上会显示你使用它的次数; 10 秒后它会变成<strong>分手</strong>砖, 触碰任何砖都能使其降级, 以此来偿还之前使用的次数.";

  document.body.style.fontFamily = '"Clear Sans", "Helvetica Neue", Arial, "Hiragino Sans CNS", "PingFang TC", "Microsoft JhengHei", "Source Han Sans TC", "Noto Sans CJK TC", sans-serif';
}

function play_in_chinese(){
  window.removeEventListener('resize', update_captions, true);
  game_title = "Mengmeng";
  result_msg = "你得到了";
  var titleElem = document.getElementById('title');
  if(titleElem.textContent != "Love") titleElem.textContent = game_title;

  if(determine_zh_var() == 'hant') use_traditional();
  else use_simplified();

  if(span_zh) span_zh.parentNode.removeChild(span_zh);
  create_switch_en();
  window.game.storageManager.storage.setItem('lang', 'zh');
}
