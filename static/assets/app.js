var app = angular.module('app',[]);

app.controller('dashboardCtrl', ['$scope','$http', '$interval',function($scope, $http, $interval) {

    $scope.activeData = [];
    $scope.marketDelay = '';
    $scope.tickWidth = '';
    $scope.logBase = '';



    $scope.submitData = function(){

        var params = {
            marketDelay : $cope.marketDelay,
            tickWidth : $scope.tickWidth,
            logBase : $scope.logBase
        };

        //console.log("params >> " + angular.toJson(params));

         $http({
            method: "GET",
            url: '/fetchData',
            params: params
         }).then(function(result) {
          //Success

          alert('success');

         }, function(error) {
         //Error
            alert('error');
         });


    };


    $scope.removeActive = function(value){
        var index = $scope.activeData.indexOf(value);
        $scope.activeData.splice(index, 1);

    };

   $scope.addActive = function(value){
        $scope.activeData.push({
                    key: value.key,
                    vol: value.vol,
                    price: value.price,
                    mv: value.mv,
                    mp: value.mp,
                    vRank : value.vRank,
                    pRank : value.pRank,
                    cRank : value.cRank,
                    vdiff1 : value.vdiff1,
                    vdiff2 : value.vdiff2,
                    vdiff3 : value.vdiff3,
                    pdiff1 : value.pdiff1,
                    pdiff2 : value.pdiff2,
                    pdiff3 : value.pdiff3
        });

        //console.log("activeData >> " + angular.toJson($scope.activeData));
   };

   $scope.getInitData = function(status){
        $scope.appData = [];
        if(status){
             $('#cover-spin').show();
        }
         $http({
            method: "GET",
            url: '/data',
         }).then(function(result) {
          //Success
            $('#cover-spin').hide();

            $scope.appData = result.data;
            $scope.dataList = [];

            angular.forEach($scope.appData, function (value, key) {
                //$scope.names.push(value.name);
                $scope.dataList.push({
                    key: key,
                    vol: value.vol,
                    price: value.price,
                    mv: value.mv,
                    mp: value.mp,
                    vRank : value.vRank,
                    pRank : value.pRank,
                    cRank : value.cRank,
                    vdiff1 : value.vdiff1,
                    vdiff2 : value.vdiff2,
                    vdiff3 : value.vdiff3,
                    pdiff1 : value.pdiff1,
                    pdiff2 : value.pdiff2,
                    pdiff3 : value.pdiff3
                });
            });

            console.log("$scope.dataList >> " + angular.toJson($scope.dataList));

            $scope.finalData = [];
            $scope.combinedData = [];
            var len1 = 12;
            var len2 = 24;
            for(var i=0; i<len1; i++){
                if(i <= len1 && typeof $scope.dataList[i] != 'undefined'){
                    $scope.finalData.push($scope.dataList[i]);
                }else if(i<=len1 && typeof $scope.dataList[i] == 'undefined'){
                    $scope.finalData.push({
                        key: '',
                        vol: '',
                        price: '',
                        mv: '',
                        mp: '',
                        vRank : '',
                        pRank : '',
                        cRank : '',
                        vdiff1 : '',
                        vdiff2 : '',
                        vdiff3 : '',
                        pdiff1 : '',
                        pdiff2 : '',
                        pdiff3 : ''
                    });
                }else{
                    console.log("Exceeded 12");
                }
            }

            for(var j=0; j<len2; j++){
                if(j <= len2 && typeof $scope.dataList[j] != 'undefined'){
                    $scope.combinedData.push($scope.dataList[j]);
                }else if(j<=len2 && typeof $scope.dataList[j] == 'undefined'){
                    $scope.combinedData.push({
                        key: '',
                        vol: '',
                        price: '',
                        mv: '',
                        mp: '',
                        vRank : '',
                        pRank : '',
                        cRank : '',
                        vdiff1 : '',
                        vdiff2 : '',
                        vdiff3 : '',
                        pdiff1 : '',
                        pdiff2 : '',
                        pdiff3 : ''
                    });
                }else{
                    console.log("Exceeded 12");
                }
            }


         }, function(error) {
         //Error
         $('#cover-spin').hide();
            alert('error');
         });
   };

   $interval(function() {
        // your stuff
        $scope.getInitData(false);
    }, 120000);

    (function initController() {
        $scope.getInitData(true);
    })();

}]);