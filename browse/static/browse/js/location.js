var deliveryLocation = (function () {
	// =============================
	// Private methods and propeties
	// =============================
	location = '';

	// Constructor
	function Location(coord) {
		this.location = coord;
	}

	// Save location
	function saveLocation() {
		localStorage.setItem('deliveryLocation', JSON.stringify(location));
	}

	// Load location
	function loadlocation() {
		location = JSON.parse(localStorage.getItem('deliveryLocation'));
	}

	if (localStorage.getItem("deliveryLocation") != null) {
		loadlocation();
	}


	// =============================
	// Public methods and propeties
	// =============================
	var obj = {};

	// Add to location
	obj.setlocation = function (coord) {
		this.location = coord;
		saveLocation();
		console.log('set location');
		console.log(this.location);
		console.log(localStorage.getItem('deliveryLocation'));
		return true;
	};

	// Clear location
	obj.clearlocation = function () {
		location = '';
		saveLocation();
	};

	return obj;
});

function updateLocation() {
	// event.preventDefault();
	console.log('here>>>>');
	loc = document.getElementById('delivery_area_srch').value;
	deliveryLocation.setlocation(loc);
	console.log(localStorage.getItem('deliveryLocation'))
}


function setLocation() {
	document.getElementById('delivery_area_srch').value = localStorage.getItem('deliveryLocation');
	console.log("Value Set");
	console.log(localStorage.getItem('deliveryLocation'))
}


setLocation();