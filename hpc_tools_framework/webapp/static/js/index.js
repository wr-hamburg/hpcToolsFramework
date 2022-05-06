$(document).ready(function () {
  $(".selectpicker").selectpicker();

  selectDarshan = document.querySelector(".darshan-select");
  first = selectDarshan.querySelector("option");

  selectDarshan.addEventListener("change", function (el) {
    first.value = el.target.value;
    el.target.querySelector("option").setAttribute("selected", false);
    el.target.selectedIndex = 0;
    console.log(first.value);
  });
  $("#skills").change(function () {
    $("#hidden_skills").val($("#skills").val());
  });

  $("#multiple_select_form").on("submit", function (event) {
    event.preventDefault();
    if ($("#skills").val() != "") {
      var form_data = $(this).serialize();
      $.ajax({
        url: "/ajax_add",
        method: "POST",
        data: form_data,
        success: function (data) {
          //console.log(data);
          $("#hidden_skills").val("");
          $(".selectpicker").selectpicker("val", "");
          alert(data);
        },
      });
    } else {
      alert("Please select framework");
      return false;
    }
  });

  selectVampire = document.querySelector(".vampire-select");
  firstVampire = selectVampire.querySelector("option");

  selectVampire.addEventListener("change", function (el) {
    firstVampire.value = el.target.value;
    el.target.querySelector("option").setAttribute("selected", false);
    el.target.selectedIndex = 0;
    console.log(firstVampire.value);
  });
});

$(".menu-toggle").click(function (e) {
  e.preventDefault();
  var toggleButton = $(this);
  if (toggleButton.next().hasClass("active")) {
    toggleButton.next().removeClass("active");
    toggleButton.next().slideUp(400);
    toggleButton.removeClass("rotate");
  } else {
    toggleButton.parent().parent().find("li .sub-menu").removeClass("active");
    toggleButton.parent().parent().find("li .sub-menu").slideUp(400);
    toggleButton.parent().parent().find(".menu-toggle").removeClass("rotate");
    toggleButton.next().toggleClass("active");
    toggleButton.next().slideToggle(400);
    toggleButton.toggleClass("rotate");
  }
});

$(".list-group .list-group-item").click(function (e) {
  $(".list-group .list-group-item").removeClass("active");
  $(e.target).addClass("active");
  console.log(e.target.firstElementChild.id);
  if ($(".list-group .list-group-item").hasClass("active")) {
    $(
      "#facheck" +
        e.target.firstElementChild.id.slice(
          e.target.firstElementChild.id.length - 1
        )
    ).css("display", "block");
  }
  for (var i = 1; i < 6; i++) {
    if (
      i !=
      parseInt(
        e.target.firstElementChild.id.slice(
          e.target.firstElementChild.id.length - 1
        )
      )
    ) {
      $("#facheck" + i).css("display", "none");
      $("#facheck" + i)
        .parent()
        .removeClass("active");
    }
  }
});
