
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

  //メニュー
  $(function(){
    $(".has-sub").mouseover(function(){
      $(this).children(".sub").stop().slideDown();
    });
    $(".has-sub").mouseout(function(){
      $(".sub").stop().slideUp();
    });
  });

  //上にスクロールボタン
  $(function() {
    $(window).on("scroll", function() {
      if($(this).scrollTop() > 400) {
        $(".fixed").fadeIn(300);
      }else {
        $(".fixed").fadeOut(300);
      }
    });
  });
  const scroll_top = function () {
    const topLeft = document.getElementById("nav").getBoundingClientRect().left;
    const topTop = document.getElementById("nav").getBoundingClientRect().top;
    window.scrollTo({
      left: topLeft,
      top: topTop,
      behavior: 'smooth'
    });
  };

  const scroll_towa = function () {
    const toLeft = document.getElementById("towa").getBoundingClientRect().left;
    const toTop = document.getElementById("towa").getBoundingClientRect().top;
    window.scrollTo({
      left: toLeft,
      top: toTop,
      behavior: 'smooth'
    });
  };

  const scroll_toro = function () {
    const roLeft = document.getElementById("toro").getBoundingClientRect().left;
    const roTop = document.getElementById("toro").getBoundingClientRect().top;
    window.scrollTo({
      left: roLeft,
      top: roTop,
      behavior: 'smooth'
    });
  };
