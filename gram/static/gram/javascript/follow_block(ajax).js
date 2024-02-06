$(".followRequest").click(function (e) {
    var requested_by_user = this.id;
    console.log(requested_by_user)
    var href = $(".followRequest").find("a").attr("href");
    e.preventDefault();
    
    $.ajax({
      url: href,
      data: {
        by_user: requested_by_user,
      },
      success: function (response) {
        if (response.action=="requested") {
          
            $("#followbtn" + requested_by_user).html("Requested");
        }
        else if(response.action=="unfollow"){
            $("#followbtn" + requested_by_user).html("Unfollow");
        }
        else {
            $("#followbtn" + requested_by_user).html("Follow");
        }
      },
    });
  });

  $(".acceptRequest").click(function (e) {
    var requested_by_user = this.id;
    var currentLocation=window.location.origin
    var href = currentLocation +'/accept-request/'
    e.preventDefault();
    
    $.ajax({
      url: href,
      data: {
        by_user: requested_by_user,
      },
      success: function (response) {
        $(".deleteRequest" + requested_by_user).remove();
        if (response.action=="requested") {
          
            $("#followbtn" + requested_by_user).html("Requested");
            $(".deleteRequest" + requested_by_user).remove();
        }
        else if(response.action=="unfollow"){
            $("#followbtn" + requested_by_user).html("Unfollow");
            $(".deleteRequest" + requested_by_user).remove();
        }
        else {
            $("#followbtn" + requested_by_user).html("Follow");
            $(".deleteRequest" + requested_by_user).remove();
        }
      },
    });
  });
  
  $(".deleteRequest").click(function (e) {
    var requested_by_user = this.id;
    var currentLocation=window.location.origin
    var href = currentLocation +'/delete-request/'
    e.preventDefault();
    
    $.ajax({
      url: href,
      data: {
        by_user: requested_by_user,
      },
      success: function (response) {
        if (response.deleted) {
          
            $("#R" + requested_by_user).remove();
        }
        
      },
    });
  });

  $(".Ublock").click(function (e) {
    var blockUserID = this.id;
    var currentLocation=window.location.origin
    var href = currentLocation +'/block-user/'
    e.preventDefault();
    
    $.ajax({
      url: href,
      data: {
        user: blockUserID,
      },
      success: function (response) {
        if (response.blocked) {
          
            $("#Block" + blockUserID).html("Unblock");
        }
        else {
            $("#Block" + blockUserID).html("Block");
        }
      },
    });
  });

  $(".removeF").click(function (e) {
    var remove_user = this.id;
    var currentLocation=window.location.origin
    var href = currentLocation +'/remove-follower/'
    e.preventDefault();
    
    $.ajax({
      url: href,
      data: {
        to_remove_user: remove_user,
      },
      success: function (response) {
        if(response.removed) {
            $("#F"+remove_user).html("Add back");
        }
        
        else {
            $("#F"+remove_user).html("remove");
        }
      },
    });
  });

  $(".removeFollowing").click(function (e) {
    var remove_user = this.id;
    var currentLocation=window.location.origin
    var href = currentLocation +'/remove-following/'
    e.preventDefault();
    
    $.ajax({
      url: href,
      data: {
        to_remove_user: remove_user,
      },
      success: function (response) {
        if(response.removed) {
            $("#F"+remove_user).html("Add back");
        }
        
        else {
            $("#F"+remove_user).html("Unfollow");
        }
      },
    });
  });

 