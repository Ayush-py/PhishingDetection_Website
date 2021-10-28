function transfer(){
	var tablink;
	chrome.tabs.getSelected(null,function(tab) {
	  tablink = tab.url;
		$("#p1").text(""+tablink);

		var xhr = new XMLHttpRequest();
		params="url="+tablink;

		var markup = "url="+tablink+"&html="+document.documentElement.innerHTML;

		xhr.onreadystatechange = function() {
    if( xhr.readyState==4 && xhr.status==200 ){
        console.log( xhr.responseText );
    }
};
		xhr.open("POST","http://localhost/EXTENSION/ClientServer.php");
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		xhr.send(markup);
		xhr.onload = function (e) {
    if (xhr.readyState === 4) {
    if (xhr.status === 200) {
			label1 = document.getElementById('label1');
			p1 = document.getElementById('p1');
			div2 = document.getElementById('div2');
			p1.remove();
			label1.style.padding = '160px 0px 10px 95px';
			label1.innerHTML = ("This URL is:  ");
      if(xhr.responseText == "PHISHING"){
			 div2.innerHTML =	("Beware, looks like we caught a Phish");
			 div2.style.padding = '10px 0px 10px 40px';
			 div2.style.fontWeight = '600';
			 div2.style.color = 'white';
			}
			if(xhr.responseText == "SAFE")
			{
				div2.innerHTML =	("Keep surfing, the waters seems safe");
				div2.style.padding = '10px 0px 10px 50px';
				div2.style.fontWeight = '600';
				div2.style.color = 'white';
			}
      $("#div1").text(xhr.responseText);
    } else {
      console.error(xhr.statusText);
    }
  }
};
    console.log("result");
		$("#div1").text(xhr.responseText);
		return xhr.responseText;
	});
}


$(document).ready(function(){
    $("button").click(function(){
		var val = transfer();
    });
});

chrome.tabs.getSelected(null,function(tab) {
   	var tablink = tab.url;
	$("#p1").text(""+tablink);
});
