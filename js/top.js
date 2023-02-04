window.addEventListener("scroll", function () {
    const tejun = document.querySelector("#towa");
    const scroll = window.pageYOffset;
    let k=(scroll-180)/(530-180);
    tejun.style.opacity=k.toString();
  });
  window.addEventListener("scroll", function () {
    const tejun = document.querySelector("#toro");
    const scroll = window.pageYOffset;
    let k=(scroll-810)/(1250-810);
    tejun.style.opacity=k.toString();
  });

  $(document).ready(function(){
    $(".menu p").on("click",function(){
      $(this).next().toggleClass("hidden");
    });
  });
  