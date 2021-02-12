var stamps = new Array(
    '10001', '10002', '10003', '10004', '10005', '10006', '10007', '10008', '10009', '10010',
    '10011', '10012', '10013', '10014', '10015', '10016', '10017', '10018', '10019', '10020',
    '10021', '10022', '10023', '10024', '10025', '10026', '10027', '10028', '10029', '10030',
    '10031', '10101', '10102', '10103', '10104', '10105', '10201', '10202', '10203', '10301',
    '10302', '10303', '10401', '10501', '10502', '10503', '10601', '10602', '10603', '10604',
    '10701', '10702', '10703', '10801', '10802', '10901', '10902', '11001', '11002', '11003',
    '11004', '11101', '11102', '11103', '11104', '11105', '11106', '11107', '11108', '11201',
    '11202', '11301', '11302', '11303', '11304', '11305', '11306', '11401', '11501', '11502',
    '11503', '11601', '11602', '11603', '11604', '11605', '11701', '11702', '11801', '11901',
    '11902', '12001', '12002', '12101', '12102', '12201', '12202', '12301', '12302', '12401',
    '12402', '12403', '12404', '12405', '12501', '12502')

var framed = true;
var iconLang = 'zh_cn';
var soundLang = 'jp'

$(document).ready(function() {
    refreshStamps();
    $('select.icon-lang-select').on('select2:select', function(e) {
        let langSelect = document.getElementById("icon-lang-select");
        iconLang = langSelect.options[langSelect.selectedIndex].value;
        refreshStamps();
    });
    $('select.icon-lang-select').select2({
        dropdownAutoWidth: true,
        width: 'auto',
        minimumResultsForSearch: -1
    });
    $('select.icon-lang-select').val(iconLang).trigger('change');

    $('select.sound-lang-select').on('select2:select', function(e) {
        let langSelect = document.getElementById("sound-lang-select");
        soundLang = langSelect.options[langSelect.selectedIndex].value;
        refreshStamps();
    });
    $('select.sound-lang-select').select2({
        dropdownAutoWidth: true,
        width: 'auto',
        minimumResultsForSearch: -1
    });
    $('select.sound-lang-select').val(soundLang).trigger('change');

    $('select.mode-select').on('select2:select', function(e) {
        let modeSelect = document.getElementById("mode-select");
        framed = (modeSelect.options[modeSelect.selectedIndex].value == "true") ? true : false;
        refreshStamps();
    });
    $('select.mode-select').select2({
        dropdownAutoWidth: true,
        width: 'auto',
        minimumResultsForSearch: -1
    });
    $('select.mode-select').val((framed) ? 'true' : 'false').trigger('change');
});

function refreshStamps() {
    document.getElementById('stamps').innerHTML = "";
    stamps.forEach(addStamp);
}

function addStamp(value) {
    var btn = document.createElement('button');
    var audio = document.createElement('audio');
    mode = (framed) ? 'framed' : 'normal'
    btn.innerHTML = `<img src="./stamps/img/${iconLang}/${mode}/${value}.png" />`;
    btn.onclick = function() {
        var audio = document.getElementById(value);
        audio.play();
    }

    audio.id = value;
    audioSrc = (['11102', '11103', '11104', '11105', '11106', '11107', '11108'].includes(value)) ? '11101' : value
    audio.src = `./stamps/sound/${soundLang}/${audioSrc}.wav`;

    var div = document.getElementById('stamps');
    div.appendChild(btn);
    div.appendChild(audio);
}