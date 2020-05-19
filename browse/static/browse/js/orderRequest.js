var order_now = document.getElementById("order_now");
order_now.addEventListener("click", function () {
		var order_type = document.getElementById("order-type");
		var food_item = document.getElementById("food-item");
		var rest_name = document.getElementById("rest-name");
		var rest_branch_name = document.getElementById("rest-branch-name");
		var delivery_time = document.getElementById("delivery_time");
		var delivery_addr = document.getElementById("delivery_addr");
		var food_item_id = document.getElementById("food-item").selectedIndex;
		var rest_name_id = document.getElementById("rest-name").selectedIndex;
		var rest_branch_name_id = document.getElementById("rest-branch-name").selectedIndex;
		// order_type.options[sel.selectedIndex].text;
		let orderData = JSON.stringify({
			"user_id": "0",
			"item_id": food_item_id,
			"restaurant_id": rest_name_id,
			"branch_id": rest_branch_name_id,
			// "delivery_id": "404",
			"payment_id": "420",
			"delivery_address": delivery_addr.value,
			"delivery_time": delivery_time.value
		});
		if (rest_name_id === 0){
			alert("Select a restaurant to order from!!!.");
			// rest_name.setAttribute("class", "dropdown;");
			// rest_name.setAttribute("style", "color: red;");
			rest_name.setAttribute("style","width: 350px;height:40px;font-size:0.25in;color:red");
			return;
		}
		if (delivery_addr.value === "Address") {
			delivery_addr.setAttribute("style","width: 350px;height:40px;font-size:0.25in;background-color: red;");
			// delivery_addr.setAttribute("style", "");
			alert("Please Provide a valid address to deliver the order.");
			return;
		}
		orderReq = new XMLHttpRequest();
		var url = "submitOrder?data=" + encodeURIComponent(orderData);
		orderReq.open("GET", url, true);
		orderReq.setRequestHeader("Content-type", "application/json");
		orderReq.onreadystatechange = function () {
			if (orderReq.readyState === 4 && orderReq.status === 200) {


				var modal = document.querySelector(".modal");
				// var trigger = document.querySelector(".trigger");
				var closeButton = document.querySelector(".close-button");

				function toggleModal() {
					modal.classList.toggle("show-modal");
				}

				modal.classList.toggle("show-modal");
				Push.create("Order Processed for " + food_item.options[food_item_id].text + " from " + rest_name.options[rest_name_id].text, {
					body: "Thanks for being with us.",
					// icon: '/icon.png',
					timeout: 4000,
					onClick: function () {
						window.focus();
						this.close();
					}
				});

				// alert("Order Confirmed");
				location.href = "/order";

				function windowOnClick(event) {
					if (event.target === modal) {
						toggleModal();
					}
				}

				// trigger.addEventListener("click", toggleModal);
				closeButton.addEventListener("click", toggleModal);
				window.addEventListener("click", windowOnClick);

			}
		}
		;
		// orderReq.send(orderData);
		orderReq.send();
		// alert("Order Submitted:\n" + orderData);
	}
);


// Sending a receiving data in JSON format using GET method
//
// var order_now = document.getElementById("order_now");
// order_now.addEventListener("click", function () {
//     var xhr = new XMLHttpRequest();
//     var url = "submitOrder?data=" + encodeURIComponent(JSON.stringify({"email": "hey@mail.com", "password": "101010"}));
//     xhr.open("GET", url, true);
//     xhr.setRequestHeader("Content-Type", "application/json");
//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === 4 && xhr.status === 200) {
//             var json = JSON.parse(xhr.responseText);
//             console.log(json.email + ", " + json.password);
//         }
//     };
//     xhr.send();
// };


//////////////////////////// ajax-query ///////////////////////////////
//
// function csrfSafeMethod(method) {
//     // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }
//
// var order_now = document.getElementById("order_now");
// order_now.addEventListener("click", function () {
//     var xhr = new XMLHttpRequest();
//     // var url = "submitOrder?data=" + encodeURIComponent(JSON.stringify({"email": "hey@mail.com", "password": "101010"}));
//     // xhr.open("GET", url, true);
//     // $.ajaxSetup({
//     //     beforeSend: function (xhr, settings) {
//     //         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//     //             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//     //         }
//     //     }
//     // });
//
//     data = {"email": "hey@mail.com", "password": "101010"};
//     $.ajax({
//         url: '/submitOrder/',
//         cache: 'false',
//         dataType: 'json',
//         type: 'POST',
//         data: data,
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
//         },
//         success: function (data) {
//         },
//         error: function (error) {
//         }
//     });
//
// });
//
