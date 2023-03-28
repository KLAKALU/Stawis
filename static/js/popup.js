// ボタンエレメントを取得
button = $('#btn');

// クリックされたらポップアップ画面表示
button.click(function() {
    data = 'test'
    // 接続を行う
    $.ajax({
        url : '/popup/' + data,
        type: 'get'
    })
    // 接続が正常に行われた場合
    .done(function(data) {
        $('#popup').css('display', 'block')
        html = data;
        $('#popup-modal').html(html)
    })
})
