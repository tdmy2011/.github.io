function getInfo(){
	var txt = document.getElementById("message").value
	if (txt){
		alert("你的留言：" + txt + "，已提交成功")
	} else {
		alert("请输入你的留言");
	}
}