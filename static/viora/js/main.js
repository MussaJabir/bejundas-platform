/**
 
 * Project Name: Viora AI-powered Multipurpose HTML Themes
 * Project Description: Viora is an AI-powered multipurpose HTML theme designed for speed and versatility. Perfect for business, tech startups, portfolios, and more with clean, modern design.        Easily customizable and optimized for performance across all devices
 * Tags: AI, HTML, Template, Theme, Website, Responsive, Multipurpose, Portfolio, Business, Design
 * Version: 1.0.0
 * This product is available exclusively on Themeforest
 * File name: main.js
 ----------------------------------------------------------------------------------

 1. animateCounters
 2. headerSticky
 3. headerFixed
 4. handleFooter
 5. video
 6. infiniteslide
 7. tabSlide
 8. tabs
 9. cursorCustom
 10. hoverActive
 11. hoverTabs
 12. accordionActive
 13. goTop
 14. wow
 15. fillterIso
 16. datePicker
 17. rangeSlide
 18. dropdownSelect
 19. handleBookingStep
 20. handleProgress
 21. handleCampaign
 22. handleAtropos
 23. initSwitchPriceValue
 24. handleBookingStep2
 25. handleSidebar
 26. oneNavOnePage
 27. getDataImage
 28. animateInput

**/

(function ($) {
    ("use strict");

    /* header_sticky
  -------------------------------------------------------------------------------------*/
    const headerSticky = function () {
        let lastScrollTop = 0;
        const delta = 10;
        const $header = $(".header-sticky");
        let navbarHeight = $header.outerHeight();

        let resizeTimeout;
        $(window).on("resize", function () {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(function () {
                navbarHeight = $header.outerHeight();
            }, 100);
        });
        $(window).on("scroll", function () {
            let scrollTop = $(this).scrollTop();

            if (scrollTop < 400) {
                $header.removeClass("is-sticky");
                return;
            }

            if (scrollTop > lastScrollTop + delta) {
                $header.removeClass("is-sticky");
                $(".sticky-top").css("top", "50px");
            } else if (scrollTop < lastScrollTop - delta) {
                $header.addClass("is-sticky");
                $(".sticky-top").css("top", `${30 + navbarHeight}px`);
            }

            lastScrollTop = scrollTop;
        });
    };

    /* Header Fixed
  ------------------------------------------------------------------------------------- */
    var headerFixed = function () {
        if ($(".header").hasClass("header-fixed")) {
            var nav = $(".header");
            if (nav.length) {
                var offsetTop = nav.offset().top,
                    headerHeight = nav.height(),
                    injectSpace = $("<div>", {
                        height: headerHeight,
                    });
                injectSpace.hide();

                $(window).on("load scroll", function () {
                    if ($(window).scrollTop() > 300) {
                        nav.addClass("is-fixed");
                        injectSpace.show();
                    } else {
                        nav.removeClass("is-fixed");
                        injectSpace.hide();
                    }
                });
            }
        }
    };

    /* animateCounters
  -------------------------------------------------------------------------------------*/
    const animateCounters = () => {
        const isInViewport = (element) => {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <=
                    (window.innerHeight ||
                        document.documentElement.clientHeight) &&
                rect.right <=
                    (window.innerWidth || document.documentElement.clientWidth)
            );
        };

        const runCounter = ($item) => {
            if ($item.data("animated")) return;

            $item.find(".numberCounter").each(function () {
                const $this = $(this);
                const countTo = parseInt($this.data("count")) || 0;
                const duration = parseInt($this.data("duration")) || 2000;

                $({ countNum: 0 }).animate(
                    { countNum: countTo },
                    {
                        duration: duration,
                        easing: "swing",
                        step: function () {
                            const num = Math.floor(this.countNum);
                            $this.text(String(num).padStart(1, "0"));
                        },
                        complete: function () {
                            const num = this.countNum;
                            $this.text(String(num).padStart(1, "0"));
                        },
                    }
                );
            });

            $item.data("animated", true);
        };

        const checkAndAnimate = () => {
            $(".counter-item").each(function () {
                const $item = $(this);
                if (isInViewport(this)) {
                    runCounter($item);
                }
            });
        };

        $(window).on("scroll resize", checkAndAnimate);
        $(document).ready(checkAndAnimate);
    };

    /* footer accordion
  -------------------------------------------------------------------------*/
    var handleFooter = function () {
        var footerAccordion = function () {
            var args = { duration: 250 };
            $(".footer-heading-mobile").on("click", function () {
                $(this).parent(".footer-col-block").toggleClass("open");
                if (!$(this).parent(".footer-col-block").is(".open")) {
                    $(this).next().slideUp(args);
                } else {
                    $(this).next().slideDown(args);
                }
            });
        };
        function handleAccordion() {
            if (matchMedia("only screen and (max-width: 767px)").matches) {
                if (
                    !$(".footer-heading-mobile").data("accordion-initialized")
                ) {
                    footerAccordion();
                    $(".footer-heading-mobile").data(
                        "accordion-initialized",
                        true
                    );
                }
            } else {
                $(".footer-heading-mobile").off("click");
                $(".footer-heading-mobile")
                    .parent(".footer-col-block")
                    .removeClass("open");
                $(".footer-heading-mobile").next().removeAttr("style");
                $(".footer-heading-mobile").data(
                    "accordion-initialized",
                    false
                );
            }
        }
        handleAccordion();
        window.addEventListener("resize", function () {
            handleAccordion();
        });
    };

    /* video
  -------------------------------------------------------------------------------------*/
    var video = function () {
        if ($("div").hasClass("widget-video")) {
            $(".popup-youtube").magnificPopup({
                type: "iframe",
            });
        }
    };

    /* infiniteslide
  -------------------------------------------------------------------------------------*/
    const infiniteslide = () => {
        if ($(".infiniteslide").length > 0) {
            $(".infiniteslide").each(function () {
                var $this = $(this);
                var style = $this.data("style") || "left";
                var clone = $this.data("clone") || 4;
                var speed = $this.data("speed") || 50;
                $this.infiniteslide({
                    speed: speed,
                    direction: style,
                    clone: clone,
                });
            });
        }
    };

    /* Tab Slide 
  ------------------------------------------------------------------------------------- */
    var tabSlide = function () {
        $(".tab-slide").each(function () {
            var $tabSlide = $(this);

            function updateTabSlide() {
                var $activeTab = $tabSlide.find("li.active");
                if ($activeTab.length > 0) {
                    var $width = $activeTab.outerWidth();
                    var $left = $activeTab.position().left;
                    var $sideEffect = $tabSlide.find(".item-slide-effect");
                    $sideEffect.css({
                        width: $width,
                        transform: "translateX(" + $left + "px)",
                    });
                }
            }

            $tabSlide.find("li").on("click", function () {
                $tabSlide.find("li").removeClass("active");
                $(this).addClass("active");

                var $width = $(this).outerWidth();
                var $left = $(this).position().left;
                var $sideEffect = $tabSlide.find(".item-slide-effect");
                $sideEffect.css({
                    width: $width,
                    transform: "translateX(" + $left + "px)",
                });
            });

            $(window).on("resize", updateTabSlide);

            updateTabSlide();
        });
    };

    /* tabs
  -------------------------------------------------------------------------*/
    const tabs = () => {
        if (!$(".widget-tabs").length) return;
        $(".widget-tabs").each(function () {
            const $widgetTabs = $(this);
            const $menuTabs = $widgetTabs.find(".widget-menu-tab .item-title");
            const $contentTabs = $widgetTabs
                .find(".widget-content-tab")
                .children();

            $menuTabs.on("click", function () {
                const tabIndex = $(this).index();
                $menuTabs.removeClass("active");
                $(this).addClass("active");
                $contentTabs.removeClass("active");
                $contentTabs.eq(tabIndex).addClass("active");
            });
        });
    };

    /* cursorCustom 
  ------------------------------------------------------------------------------------- */
    var cursorCustom = function () {
        if ($(".custom-cursor").length > 0) {
            $(".cursor-wrapper").each(function () {
                var $wrapper = $(this);
                var $cursor = $wrapper.find(".custom-cursor");
                var $title = $wrapper.find(".process-title");
                var $area = $wrapper.find(".area-cursor-custom");

                if ($cursor.length && $area.length) {
                    function moveCursor(e) {
                        var left = $area.offset().left;
                        var top = $area.offset().top - $(window).scrollTop();

                        $cursor.css({
                            top: e.clientY - top - 60 + "px",
                            left: e.clientX - left - 60 + "px",
                            opacity: 1,
                            transform: "scale(1)",
                        });
                    }

                    $area.on("mousemove pointermove", moveCursor);
                    $area.on("mouseleave", () => {
                        $cursor.css({
                            opacity: 0,
                            transform: "scale(0.3)",
                        });
                    });

                    $title.on({
                        mouseenter: () => $cursor.addClass("disable"),
                        mouseleave: () => $cursor.removeClass("disable"),
                    });
                }
            });
        }
    };

    /* hoverActive 
  -------------------------------------------------------------------------------------*/
    var hoverActive = function () {
        $(".wrap-box-hover-active").each(function (index) {
            var $container = $(this);
            var containerId = `hover-container-${index}`;
            $container.attr("data-hover-id", containerId);
            var $hoverItems = $container.find(".item-hover");
            if (
                $container.find(".item-hover.is-active").length === 0 &&
                $hoverItems.length > 0
            ) {
                $hoverItems.first().addClass("is-active");
            }
            $container.on("mouseenter", ".item-hover", function () {
                var $activeItem = $container.find(".item-hover.is-active");
                if ($activeItem.length > 0 && $activeItem[0] !== this) {
                    $activeItem.removeClass("is-active");
                }
                $(this).addClass("is-active");
            });
        });
    };

    /* hoverTabs 
  -------------------------------------------------------------------------------------*/
    var hoverTabs = function () {
        if (!$(".tabs-hover-wrap").length) return;

        $(".tabs-hover-wrap").each(function () {
            const $wrapper = $(this);
            const $tabBtns = $wrapper.find(".item");
            const $tabContents = $wrapper.find(".tab-content");
            let hoverTimer;
            $tabBtns
                .on("mouseenter", function () {
                    const $this = $(this);
                    hoverTimer = setTimeout(function () {
                        const tabId = $this.data("tab");
                        if (!$this.hasClass("active")) {
                            $tabBtns.removeClass("active");
                            $tabContents.removeClass("active");
                            $this.addClass("active");
                            $wrapper.find(`#${tabId}`).addClass("active");
                        }
                    }, 100);
                })
                .on("mouseleave", function () {
                    clearTimeout(hoverTimer);
                });

            $wrapper.on("mouseleave", function () {
                $tabBtns.removeClass("active");
                $tabContents.removeClass("active");
                $tabContents.first().addClass("active");
            });
            $tabBtns.removeClass("active");
            $tabContents.removeClass("active");
            $tabContents.first().addClass("active");
        });
    };

    /* accordionActive
  -------------------------------------------------------------------------------------*/
    var accordionActive = function () {
        if ($(".action_click").length > 0) {
            var isProcessing = false;
            $(".action").click(function () {
                if (isProcessing) {
                    return;
                }
                isProcessing = true;
                $(".action_click")
                    .not($(this).closest(".action_click"))
                    .removeClass("active");
                $(this).closest(".action_click").toggleClass("active");
                setTimeout(function () {
                    isProcessing = false;
                }, 500);
            });
        }
    };

    /* goTop
  -------------------------------------------------------------------------------------*/
    const goTop = () => {
        if ($("div").hasClass("progress-wrap")) {
            var progressPath = document.querySelector(".progress-wrap path");
            var pathLength = progressPath.getTotalLength();
            progressPath.style.transition =
                progressPath.style.WebkitTransition = "none";
            progressPath.style.strokeDasharray = pathLength + " " + pathLength;
            progressPath.style.strokeDashoffset = pathLength;
            progressPath.getBoundingClientRect();
            progressPath.style.transition =
                progressPath.style.WebkitTransition =
                    "stroke-dashoffset 10ms linear";
            var updateprogress = function () {
                var scroll = $(window).scrollTop();
                var height = $(document).height() - $(window).height();
                var progress = pathLength - (scroll * pathLength) / height;
                progressPath.style.strokeDashoffset = progress;
            };
            updateprogress();
            $(window).scroll(updateprogress);
            var offset = 200;
            var duration = 0;
            jQuery(window).on("scroll", function () {
                if (jQuery(this).scrollTop() > offset) {
                    jQuery(".progress-wrap").addClass("active-progress");
                } else {
                    jQuery(".progress-wrap").removeClass("active-progress");
                }
            });
            jQuery(".progress-wrap").on("click", function (event) {
                event.preventDefault();
                jQuery("html, body").animate({ scrollTop: 0 }, duration);
                return false;
            });
        }
    };

    /* wow
  -------------------------------------------------------------------------------------*/
    var wow = function () {
        if ($(".wow").length > 0) {
            var wow = new WOW({
                boxClass: "wow",
                animateClass: "animated",
                offset: 30,
                live: true,
            });
            wow.init();
        }
    };

    /* fillterIso
  -------------------------------------------------------------------------------------*/
    const fillterIso = () => {
        if (!$(".fillters-wrap").length) return;
        var $grid = $(".fillters-wrap").isotope({
            itemSelector: ".item-fillter",
            layoutMode: "fitRows",
        });
        $(".tf-filters button").on("click", function () {
            $(".tf-filters button").removeClass("active");
            $(this).addClass("active");
            var filterValue = $(this).attr("data-filter");
            $grid.isotope({ filter: filterValue });
        });
    };

    /* datePicker
  -------------------------------------------------------------------------------------*/
    const datePicker = () => {
        if (!$("#datepicker").length) return;
        $("#datepicker").datepicker();
    };

    /* rangeSlide
  -------------------------------------------------------------------------------------*/
    const rangeSlide = () => {
        if (!$(".tf-range-slider").length) return;
        const containers = document.querySelectorAll(".tf-range-slider");
        containers.forEach(function (container) {
            const slider = container.querySelector(".slider");
            const thumb = container.querySelector(".thumb");
            function updateThumb() {
                const sliderWidth = slider.offsetWidth;
                const min = +slider.min;
                const max = +slider.max;
                const val = +slider.value;
                const percent = (val - min) / (max - min);
                const offset = percent * (sliderWidth - 40) + 20;

                thumb.style.left = offset + "px";
                thumb.textContent = val;
            }

            slider.addEventListener("input", updateThumb);
            window.addEventListener("resize", updateThumb);
            updateThumb();
        });
    };

    /* Select Image
    -------------------------------------------------------------------------*/
    var dropdownSelect = function () {
        if ($(".tf-dropdown-select").length > 0) {
            const selectIMG = $(".tf-dropdown-select");

            selectIMG.find("option").each((idx, elem) => {
                const selectOption = $(elem);
                const imgURL = selectOption.attr("data-thumbnail");
                if (imgURL) {
                    selectOption.attr(
                        "data-content",
                        `<img src="${imgURL}" alt="Country" /> ${selectOption.text()}`
                    );
                }
            });
            selectIMG.selectpicker();
        }
    };

    /* handleBookingStep
    -------------------------------------------------------------------------*/
    var handleBookingStep = function () {
        if ($(".booking-step").length > 0) {
            let currentStep = 0;
            const $steps = $(".step");
            const $progress = $("#progress");
            const $progressText = $("#progressText");
            const $stepTitle = $("#stepTitle");
            const $btnNextStep = $(".btn-nextStep");

            function showStep(index) {
                $steps.removeClass("active").eq(index).addClass("active");
                let percent = Math.round(((index + 1) / $steps.length) * 100);
                $progress.css("width", percent + "%");
                $progressText.text(percent + "%");
                $stepTitle.text(`Step ${index + 1} of ${$steps.length}`);
            }

            $btnNextStep.on("click", function (e) {
                e.preventDefault();
                if (currentStep < $steps.length - 1) {
                    currentStep++;
                    showStep(currentStep);
                }
            });

            showStep(currentStep);
        }
    };

    /* Handle Progress
  ------------------------------------------------------------------------------------- */
    var handleProgress = function () {
        if ($(".progress-effect").length > 0) {
            var $progressSold = $(".progress-effect");
            if ($progressSold.length > 0) {
                var progressAnimated = false;

                function isInViewport(element) {
                    var elementTop = $(element).offset().top;
                    var elementBottom = elementTop + $(element).outerHeight();
                    var viewportTop = $(window).scrollTop();
                    var viewportBottom = viewportTop + $(window).height();
                    return (
                        elementBottom > viewportTop &&
                        elementTop < viewportBottom
                    );
                }

                function animateProgress() {
                    $progressSold.each(function () {
                        var $value = $(this).find(".value");
                        var progressValue = $value.data("progress");
                        setTimeout(function () {
                            $value.css({
                                width: progressValue + "%",
                                transition: "width 1s ease",
                            });
                        }, 300);
                    });
                    progressAnimated = true;
                }

                function checkAndAnimate() {
                    if (!progressAnimated && isInViewport($progressSold)) {
                        animateProgress();
                    }
                }

                checkAndAnimate();
                $(window).on("scroll", function () {
                    checkAndAnimate();
                });
            }
        }
    };

    /* handleCampaign
  ------------------------------------------------------------------------------------- */
    var handleCampaign = function () {
        if ($(".form-campaign").length > 0) {
            const amountInput = document.querySelector(".amount-input");
            const quickAmountBtns =
                document.querySelectorAll(".quick-amount-btn");
            const customBtn = document.querySelector(".custom-btn");
            const sponsorBtn = document.querySelector(".sponsor-btn");

            quickAmountBtns.forEach((btn) => {
                btn.addEventListener("click", () => {
                    quickAmountBtns.forEach((b) =>
                        b.classList.remove("highlighted")
                    );
                    btn.classList.add("highlighted");
                    const amount = btn.textContent.replace("$", "");
                    amountInput.value = amount;
                });
            });

            customBtn.addEventListener("click", () => {
                quickAmountBtns.forEach((b) =>
                    b.classList.remove("highlighted")
                );
                amountInput.focus();
            });

            sponsorBtn.addEventListener("click", () => {
                const amount = amountInput.value;
                alert(`Thank you for your donation of $${amount}!`);
            });

            amountInput.addEventListener("input", () => {
                quickAmountBtns.forEach((b) =>
                    b.classList.remove("highlighted")
                );
            });
        }
    };

    /* handleCampaign
  ------------------------------------------------------------------------------------- */
    var handleAtropos = function () {
        if ($(".my-atropos").length > 0) {
            $(".my-atropos").each(function () {
                Atropos({
                    el: this,
                    shadow: true,
                    highlight: true,
                });
            });
        }
    };

    /* handleCampaign
  ------------------------------------------------------------------------------------- */
    var initSwitchPriceValue = function () {
        $(".pricing-container").each(function () {
            const $container = $(this);
            const $tabs = $container.find("[data-pricing]");
            const $prices = $container.find(".price-value");

            function updatePrices(type) {
                $prices.each(function () {
                    const $priceEl = $(this);
                    const monthly = $priceEl.data("monthly");
                    const yearly = $priceEl.data("yearly");
                    const $amountEl = $priceEl.find(".price-month");
                    const $amountNewEl = $priceEl.find(".price-year");
                    const $periodEl = $priceEl.find(".price-period");

                    if (
                        !$amountEl.length ||
                        !$amountNewEl.length ||
                        !$periodEl.length
                    )
                        return;

                    $amountEl.text(monthly);
                    $amountNewEl.text(yearly);

                    if (type === "monthly") {
                        $periodEl.text("/ month");
                        $amountEl.addClass("active");
                        $amountNewEl.removeClass("active");
                    } else {
                        $periodEl.text("/ year");
                        $amountEl.removeClass("active");
                        $amountNewEl.addClass("active");
                    }
                });
            }

            $tabs.on("click", function () {
                const type = $(this).data("pricing");
                updatePrices(type);

                $tabs.removeClass("active");
                $(this).addClass("active");
            });

            updatePrices("monthly");
        });
    };

    /* handleCampaign
  ------------------------------------------------------------------------------------- */
    var handleBookingStep2 = function () {
        if ($(".wg-booking-step").length > 0) {
            const nextBtns = document.querySelectorAll(".btn-step-next");
            const prevBtns = document.querySelectorAll(".btn-step-prev");
            const formSteps = document.querySelectorAll(".form-step");
            const steps = document.querySelectorAll(".steps li");
            let currentStep = 0;

            function showStep(step) {
                formSteps.forEach((form) => form.classList.remove("active"));
                formSteps[step].classList.add("active");

                steps.forEach((s, index) =>
                    s.classList.toggle("active", index <= step)
                );

                formSteps[step].style.animation = "none";
                formSteps[step].offsetHeight;
                formSteps[step].style.animation = "";
            }

            function validateStep(step) {
                const inputs = formSteps[step].querySelectorAll(
                    "input[required], select[required], textarea[required]"
                );
                let valid = true;
                let firstErrorInput = null;

                inputs.forEach((input) => {
                    let errorSpan =
                        input.parentElement.querySelector(".error-msg");
                    if (!errorSpan) {
                        errorSpan = document.createElement("span");
                        errorSpan.classList.add("error-msg");
                        input.parentElement.appendChild(errorSpan);
                    }

                    input.classList.remove("error");
                    errorSpan.style.display = "none";
                    errorSpan.textContent = "";

                    if (input.value.trim() === "") {
                        valid = false;
                        input.classList.add("error");
                        errorSpan.textContent =
                            "Please enter this information.";
                        errorSpan.style.display = "block";
                        if (!firstErrorInput) firstErrorInput = input;
                    } else if (input.type === "email") {
                        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                        if (!emailRegex.test(input.value.trim())) {
                            valid = false;
                            input.classList.add("error");
                            errorSpan.textContent =
                                "The email is not in the correct format.";
                            errorSpan.style.display = "block";
                            if (!firstErrorInput) firstErrorInput = input;
                        }
                    } else if (input.name === "phone") {
                        const phoneRegex = /^(0\d{9}|\+84\d{8,9})$/;
                        if (!phoneRegex.test(input.value.trim())) {
                            valid = false;
                            input.classList.add("error");
                            errorSpan.textContent =
                                "The phone number is invalid.";
                            errorSpan.style.display = "block";
                            if (!firstErrorInput) firstErrorInput = input;
                        }
                    }
                });

                if (firstErrorInput) {
                    firstErrorInput.focus();
                    firstErrorInput.scrollIntoView({
                        behavior: "smooth",
                        block: "center",
                    });
                }

                return valid;
            }

            nextBtns.forEach((btn) => {
                btn.addEventListener("click", () => {
                    if (validateStep(currentStep)) {
                        if (currentStep < formSteps.length - 1) {
                            currentStep++;
                            showStep(currentStep);
                        }
                    }
                });
            });

            prevBtns.forEach((btn) => {
                btn.addEventListener("click", () => {
                    if (currentStep > 0) {
                        currentStep--;
                        showStep(currentStep);
                    }
                });
            });
        }
    };

    /* handleSidebar
  -------------------------------------------------------------------------------------*/
    const handleSidebar = () => {
        const mobileNav = document.getElementById("menu-mobile");
        const offcanvasInstance =
            bootstrap.Offcanvas.getOrCreateInstance(mobileNav);
        $(document).on("click", ".mobile-nav-wrap .nav_link", function () {
            offcanvasInstance.hide();
        });
    };

    /* oneNavOnePage
  -------------------------------------------------------------------------------------*/
    const oneNavOnePage = () => {
        if (!$(".section-onepage").length) return;

        const $navLinks = $(".nav_link");
        const $sections = $(".section");
        const headerHeight = $(".header").outerHeight() || 0;

        $navLinks.on("click", function (e) {
            e.preventDefault();
            const target = $(this).attr("href");
            const targetOffset = $(target).offset().top - headerHeight;
            $("html, body").animate({ scrollTop: targetOffset }, 0);
        });

        const updateActiveMenu = () => {
            const scrollTop = $(window).scrollTop() + headerHeight + 1;
            let current = "";
            $sections.each(function () {
                const $section = $(this);
                const top = $section.offset().top;
                const bottom = top + $section.outerHeight();
                if (scrollTop >= top && scrollTop < bottom)
                    current = $section.attr("id");
            });
            $navLinks
                .removeClass("active")
                .filter(`[href="#${current}"]`)
                .addClass("active");
        };

        $(window).on("scroll", updateActiveMenu);
        updateActiveMenu();
    };

    /* getDataImage
  -------------------------------------------------------------------------------------*/
    const getDataImage = () => {
        if (!$("[data-background]").length) return;
        $("[data-background]").each(function () {
            $(this).css(
                "background-image",
                "url(" + $(this).attr("data-background") + ")"
            );
        });
    };

    /* animateInput
  -------------------------------------------------------------------------------------*/
    const animateInput = () => {
        if (!$(".animated-input").length) return;
        $(".animated-input").each(function () {
            const $input = $(this);
            const $wrapper = $input.next();
            const $placeholderElement = $wrapper.find(".typing-animation");

            const placeholdersData = $input.data("placeholders") || "";
            const placeholders = placeholdersData.split("|");
            const interval = parseInt($input.data("interval")) || 100;

            let currentIndex = 0;
            let isTyping = false;

            function typeIn() {
                isTyping = true;
                $placeholderElement.text(placeholders[currentIndex]);
                $placeholderElement.attr(
                    "class",
                    "placeholder-text typing-animation typing-in"
                );

                setTimeout(() => {
                    isTyping = false;
                }, 2000);
            }

            function typeOut() {
                if (isTyping) return;

                $placeholderElement.attr(
                    "class",
                    "placeholder-text typing-animation typing-out"
                );

                setTimeout(() => {
                    currentIndex = (currentIndex + 1) % placeholders.length;
                    typeIn();
                }, 800);
            }

            typeIn();

            setInterval(() => {
                if (!isTyping) {
                    typeOut();
                }
            }, interval);
        });
    };

    /* Handle Progress
    -------------------------------------------------------------------------*/
    // var handleProgress = function () {
    //     if ($(".progress-cart").length > 0) {
    //         var progressValue = $(".progress-cart .value").data("progress");
    //         setTimeout(function () {
    //             $(".progress-cart .value").css("width", progressValue + "%");
    //         }, 800);
    //     }
    // };

    // Dom Ready
    $(function () {
        animateCounters();
        headerSticky();
        headerFixed();
        handleFooter();
        video();
        infiniteslide();
        tabSlide();
        tabs();
        cursorCustom();
        hoverActive();
        hoverTabs();
        accordionActive();
        goTop();
        wow();
        fillterIso();
        datePicker();
        rangeSlide();
        dropdownSelect();
        handleBookingStep();
        handleProgress();
        handleCampaign();
        handleAtropos();
        initSwitchPriceValue();
        handleBookingStep2();
        handleSidebar();
        oneNavOnePage();
        getDataImage();
        animateInput();
    });
})(jQuery);
