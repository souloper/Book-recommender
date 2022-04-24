$(document).ready(function() {
    var outputList = document.getElementsById("list-output");
    var bookUrl = "https://www.googleapis.com/books/v1/volumes?q="
    var placeHlder = '<img src="https://via.placeholder.com/150">'
    var searchData;


    $("#search").click(function() {
        outputList.innerHTML = ""
        searchData = $("#search-box").val();

        if(searchData === "" || searchData === null) {
            console.log("Enter Something!!");
        }
        else{
            $.ajax({
                url: bookUrl + searchData,
                dataType: "json",
                success: function(res) {
                    console.log(res)

                    if(response.totalItems === 0) {
                        alert("Try again");
                    }
                    else{
                        $(".main-heading").css('color: red');

                        // displayResults(res);
                    }
                },
                error: function() {
                    alert("something went wrong")
                }
            })
        }
        $("#search-box").val("")
    })
});