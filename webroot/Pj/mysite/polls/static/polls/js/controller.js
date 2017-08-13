var controller = angular.module('controller', []);

controller.controller("DbController", ['$scope', '$http', function($scope, $http) {
	 getInfo();
	 function getInfo(){
		 // Sending request to itemDetails.php files 
		 $http.post('database/itemDetails.php').success(function(data){
		 // Stored the returned data into scope 
			 $scope.items = data;
		 });
	 }
}]);


controller.controller("InventoryController", ['$scope', '$http', function($scope, $http) {
	 getInfo();
	 function getInfo(){
		 // Sending request to itemInventory.php files 
		 $http.post('database/itemInventory.php').success(function(data){
		 // Stored the returned data into scope 
			 $scope.inventory = data;
		 });
	}
	$scope.insertInfo = function(info){
	 $http.post('database/insertDetails.php',{"itemPicture":info.itemPicture,"itemName":info.itemName,"itemDescription":info.itemDescription}).success(function(data){
		 if (data == true) {
			 $('#itemForm').css('display', 'none');
		 }
		 });
	 }
	 $scope.deleteInfo = function(info){
		$http.post('database/deleteDetails.php',{"del_id":info.itemID}).success(function(data){
		if (data == true) {
		getInfo();
		}
		});
	 }
}]);

controller.controller("WishlistController", ['$scope', '$http', function($scope, $http) {
	 getInfo();
	 function getInfo(){
		 // Sending request to itemWishlist.php files 
		 $http.post('database/itemWishlist.php').success(function(data){
		 // Stored the returned data into scope 
			 $scope.wishlist = data;
		 });
	}
}]);

controller.controller('DetailsController', ['$scope', '$http','$routeParams', function($scope, $http, $routeParams) {
	 getInfo();
	 function getInfo(){
		 // Sending request to itemDetails.php files 
		 $http.post('database/itemDetails.php').success(function(data){
		 // Stored the returned data into scope 
			 $scope.items = data;
			 $scope.whichItem = $routeParams.itemId;
				 if ($routeParams.itemId > 0) {
					 $scope.prevItem = Number($routeParams.itemId)-1;
				 } else {
					 $scope.prevItem = $scope.products.length-1;
				 }
				 if ($routeParams.itemId < $scope.products.length-1) {
					 $scope.nextItem = Number($routeParams.itemId)+1;
				 } else {
					 $scope.nextItem = 0;
				 }
		 });
	 }
}]);
