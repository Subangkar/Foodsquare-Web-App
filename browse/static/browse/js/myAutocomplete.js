function autocomplete(inp, arr) {
	// console.log(arr);
	/*the autocomplete function takes two arguments,
	the text field element and an array of possible autocompleted values:*/
	var currentFocus;
	/*execute a function when someone writes in the text field:*/
	inp.addEventListener("input", function (e) {
		var a, b, i, val = this.value;
		/*close any already open lists of autocompleted values*/
		closeAllLists();
		if (!val) {
			return false;
		}
		currentFocus = -1;
		/*create a DIV element that will contain the items (values):*/
		a = document.createElement("DIV");
		a.setAttribute("id", this.id + "autocomplete-list");
		a.setAttribute("class", "autocomplete-items");
		/*append the DIV element as a child of the autocomplete container:*/
		this.parentNode.appendChild(a);
		/*for each item in the array...*/
		for (i = 0; i < arr.length; i++) {
			// console.log(arr[i].display_name.substr(0, val.length).toUpperCase());
			/*check if the item starts with the same letters as the text field value:*/
			if (arr[i].display_name.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
				/*create a DIV element for each matching element:*/
				b = document.createElement("DIV");
				/*make the matching letters bold:*/
				b.innerHTML = "<strong>" + arr[i].display_name.substr(0, val.length) + "</strong>";
				b.innerHTML += arr[i].display_name.substr(val.length);
				/*insert a input field that will hold the current array item's value:*/
				b.innerHTML += "<input type='hidden' value='" + arr[i].display_name + "'>";
				b.innerHTML += "<input type='hidden' value='" + arr[i].co_ordinates + "'>";

				/*execute a function when someone clicks on the item value (DIV element):*/
				b.addEventListener("click", function (e) {
					/*insert the value for the autocomplete text field:*/
					inp.value = this.getElementsByTagName("input")[0].value;

					// hid.value = this.getElementsByTagName("input")[1].value;

					/*close the list of autocompleted values,
					(or any other open lists of autocompleted values:*/
					closeAllLists();
				});
				a.appendChild(b);
			}
		}
	});
	/*execute a function presses a key on the keyboard:*/
	inp.addEventListener("keydown", function (e) {
		var x = document.getElementById(this.id + "autocomplete-list");
		if (x) x = x.getElementsByTagName("div");
		if (e.keyCode == 40) {
			/*If the arrow DOWN key is pressed,
			increase the currentFocus variable:*/
			currentFocus++;
			/*and and make the current item more visible:*/
			addActive(x);
		} else if (e.keyCode == 38) { //up
			/*If the arrow UP key is pressed,
			decrease the currentFocus variable:*/
			currentFocus--;
			/*and and make the current item more visible:*/
			addActive(x);
		} else if (e.keyCode == 13) {
			/*If the ENTER key is pressed, prevent the form from being submitted,*/
			e.preventDefault();
			if (currentFocus > -1) {
				/*and simulate a click on the "active" item:*/
				if (x) x[currentFocus].click();
			}
		}
	});

	function addActive(x) {
		/*a function to classify an item as "active":*/
		if (!x) return false;
		/*start by removing the "active" class on all items:*/
		removeActive(x);
		if (currentFocus >= x.length) currentFocus = 0;
		if (currentFocus < 0) currentFocus = (x.length - 1);
		/*add class "autocomplete-active":*/
		x[currentFocus].classList.add("autocomplete-active");
	}

	function removeActive(x) {
		/*a function to remove the "active" class from all autocomplete items:*/
		for (var i = 0; i < x.length; i++) {
			x[i].classList.remove("autocomplete-active");
		}
	}

	function closeAllLists(elmnt) {
		/*close all autocomplete lists in the document,
		except the one passed as an argument:*/
		var x = document.getElementsByClassName("autocomplete-items");
		for (var i = 0; i < x.length; i++) {
			if (elmnt != x[i] && elmnt != inp) {
				x[i].parentNode.removeChild(x[i]);
			}
		}
	}

	/*execute a function when someone clicks in the document:*/
	document.addEventListener("click", function (e) {
		closeAllLists(e.target);
	});
}

/*An array containing all the country names in the world:*/
// var countries = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua & Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia & Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central Arfrican Republic","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cuba","Curacao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Namibia","Nauro","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","North Korea","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre & Miquelon","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","St Kitts & Nevis","St Lucia","St Vincent","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad & Tobago","Tunisia","Turkey","Turkmenistan","Turks & Caicos","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States of America","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"];
var areas = [{
	'display_name': 'Agargaon',
	'actual_name': 'Taltola',
	'co_ordinates': '23.7811642,90.3793618'
}, {'display_name': 'Armanitola', 'actual_name': 'Noorbagh', 'co_ordinates': '23.71494615,90.4021036961364'},
	{
		'display_name': 'Azimpur, Dhaka',
		'actual_name': 'Siddikbazar',
		'co_ordinates': '23.72290025,90.3859056043079'
	}, {
		'display_name': 'Banani DOHS',
		'actual_name': 'Banani',
		'co_ordinates': '23.7926587,90.3983848927147'
	}, {'display_name': 'Banasree', 'actual_name': 'Banasree', 'co_ordinates': '23.7645697,90.4268142'},
	{
		'display_name': 'Bangla bazar',
		'actual_name': 'Bangla Bazar',
		'co_ordinates': '23.7061272,90.4110565'
	}, {'display_name': 'Baridhara', 'actual_name': 'Banani', 'co_ordinates': '23.8032197,90.4194794'},
	{
		'display_name': 'Baridhara DOHS',
		'actual_name': 'Matikata',
		'co_ordinates': '23.81400995,90.4105504954163'
	}, {
		'display_name': 'Bashundhara Residential Area',
		'actual_name': 'Badda',
		'co_ordinates': '23.8139162,90.4291903'
	},
	{
		'display_name': 'East Nakhalpara',
		'actual_name': 'East Nakhalpara',
		'co_ordinates': '23.7675074,90.3973781'
	}, {
		'display_name': 'Farashganj',
		'actual_name': 'Dailpotti',
		'co_ordinates': '23.7030612,90.4175185'
	}, {
		'display_name': 'Hatirpool',
		'actual_name': 'Dhanmondi R/A',
		'co_ordinates': '23.7417837,90.3909892'
	}, {
		'display_name': 'Jhilmil Residential Area',
		'actual_name': 'Gopibag',
		'co_ordinates': '23.7036347,90.4235840261515'
	},
	{'display_name': 'Kallyanpur', 'actual_name': 'Taltola', 'co_ordinates': '23.7806848,90.3613321'},
	{
		'display_name': 'Kawran Bazar',
		'actual_name': 'East Nakhalpara',
		'co_ordinates': '23.7514308,90.3948605'
	}, {'display_name': 'Lalmatia', 'actual_name': 'Lalmatia', 'co_ordinates': '23.7567008,90.3691554'},
	{
		'display_name': 'Maghbazar',
		'actual_name': 'Mogbazar',
		'co_ordinates': '23.7509605,90.4049131643058'
	}, {
		'display_name': 'Malibagh',
		'actual_name': 'Dokkhin Shajahanpur',
		'co_ordinates': '23.7508251,90.4140763'
	}, {'display_name': 'Mirpur DOHS', 'actual_name': 'Harunabad', 'co_ordinates': '23.83685315,90.3697904577767'},
	{
		'display_name': 'Mohakhali DOHS',
		'actual_name': 'Niketan',
		'co_ordinates': '23.78075935,90.3952940558211'
	}, {
		'display_name': 'Nakhalpara',
		'actual_name': 'East Nakhalpara',
		'co_ordinates': '23.7675074,90.3973781'
	}, {
		'display_name': 'Narinda',
		'actual_name': 'Gopibag',
		'co_ordinates': '23.710897,90.4220765'
	}, {
		'display_name': 'New Market, Dhaka',
		'actual_name': 'Hazaribagh',
		'co_ordinates': '23.73330855,90.3828048040032'
	}, {'display_name': 'New Paltan', 'actual_name': 'Fakirapool', 'co_ordinates': '23.7306354,90.4117556'},
	{
		'display_name': 'Nilkhet',
		'actual_name': 'Nijhum Residential Area',
		'co_ordinates': '23.73155935,90.3877816302328'
	},
	{
		'display_name': 'Panthapath',
		'actual_name': 'Dhanmondi R/A',
		'co_ordinates': '23.7511561,90.3872285'
	}, {
		'display_name': 'Rajarbagh',
		'actual_name': 'TitiPara',
		'co_ordinates': '23.7404944,90.4171926485573'
	}, {
		'display_name': 'Shahbag',
		'actual_name': 'Fakirapool',
		'co_ordinates': '23.7380681,90.3960234'
	}, {'display_name': 'Shahjadpur', 'actual_name': 'Banani', 'co_ordinates': '23.7942325,90.4237343968813'},
	{
		'display_name': 'Shantinagar, Dhaka',
		'actual_name': 'Dokkhin Shajahanpur',
		'co_ordinates': '23.7416008,90.4118658'
	}, {
		'display_name': 'Tejturi Bazar',
		'actual_name': 'Pashcim Nakhalpara',
		'co_ordinates': '23.7553685,90.3907724'
	}, {'display_name': 'Tikatuli', 'actual_name': 'Gopibag', 'co_ordinates': '23.7194603,90.4205597113305'},]

/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
autocomplete(document.getElementById("delivery_input"), areas);


