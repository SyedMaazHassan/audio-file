$(".favorite_heart").on('click', function () {
    let icon_id = this.id;
    let song_id = this.id.split("_")[1];

    $.ajax({
        url: "/mark_as_favorite",
        type: "GET",
        data: "song_id="+song_id,
        success: (response)=>{
            console.log(response);
            if (response.status) {
            let favourite_icon_txt = "";
            let title = "";

            if (response.song_status) {
                favourite_icon_txt = "favorite";
                title = "Remove from favorite";

            }else{
                favourite_icon_txt = "favorite_border";
                title = "Mark as favorite";
            }

            $(`#${icon_id}`).text(favourite_icon_txt);
            $(`#${icon_id}`).prop('title', title);
            }

        }
    });
});



