function chooseIcon(debit) {
    // document.write(debit);
    var tableEle = document.getElementById("transactions-table");
    tableEle.getElementsByTagName("i").className = "fa fa-heart";
    // document.write(tableEle.getElementsByTagName("i"));
    if(debit == "1") {
        tableEle.getElementsByTagName("i").className = "fa fa-heart";
    }
}