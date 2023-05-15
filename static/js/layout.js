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
