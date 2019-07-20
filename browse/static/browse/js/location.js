var deliveryLocation = (function () {
	// =============================
	// Private methods and propeties
	// =============================
	let location_data = ['', ''];//coord, name


	// Save location
	function saveLocation() {
		localStorage.setItem('deliveryLocation', JSON.stringify(location_data));
	}

	// Load location
	function loadlocation() {
		location_data = JSON.parse(localStorage.getItem('deliveryLocation'));
	}

	if (localStorage.getItem("deliveryLocation") != null) {
		loadlocation();
		// console.log(location_data);
	}


	// =============================
	// Public methods and propeties
	// =============================
	var obj = {};

	// Add to location
	obj.setlocation = function (coord) {
		location_data[0] = coord;
		saveLocation();
		return true;
	};

	// Add to location
	obj.setlocationName = function (name) {
		location_data[1] = name;
		saveLocation();
		return true;
	};

	// Add to location
	obj.set = function (coord, name) {
		location_data = [coord, name];
		saveLocation();
		return true;
	};

	// Clear location
	obj.clearlocation = function () {
		location_data = ['', ''];
		saveLocation();
	};

	// Load
	obj.getlocation = function () {
		loadlocation();
		return location_data[0];
	};

	obj.getlocationName = function () {
		loadlocation();
		return location_data[1];
	};

	// Load
	obj.get = function () {
		loadlocation();
		return location_data;
	};

	return obj;
})();


// -------------------------------------------------------------
function loadDeliveryLocation() {
	document.getElementById('delivery_area_srch').value = deliveryLocation.get()[0];
	document.getElementById('delivery_input').value = deliveryLocation.get()[1];
}

$('.hotelsearchBox').one("click", ".hotelsearchButton", function (event) {
	event.preventDefault();
	console.log('button clicked');
	deliveryLocation.clearlocation();
	deliveryLocation.set(document.getElementById('delivery_area_srch').value, document.getElementById('delivery_input').value);
	$(this).trigger(event.type);
});
$('.hotelsearchBox').one("submit", ".hotelsearchButton", function (event) {
	event.preventDefault();
	console.log('button submitted');
	deliveryLocation.clearlocation();
	deliveryLocation.set(document.getElementById('delivery_area_srch').value, document.getElementById('delivery_input').value);
	$(this).trigger(event.type);
});

loadDeliveryLocation();