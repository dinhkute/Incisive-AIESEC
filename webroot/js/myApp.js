var myApp = angular.module('myApp', [
	'ngRoute', 	
	'controller'
]);
myApp.config(['$routeProvider', function($routeProvider) {
	$routeProvider.
	when('/', {
		templateUrl: 'partials/RecruitmentManagement.html',
	}).
	when('/addItem', {
		templateUrl: 'partials/addItem.html',
		controller: 'InventoryController'
	}).
	when('/myInventory', {
		templateUrl: 'partials/myInventory.html',
		controller: 'InventoryController'
	}).
	when('/myWishlist', {
		templateUrl: 'partials/myWishlist.html',
		controller: 'WishlistController'
	}).
	when('/itemDetails',{
		templateUrl: 'partials/itemDetails.html',
		controller: 'DetailsController'
	}).
	when('/itemRequested',{
		templateUrl: 'partials/itemRequested.html'
	}).
	when('/tradeRequest',{
		templateUrl: 'partials/tradeRequest.html'
	}).
	when('/tradeDetail',{
		templateUrl: 'partials/tradeDetail.html'
	}).
	when('/thankyou',{
		templateUrl: 'partials/thankyou.html'
	})
}]);