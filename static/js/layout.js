//削除確認
function confirmDelete(isbn) {
    if (window.confirm("本当に削除しますか？")) {
        window.location.href = '/delete/' + isbn;
        alert("削除されました")
    }
    else{
        alert("キャンセルされました")
    }
}

//編集
function confirmEdit(isbn){
    window.location.href = '/edit/' + isbn;
    alert("更新されました")
}

//ポップアップ
var dialog = document.getElementById('dialog');
var cover = document.getElementById('cover');
var btn = document.getElementById('btn');
var cancel = document.getElementById('cancel');
var comment = document.getElementById('comment');
function popup(review){
    comment.textContent = review;
    dialog.style.display = 'block';
    cover.style.display = 'block';
}
cancel.addEventListener('click', function(){
    dialog.style.display = 'none';
    cover.style.display = 'none';
});