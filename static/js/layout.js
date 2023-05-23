
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

//ポップアップ
var dialog = document.getElementById('dialog');
var cover = document.getElementById('cover');
var btn = document.getElementById('btn');
var cancel = document.getElementById('cancel');
btn.addEventListener('click',function(){
    dialog.style.display = 'block';
    cover.style.display = 'block';
});
cancel.addEventListener('click', function(){
    dialog.style.display = 'none';
    cover.style.display = 'none';
});

//編集
var EditBtn = document.getElementById('edit');
var EditDialog = document.getElementById('EditDialog');
var EditCancel = document.getElementById('EditCancel');
var EditText = document.getElementById('EditText');
var Edit = document.getElementById('EditBtn')
EditBtn.addEventListener('click',function(){
    dialog.style.display = 'none';
    EditDialog.style.display = 'block'
    EditText.innerHTML = review;
});
EditCancel.addEventListener('click',function(){
    EditDialog.style.display = 'none'
    cover.style.display = 'none';
});

function confirmEdit(){
    alert("更新されました")
}
