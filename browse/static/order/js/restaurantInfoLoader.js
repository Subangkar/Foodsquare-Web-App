document.getElementById("rest-name").onchange = function () {
	var sel = document.getElementById("rest-name");
	loadBranchLists(sel.options[sel.selectedIndex].text);
	loadFoodItemLists(sel.options[sel.selectedIndex].text);
};

clearDropDownList("rest-name");
var url = "allRestaurantList";
var xhr = new XMLHttpRequest();
xhr.open("GET", url, true);
xhr.onreadystatechange = function () {
	var sel = document.getElementById("rest-name");

	if (xhr.readyState === 4 && xhr.status === 200) {
		var json = JSON.parse(xhr.responseText);
		addRestDropDownList("rest-name", " \t ----- Select a Restaurant ----- ", 0);
		for (let i = 0; i < json.length; i++) {
			addRestDropDownList("rest-name", json[i].restaurant_name, json[i].id);
		}
		// sel.setAttribute("style","width: 350px;height:40px;font-size:0.25in;color:black");
		loadBranchLists(sel.options[sel.selectedIndex].text);
		loadFoodItemLists(sel.options[sel.selectedIndex].text);
	}
};
xhr.send();


function addRestDropDownList(drop_list, name, id) {
	var sel = document.getElementById(drop_list);
	sel.options[sel.options.length] = new Option(name, id);
}

function clearDropDownList(drop_list) {
	document.getElementById(drop_list).innerHTML = "";
}

/*
* [{"id":1,"restaurant_name":"Takeout"},{"id":2,"restaurant_name":"MadChef"},{"id":3,"restaurant_name":"Alfresco"}]*/


function loadBranchLists(restaurant_name) {
	clearDropDownList("rest-branch-name");
	// var url = "branchListForRestaurant";
	var url = "branchListForRestaurant?data=" + encodeURIComponent(JSON.stringify({
		"restaurant_name": restaurant_name
	}));
	var xhr = new XMLHttpRequest();
	xhr.open("GET", url, true);
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			var json = JSON.parse(xhr.responseText);
			// alert(xhr.responseText);
			for (let i = 0; i < json.length; i++) {
				addRestDropDownList("rest-branch-name", json[i].branch_name, json[i].id);
				// [{"id":3,"branch_name":"Dhanmondi","restaurant_id":3}]
			}
		}
	};
	xhr.send();
}


function loadFoodItemLists(restaurant_name) {
	clearDropDownList("food-item");
	// var url = "branchListForRestaurant";
	var url = "menuEntryForRestaurant?data=" + encodeURIComponent(JSON.stringify({
		"restaurant_name": restaurant_name
	}));
	var xhr = new XMLHttpRequest();
	xhr.open("GET", url, true);
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			var json = JSON.parse(xhr.responseText);
			// alert(xhr.responseText);
			for (let i = 0; i < json.length; i++) {
				addRestDropDownList("food-item", json[i].entry_name + '\t\t$' + json[i].price, json[i].id);
			}
		}
	};
	xhr.send();
}
