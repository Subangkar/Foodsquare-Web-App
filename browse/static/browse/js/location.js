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
		return true;
	};

	// Clear location
	obj.clearlocation = function () {
		location = [];
		saveLocation();
	};

	return obj;
})();

function updateLocation() {
	loc = document.getElementById('hotelsearchButton').value;
	deliveryLocation.setlocation(loc);
}