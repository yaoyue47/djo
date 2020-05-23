window.onload = function () {


    new myPagination({
        id: 'pagination_wendu',
        curPage:1, //初始页码
        pageTotal: 60, //总页数
		pageAmount: 10,  //每页多少条
        dataTotal: 600, //总共多少条数据
		pageSize: 7, //可选,分页个数
        showPageTotalFlag:true, //是否显示数据统计
        showSkipInputFlag:true, //是否支持跳转
        getPage: function (page) {
            //获取当前页数
            getdata(page,"wendu");
        }
    })
    new myPagination({
        id: 'pagination_shidu',
        curPage:1, //初始页码
        pageTotal: 60, //总页数
		pageAmount: 10,  //每页多少条
        dataTotal: 600, //总共多少条数据
		pageSize: 7, //可选,分页个数
        showPageTotalFlag:true, //是否显示数据统计
        showSkipInputFlag:true, //是否支持跳转
        getPage: function (page) {
            //获取当前页数
            getdata(page,"shidu");
        }
    })
	
}