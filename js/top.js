window.addEventListener("scroll", function () {
    const tejun = document.querySelector("#towa");
    const scroll = window.pageYOffset;
    let k=(scroll-160)/(500-160);
    tejun.style.opacity=k.toString();
  });
  window.addEventListener("scroll", function () {
    const tejun = document.querySelector("#toro");
    const scroll = window.pageYOffset;
    let k=(scroll-700)/(1300-700);
    tejun.style.opacity=k.toString();
  });