if ($(".sw-layout").length > 0) {
    $(".sw-layout").each(function () {
        var tfSwCategories = $(this);
        var swiperContainer = tfSwCategories.find(".swiper");
        if (swiperContainer.length === 0) return;
        var preview = swiperContainer.data("preview") || 1;
        var screenXl = swiperContainer.data("screen-xl") || preview;
        var tablet = swiperContainer.data("tablet") || 1;
        var mobile = swiperContainer.data("mobile") || 1;
        var mobileSm = swiperContainer.data("mobile-sm") || mobile;
        var spacing = swiperContainer.data("space") || 0;
        var spacingMd = swiperContainer.data("space-md") || spacing;
        var spacingLg = swiperContainer.data("space-lg") || spacing;
        var spacingXl = swiperContainer.data("space-xl") || spacingLg;
        var perGroup = swiperContainer.data("pagination") || 1;
        var perGroupMd = swiperContainer.data("pagination-md") || 1;
        var perGroupLg = swiperContainer.data("pagination-lg") || 1;
        var center = swiperContainer.data("slide-center") || false;
        var initSlide = swiperContainer.data("init-slide") || 0;
        var autoplay =
            swiperContainer.data("autoplay") == true ||
            swiperContainer.data("autoplay") == "true";
        var paginationType = swiperContainer.data("progressbar") || "bullets";
        var loop =
            swiperContainer.data("loop") == true ||
            swiperContainer.data("loop") == "true";
        var effect = swiperContainer.data("effect") || "slide";
        var nextBtn = tfSwCategories.find(".nav-next-layout")[0] || null;
        var prevBtn = tfSwCategories.find(".nav-prev-layout")[0] || null;
        var progressbar =
            tfSwCategories.find(".sw-pagination-layout")[0] ||
            tfSwCategories.find(".sw-progress-layout")[0] ||
            null;
        var fractionEl = tfSwCategories.find(".sw-fraction-layout")[0] || null;

        var swiperOptions = {
            slidesPerView: mobile,
            spaceBetween: spacing,
            speed: 1000,
            centeredSlides: center,
            initialSlide: initSlide,
            loop: loop,
            observer: true,
            observeParents: true,
            autoplay: autoplay
                ? {
                      delay: 4000,
                      disableOnInteraction: false,
                  }
                : false,
            pagination: progressbar
                ? {
                      el: progressbar,
                      clickable: true,
                      type: paginationType,
                  }
                : false,
            navigation: {
                nextEl: nextBtn,
                prevEl: prevBtn,
            },
            breakpoints: {
                575: {
                    slidesPerView: mobileSm,
                    spaceBetween: spacing,
                    slidesPerGroup: perGroup,
                },
                768: {
                    slidesPerView: tablet,
                    spaceBetween: spacingMd,
                    slidesPerGroup: perGroupMd,
                },
                992: {
                    slidesPerView: preview,
                    spaceBetween: spacingLg,
                    slidesPerGroup: perGroupLg,
                },
                1200: {
                    slidesPerView: screenXl,
                    spaceBetween: spacingXl,
                    slidesPerGroup: perGroupLg,
                },
            },
        };

        if (effect === "fade") {
            swiperOptions.effect = "fade";
            swiperOptions.fadeEffect = { crossFade: true };
        } else if (effect === "creative") {
            swiperOptions.effect = "creative";
            swiperOptions.creativeEffect = {
                prev: {
                    shadow: true,
                    translate: [0, 0, -400],
                },
                next: {
                    translate: ["100%", 0, 0],
                },
            };
        }

        var swiper = new Swiper(swiperContainer[0], swiperOptions);

        if (fractionEl) {
            swiper.on("init slideChange", function () {
                const current = String(swiper.realIndex + 1).padStart(2, "0");
                const totalSlides = String(
                    swiperContainer.find(
                        ".swiper-slide:not(.swiper-slide-duplicate)"
                    ).length
                ).padStart(2, "0");
                fractionEl.innerHTML = `<span class="current">${current}</span> / <span class="total">${totalSlides}</span>`;
            });
            swiper.emit("init");
        }
    });
}

$(".flat-thumbs-tes").each(function (index, container) {
    const $container = $(container);

    const $thumb = $container.find(".tf-thumb-tes");
    const $main = $container.find(".tf-tes-main");

    if ($thumb.length && $main.length) {
        const spaceThumbLg = $thumb.data("space-lg");
        const spaceThumb = $thumb.data("space");
        const effect = $thumb.data("effect") || "slide";

        const spaceTesLg = $main.data("space-lg");
        const spaceTes = $main.data("space");
        const effect2 = $main.data("effect") || "slide";

        const swThumb = new Swiper($thumb[0], {
            speed: 800,
            spaceBetween: spaceThumb,
            effect: effect,
            fadeEffect: effect === "fade" ? { crossFade: true } : undefined,
            breakpoints: {
                768: {
                    spaceBetween: spaceThumbLg,
                },
            },
        });

        const swTesMain = new Swiper($main[0], {
            speed: 800,
            navigation: {
                nextEl: $container.find(".nav-next-tes")[0],
                prevEl: $container.find(".nav-prev-tes")[0],
            },
            pagination: {
                el: $container.find(".sw-pagination-tes")[0],
                clickable: true,
            },
            effect: effect2,
            fadeEffect: effect2 === "fade" ? { crossFade: true } : undefined,
            spaceBetween: spaceTes,
            breakpoints: {
                768: {
                    spaceBetween: spaceTesLg,
                },
            },
        });


        swThumb.controller.control = swTesMain;
        swTesMain.controller.control = swThumb;
    }
});

if ($(".tf-sw-mobile").length > 0) {
    $(".tf-sw-mobile").each(function () {
        var swiperMb;
        var $this = $(this);
        var screenWidth = $this.data("screen");

        function initSwiper() {
            if (
                matchMedia(`only screen and (max-width: ${screenWidth}px)`)
                    .matches
            ) {
                if (!swiperMb) {
                    var preview = $this.data("preview");
                    var spacing = $this.data("space");

                    swiperMb = new Swiper($this[0], {
                        slidesPerView: preview,
                        spaceBetween: spacing,
                        speed: 1000,
                        pagination: {
                            el: $this.find(".sw-pagination-mb")[0],
                            clickable: true,
                        },
                        navigation: {
                            nextEl: $this.find(".nav-prev-mb")[0],
                            prevEl: $this.find(".nav-next-mb")[0],
                        },
                    });
                }
            } else {
                if (swiperMb) {
                    swiperMb.destroy(true, true);
                    swiperMb = null;
                    $this.find(".swiper-wrapper").removeAttr("style");
                    $this.find(".swiper-slide").removeAttr("style");
                }
            }
        }

        initSwiper();
        window.addEventListener("resize", function () {
            initSwiper();
        });
    });
}

if ($(".sw-pagi-count").length > 0) {
    const numLeft = document.getElementById("numLeft");
    const numRight = document.getElementById("numRight");

    const swiper = new Swiper(".sw-pagi-count", {
        loop: true,
        autoplay: { delay: 4000 },
        effect: "fade",
        on: {
            slideChange: function () {
                const current = this.realIndex + 1;
                const num = current.toString().padStart(2, "0");
                numLeft.textContent = num;
                numRight.textContent = num;
            },
        },
    });

    numLeft.addEventListener("click", () => {
        swiper.slidePrev();
        swiper.autoplay.stop();
    });

    numRight.addEventListener("click", () => {
        swiper.slideNext();
        swiper.autoplay.stop();
    });
}

if ($(".sw-thumbs-pagi").length > 0 && $(".sw-single").length > 0) {
    var preview = $(".sw-thumbs-pagi").data("preview");
    var spacing = $(".sw-thumbs-pagi").data("space");
    var mobile = $(".sw-thumbs-pagi").data("mobile");
    var mobileSm = $(".sw-thumbs-pagi").data("mobile-sm");
    var autoplay = $(".sw-thumbs-pagi").data("auto-play") || false;
    var loop = $(".sw-thumbs-pagi").data("loop") || false;
    var parallaxEnable = $(".sw-single").data("parallax") || false;
    var effectType = $(".sw-single").data("effect");
    var autoplay = $(".sw-single").data("autoplay");


    var pagithumbs = new Swiper(".sw-thumbs-pagi", {
        spaceBetween: spacing,
        slidesPerView: preview,
        freeMode: true,
        watchSlidesProgress: true,
        loop: loop,
       
        navigation: {
            clickable: true,
            nextEl: ".sw-pagi-next",
            prevEl: ".sw-pagi-prev",
        },
        breakpoints: {
            375: {
                slidesPerView: 4,
                spaceBetween: spacing,
            },
            500: {
                slidesPerView: mobileSm,
            },
        },
    });

    var swiperSingle = new Swiper(".sw-single", {
        loop: loop,
        speed: 1500,
        effect: effectType,
        fadeEffect: {
            crossFade: true,
        },
        thumbs: {
            swiper: pagithumbs,
        },
        autoplay: autoplay
        ? {
              delay: 3000,
              disableOnInteraction: false,
          }
        : false,
        parallax: parallaxEnable,
        navigation: {
            clickable: true,
            nextEl: ".sw-thumbs-next",
            prevEl: ".sw-thumbs-prev",
        },
        on: {
            init: function () {
                var swiper = this;

                if (document.querySelector(".progress-bars")) {
                    initializeProgressBars(this);
                }

                if (parallaxEnable) {
                    for (var i = 0; i < swiper.slides.length; i++) {
                        $(swiper.slides[i])
                            .find(".tp-showcase-slider-bg")
                            .attr({
                                "data-swiper-parallax": 0.75 * swiper.width,
                            });
                    }
                }
            },
            slideChange: function () {
                if (document.querySelector(".progress-bars")) {
                    updateProgress(this.activeIndex);
                }
            },
            resize: function () {
                this.update();
            },
        },
    });

    function initializeProgressBars(swiperInstance) {
        const progressContainer = document.querySelector(".progress-bars");
        const totalSlides = swiperInstance.slides.length;

        progressContainer.innerHTML = "";
        for (let i = 0; i < totalSlides; i++) {
            const bar = document.createElement("div");
            bar.className = "progress-bar" + (i === 0 ? " active" : "");
            bar.innerHTML = '<div class="progress-fill"></div>';
            progressContainer.appendChild(bar);
        }

        updateProgress(swiperInstance.realIndex || 0);
    }

    function updateProgress(activeIndex) {
        const progressBars = document.querySelectorAll(".progress-bar");

        if (progressBars.length === 0) return;

        progressBars.forEach((bar, index) => {
            bar.classList.remove("active", "viewed");

            if (index < activeIndex) {
                bar.classList.add("viewed");
            } else if (index === activeIndex) {
                bar.classList.add("active");
            }
        });
    }
}
