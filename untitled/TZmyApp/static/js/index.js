 $(function () {
    $(".ui.dropdown").dropdown();
    $('.from').calendar(
        {
           type:'date',
           formatter: { // 自定义日期的格式
            date: function(date, settings) {
                if (!date) return '';

                var year  = date.getFullYear();
                var month = date.getMonth() + 1;
                var day   = date.getDate();

                month = month < 10 ? '0'+month : month;
                day   = day   < 10 ? '0'+day   : day;

                return year + '-' + month + '-' + day;
          }
      }})
    $('.to').calendar(
        {
            type:'date',
            formatter: { //
                date: function(date, settings) {
                    if (!date) return '';

                    var year  = date.getFullYear();
                    var month = date.getMonth() + 1;
                    var day   = date.getDate();

                    month = month < 10 ? '0'+month : month;
                    day   = day   < 10 ? '0'+day   : day;

                    return year + '-' + month + '-' + day;
                }
             }
        });
    $('.report').click(function(){
        type = $('.type').find("option:selected").text();
        product = $('.product').find("option:selected").text();
        indicator = $('.indicator').find("option:selected").text();
        from = $('.date-from').val();
        to = $('.date-to').val();
        console.log(type,product,indicator,from,to)
        url = 'test/';
        $.post({
            'url':url,
            'data':{'type':type,'product':product,'indicator':indicator,'from':from,'to':to},
            'success': function(data){
               console.log(data)
            }
        })

    })



  })