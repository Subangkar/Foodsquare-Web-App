// var deliveryLocation = (function () {
// 	// =============================
// 	// Private methods and propeties
// 	// =============================
// 	var location_data = ['', ''];//coord, name
//
//
// 	// Save location
// 	function saveLocation() {
// 		localStorage.setItem('deliveryLocation', JSON.stringify(location_data));
// 	}
//
// 	// Load location
// 	function loadlocation() {
// 		location_data = JSON.parse(localStorage.getItem('deliveryLocation'));
// 	}
//
// 	if (localStorage.getItem("deliveryLocation") != null) {
// 		loadlocation();
// 		// console.log(location_data);
// 	}
//
//
// 	// =============================
// 	// Public methods and propeties
// 	// =============================
// 	var obj = {};
//
// 	// Add to location
// 	obj.set = function (coord, name) {
// 		location_data = [coord, name];
// 		saveLocation();
// 		return true;
// 	};
//
// 	// Clear location
// 	obj.clear = function () {
// 		location_data = ['', ''];
// 		saveLocation();
// 	};
//
// 	// Load
// 	obj.get = function () {
// 		loadlocation();
// 		return location_data;
// 	};
//
// 	return obj;
// })();


// -------------------------------------------------------------
function loadDeliveryLocation() {
	document.getElementById('delivery_area_srch').value = deliveryLocation.get()[0];
	document.getElementById('delivery_input').value = deliveryLocation.get()[1];
	console.log("Location loaded: " + deliveryLocation.get()[0] + " - " + deliveryLocation.get()[1]);
}


var is_searched = false;
// $('.hotelsearchBox').off("click submit", ".hotelsearchButton").on("click submit", ".hotelsearchButton", function (event) {
// 	if (is_searched) return;
// 	event.preventDefault();
// 	const location_name = document.getElementById('delivery_input').value;
// 	if (!location_name) {
// 		deliveryLocation.clear();
// 		return true;
// 	}
// 	var isValid = false;
// 	areas.forEach(function (value, index, array) {
// 		if (value.display_name.toUpperCase() === location_name.trim().toUpperCase()) {
// 			document.getElementById('delivery_area_srch').value = value.co_ordinates;
// 			console.log('updating to ' + location_name);
// 			return isValid = true;
// 		}
// 	});
// 	if (!isValid && location_name) {
// 		alert("Not a valid location !!!");
// 		return false;
// 	}
// 	deliveryLocation.set(document.getElementById('delivery_area_srch').value, document.getElementById('delivery_input').value);
// 	is_searched = true;
// 	$(this).trigger(event.type);
// });


// $('#delivery_input').keyup(function (event) {
// 	if (event.keyCode === 13) $('.hotelsearchButton').click();
// });
loadDeliveryLocation();