var app = angular.module('app',[]);
var transform = function(data) {
    return jQuery.param(data);
};

app.controller('dashboardCtrl', ['$scope','$http', '$interval','$filter',function($scope, $http, $interval, $filter) {

    $scope.activeData = [];
    $scope.marketDelay = '';
    $scope.tickWidth = '';
    $scope.logBase = '';


    $scope.initObj = {
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
        pdiff3 : '',
        time : '',
        hotIcon: false
    }

    $scope.submitData = function(){
        var params = {
            marketDelay : $scope.marketDelay,
            tickWidth : $scope.tickWidth,
            logBase : $scope.logBase
        };

        $http.post('/fetchData', params,
        {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            transformRequest: transform,
            dataType : 'json'
        }).then(function(data) {

            console.log("success");

        }, function(error) {
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
                    pdiff3 : value.pdiff3,
                    time : value.time
        });

        // console.log("activeData >> " + angular.toJson($scope.activeData));
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
                    pdiff3 : value.pdiff3,
                    time : value.time,
                    hotIcon: false
                });
            });

            $scope.volumeRankData = $filter('orderBy')($scope.dataList, 'vRank');
            $scope.priceRankData = $filter('orderBy')($scope.dataList, 'pRank');
            $scope.combinedRankData = $filter('orderBy')($scope.dataList, 'cRank');

            $scope.volumeData = [];
            var len1 = 12;
            var len2 = 24;
            for(var i=0; i<len1; i++){
                if(i <= len1 && typeof $scope.volumeRankData[i] != 'undefined'){
                    $scope.volumeData.push($scope.volumeRankData[i]);
                }else if(i<=len1 && typeof $scope.volumeRankData[i] == 'undefined'){
                    $scope.volumeData.push($scope.initObj);
                }else{
                    // console.log("Exceeded 12");
                }
            }

            $scope.priceData = [];
            for(var i=0; i<len1; i++){
                if(i <= len1 && typeof $scope.priceRankData[i] != 'undefined'){
                    $scope.priceData.push($scope.priceRankData[i]);
                }else if(i<=len1 && typeof $scope.priceRankData[i] == 'undefined'){
                    $scope.priceData.push($scope.initObj);
                }else{
                    // console.log("Exceeded 12");
                }
            }
            // console.log("$scope.priceData >> " + angular.toJson($scope.priceData));

            $scope.combinedData = [];
            for(var j=0; j<len2; j++){
                if(j <= len2 && typeof $scope.combinedRankData[j] != 'undefined'){
                    $scope.combinedData.push($scope.combinedRankData[j]);
                }else if(j<=len2 && typeof $scope.combinedRankData[j] == 'undefined'){
                    $scope.combinedData.push($scope.initObj);
                }else{
                    // console.log("Exceeded 24");
                }
            }
            // console.log("$scope.combinedData >> " + angular.toJson($scope.combinedData));


            $scope.getHotIcon();

            //console.log("$scope.combinedData >> " + angular.toJson($scope.combinedData));

            if($scope.activeData.length > 0){
                for(var a=0; a<$scope.activeData.length; a++){
                    var aObj = $scope.activeData[a];

                     var found = false;
                    for(var c=0; c<$scope.combinedData.length; c++){
                        var tempObj = $scope.combinedData[c];
                        //console.log("temp obj >> " + angular.toJson(tempObj));

                        if(aObj.key != tempObj.key){
                            found = false

                        }else{
                           return found = true;

                        }
                    }

                    // console.log("found >> " + found);

                }

                if(!found){
                    $scope.activeData = [];
                }
            }


         }, function(error) {
         //Error
            $('#cover-spin').hide();
            alert('error');
         });
   };


   $scope.getHotIcon = function(){
        for(var c in $scope.combinedData){
            var tempComb = $scope.combinedData[c];

            for(var v in $scope.volumeData){
                var tempVol = $scope.volumeData[v];

                for(var p in $scope.priceData){
                    var tempPri = $scope.priceData[p];

                    if(tempComb.key !='' && tempComb.key == tempVol.key && tempComb.key == tempPri.key){
                        // alert("true :: " + tempComb.key);
                        $scope.combinedData[c].hotIcon = true;

                        $scope.combinedData[c].showImage = true;

                        //console.log("$scope.combinedData[c].hotIcon >> " + angular.toJson($scope.combinedData[c]) + " << >> " + $scope.combinedData[c].key)
                    }else{
                        $scope.combinedData[c].hotIcon = false;
                        //$scope.combinedData[c].showImage = false;
                    }

                }
            }
        }

       // console.log("$scope.combined data >> " + angular.toJson($scope.combinedData));
   }

   $scope.getmtlData = function(){
        $http({
            method: "GET",
            url: '/getMtlConfigData',
        }).then(function(result) {
            //Success
            $('#cover-spin').hide();

            //console.log("result >> " + angular.toJson(result.data));

            $scope.marketDelay = result.data.marketDelay;
            $scope.tickWidth = result.data.tickWidth;
            $scope.logBase = result.data.logBase;

        }, function(error) {
            //Error
            $('#cover-spin').hide();
            alert('error');
        });
   }

   $interval(function() {
        // your stuff
        $scope.getInitData(false);
    }, 60000);

    (function initController() {
        $scope.getInitData(true);
        $scope.getmtlData();
    })();

}]);