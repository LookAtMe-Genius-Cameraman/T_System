let language = 'en';

const language_list = [['de', 'Deutsch', 'germantrans'], ['en', 'English', 'englishtrans'], ['es', 'Espa&ntilde;ol', 'spanishtrans'], ['fr', 'Fran&ccedil;ais', 'frenchtrans'], ['it', 'Italiano', 'italiantrans'], ['tr', 'Türkçe', 'turkishtrans']];
// tr version added in the list.
//removeIf(production)
let translated_list = [];

//endRemoveIf(production)

function translate_text(lang) {
    let item;
    let content;
    let currenttrans = {};
    let translated_content = "";
    store_localdata('language', lang);
    language = lang;
    for (let lang_i = 0; lang_i < language_list.length; lang_i++) {
        if (language_list[lang_i][0] === lang) {
            currenttrans = eval(language_list[lang_i][2]);
            document.getElementById("translate_menu").innerHTML = language_list[lang_i][1];
        }
    }
    const All = document.getElementsByTagName('*');
    for (let i = 0; i < All.length; i++) {
        if (All[i].hasAttribute('translate')) {
            content = "";
            if (!All[i].hasAttribute('english_content')) {
                content = All[i].innerHTML;
                content.trim();
                All[i].setAttribute('english_content', content);
                //removeIf(production)
                item = {content: content};
                translated_list.push(item);
                //endRemoveIf(production)
            }
            content = All[i].getAttribute('english_content');
            translated_content = translate_text_item(content);

            All[i].innerHTML = translated_content;
        }
        //add support for placeholder attribut
        if (All[i].hasAttribute('translateph') && All[i].hasAttribute('placeholder')) {
            content = "";
            if (!All[i].hasAttribute('english_content')) {
                content = All[i].getAttribute('placeholder');
                content.trim();
                //removeIf(production)
                item = {content: content};
                translated_list.push(item);
                //endRemoveIf(production)
                All[i].setAttribute('english_content', content);
            }
            content = All[i].getAttribute('english_content');

            translated_content = translate_text_item(content);
            All[i].setAttribute('placeholder', translated_content)
        }
    }
}

function translate_text_item(item_text, withtag) {
    let currenttrans = {};
    let translated_content;
    let with_tag = false;
    if (typeof withtag !== "undefined") with_tag = withtag;
    for (let lang_i = 0; lang_i < language_list.length; lang_i++) {
        if (language_list[lang_i][0] === language) {
            currenttrans = eval(language_list[lang_i][2]);
        }
    }
    translated_content = currenttrans[item_text];
    if (typeof translated_content === 'undefined') translated_content = item_text;
    if (with_tag) {
        translated_content = "<span english_content=\"" + item_text + "\" translate>" + translated_content + "</span>";
    }
    return translated_content;
}
