$(".dbllike").dblclick(function (e) {
  var id = this.id;
  var currentLocation = window.location.origin;
  var href = currentLocation + "/like/";
  e.preventDefault();

  $.ajax({
    url: href,
    data: {
      likeId: id,
    },
    success: function (response) {
      if (response.liked) {
        var lik = document.getElementById("lovebtn" + id);
        lik.classList.add("fas");
        lik.classList.remove("far");

        if (response.loveCount + 1 == 1) {
          $("#loveCount" + id).html(response.loveCount + 1 + " love");
        } else {
          $("#loveCount" + id).html(response.loveCount + 1 + " loves");
        }
      } else {
        var lik = document.getElementById("lovebtn" + id);
        lik.classList.remove("fas");
        lik.classList.add("far");
        if (response.loveCount - 1 == 1) {
          $("#loveCount" + id).html(response.loveCount - 1 + " love");
        } else {
          $("#loveCount" + id).html(response.loveCount - 1 + " loves");
        }
      }
    },
  });
});

$(".like").click(function (e) {
  var id = this.id;
  var currentLocation = window.location.origin;
  var href = currentLocation + "/like/";
  e.preventDefault();

  $.ajax({
    url: href,
    data: {
      likeId: id,
    },
    success: function (response) {
      if (response.liked) {
        var lik = document.getElementById("lovebtn" + id);
        lik.classList.add("fas");
        lik.classList.remove("far");

        if (response.loveCount + 1 == 1) {
          $("#loveCount" + id).html(response.loveCount + 1 + " love");
        } else {
          $("#loveCount" + id).html(response.loveCount + 1 + " loves");
        }
      } else {
        var lik = document.getElementById("lovebtn" + id);
        lik.classList.remove("fas");
        lik.classList.add("far");

        if (response.loveCount - 1 == 1) {
          $("#loveCount" + id).html(response.loveCount - 1 + " love");
        } else {
          $("#loveCount" + id).html(response.loveCount - 1 + " loves");
        }
      }
    },
  });
});

$(".save").click(function (e) {
  var id = this.id;
  var currentLocation = window.location.origin;
  var href = currentLocation + "/save/";
  e.preventDefault();

  $.ajax({
    url: href,
    data: {
      post: id,
    },
    success: function (response) {
      if (response.saved) {
        var lik = document.getElementById("savebtn" + id);
        lik.classList.add("fas");
        lik.classList.remove("far");
      } else {
        var lik = document.getElementById("savebtn" + id);
        lik.classList.remove("fas");
        lik.classList.add("far");
      }
    },
  });
});
$(".repository").click(function (e) {
  var id = this.id;
  var currentLocation = window.location.origin;
  var href = currentLocation + "/add-repository/";
  e.preventDefault();

  $.ajax({
    url: href,
    data: {
      post: id,
    },
    success: function (response) {
      if (response.repository) {
        $("#repository" + id).html("Show on profile");
      } else {
        $("#repository" + id).html("Repository");
      }
    },
  });
});
