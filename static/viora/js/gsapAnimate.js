/**
 
 * Project Name: Viora AI-powered Multipurpose HTML Themes
 * Project Description: Viora is an AI-powered multipurpose HTML theme designed for speed and versatility. Perfect for business, tech startups, portfolios, and more with clean, modern design.        Easily customizable and optimized for performance across all devices
 * Tags: AI, HTML, Template, Theme, Website, Responsive, Multipurpose, Portfolio, Business, Design
 * Version: 1.0.0
 * This product is available exclusively on Themeforest
 * File name: gsapaAnimate.js
 ----------------------------------------------------------------------------------


 1. effectScrollSmoother
 2. fixedThumb
 3. animateImgItem
 5. animationScaleImg
 6. effectHoverButton
 7. stackElement
 8. animation_text
 9. changetext
 10. scrollTransform
 11. scrollBanners
 12. effectScaleImg
 13. scrollEffectTransformItem
 14. initRevealElements
 15. imageParallax
 16. effectBounce
 17. initCursorParallax
 18. effectSectionTriger

 
**/

(function ($) {
    "use strict";
    // DOM Ready
    gsap.registerPlugin(ScrollTrigger);

    /* effectScrollSmoother
  ------------------------------------------------------------------------------------- */
    const effectScrollSmoother = () => {
        if (!$("#smooth-wrapper").length) return;
        gsap.registerPlugin(ScrollSmoother);
        const smoother = ScrollSmoother.create({
            wrapper: "#smooth-wrapper",
            content: "#smooth-content",
            smooth: 1.2,
            effects: true,
        });
    };

    /* fixedThumb
  ------------------------------------------------------------------------------------- */
    const fixedThumb = () => {
        let pc = gsap.matchMedia();
        pc.add("(min-width: 992px)", () => {
            const $wrap = $(".fixed-thumb-wrap");
            if ($wrap.length > 0) {
                const $thumb = $wrap.find(".fixed-thumb");
                if ($thumb.length > 0) {
                    let startOffset = $thumb.data("startoffset") || 320;
                    gsap.timeline({
                        scrollTrigger: {
                            trigger: $wrap[0],
                            start: `top center-=${startOffset}`,
                            end: "bottom 65%",
                            pin: $thumb[0],
                            pinSpacing: false,
                            scrub: 1,
                        },
                    });
                }
            }
        });
    };

    /* stackElement
  -------------------------------------------------------------------------*/
    var stackElement = function () {
        let pr = gsap.matchMedia();
        if ($(".stack-element").length > 0) {
            pr.add("(min-width: 767px)", () => {
                $(".stack-element").each(function () {
                    let stack = $(this);
                    let totalHeight;
                    let scrollTriggerInstances = [];

                    const updateTotalHeight = () => {
                        totalHeight = stack
                            .find(".stack-content-wrap")
                            .outerHeight();

                        scrollTriggerInstances.forEach((instance) => {
                            instance.kill();
                        });
                        scrollTriggerInstances = [];

                        stack[0]
                            .querySelectorAll(".element")
                            .forEach((element, index) => {
                                const tabHeight = element.offsetHeight;
                                totalHeight -= tabHeight;

                                const pinTrigger = ScrollTrigger.create({
                                    trigger: element,
                                    scrub: 1,
                                    start: "top 100",
                                    end: `+=${totalHeight}`,
                                    pin: true,
                                    pinSpacing: false,
                                });

                                scrollTriggerInstances.push(pinTrigger);
                            });
                    };

                    updateTotalHeight();
                    window.addEventListener("resize", updateTotalHeight);
                });
            });
        }
    };

    /* animationScaleImg
  ------------------------------------------------------------------------------------- */
    var animationScaleImg = function () {
        if ($(".scale-img").length > 0) {
            var scale = document.querySelectorAll(".scale-img");
            var image = document.querySelectorAll(".scale-img img");
            scale.forEach((item) => {
                gsap.to(item, {
                    scale: 1,
                    duration: 1,
                    ease: "power1.out",
                    scrollTrigger: {
                        trigger: item,
                        start: "top 86%",
                        end: "bottom top",
                        toggleActions: "play reverse play reverse",
                    },
                });
            });
            image.forEach((image) => {
                gsap.set(image, {
                    scale: 1.3,
                });
                gsap.to(image, {
                    scale: 1,
                    duration: 1,
                    scrollTrigger: {
                        trigger: image,
                        start: "top 86%",
                        end: "bottom top",
                        toggleActions: "play reverse play reverse",
                    },
                });
            });
        }
    };

    /* effectHoverButton
  ------------------------------------------------------------------------------------- */
    const effectHoverButton = () => {
        if (!$(".btn-hover").length) return;
        const all_btns = gsap.utils.toArray(".btn_wrapper");
        if (all_btns.length > 0) {
            var all_btn = gsap.utils.toArray(".btn_wrapper");
        }
        const all_btn_cirlce = gsap.utils.toArray(".btn-item");
        all_btn.forEach((btn, i) => {
            $(btn).mousemove(function (e) {
                callParallax(e);
            });
            function callParallax(e) {
                parallaxIt(e, all_btn_cirlce[i], 80);
            }

            function parallaxIt(e, target, movement) {
                var $this = $(btn);
                var relX = e.pageX - $this.offset().left;
                var relY = e.pageY - $this.offset().top;

                gsap.to(target, 0.5, {
                    x: ((relX - $this.width() / 2) / $this.width()) * movement,
                    y:
                        ((relY - $this.height() / 2) / $this.height()) *
                        movement,
                    ease: "Power4.easeOut",
                });
            }
            $(btn).mouseleave(function (e) {
                gsap.to(all_btn_cirlce[i], 0.5, {
                    x: 0,
                    y: 0,
                    ease: "Power4.easeOut",
                });
            });
        });
    };

    /* animateImgItem
    -------------------------------------------------------------------------------------*/
    var animateImgItem = function () {
        const isSmallScreen = window.matchMedia("(max-width: 991px)").matches;

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const delay =
                            parseFloat(
                                entry.target.getAttribute("data-delay")
                            ) || 0;
                        setTimeout(() => {
                            $(entry.target).addClass("active-animate");
                        }, delay * 1000);
                    }
                });
            },
            {
                threshold: isSmallScreen ? 0.1 : 0.1,
            }
        );

        const elements = $(
            ".tf-animateCLP-left, .tf-animateCLP-up, .tf-animateCLP-right, .tf-animateCLP-down"
        );
        elements.each(function () {
            observer.observe(this);
        });

        const checkVisible = () => {
            elements.each(function () {
                const sectionOffsetTop = $(this).offset().top;
                const sectionHeight = $(this).outerHeight();
                const scrollPosition = $(window).scrollTop();
                const windowHeight = $(window).height();

                if (
                    scrollPosition + windowHeight * 0.9 > sectionOffsetTop &&
                    scrollPosition < sectionOffsetTop + sectionHeight
                ) {
                    const delay = parseFloat($(this).attr("data-delay")) || 0;
                    setTimeout(() => {
                        $(this).addClass("active-animate");
                    }, delay * 1000);
                }
            });
        };

        $(document).ready(checkVisible);
        $(window).on("scroll", checkVisible);
    };

    /* animation_text
  -------------------------------------------------------------------------*/
    const animation_text = () => {
        const $splitText = $(".split-text");
        if (!$splitText.length) return;
        gsap.registerPlugin(SplitText);
        const makeScrollTrigger = (target, extra = {}) => ({
            trigger: target,
            start: "top 86%",
            toggleActions: "play none none reverse",
            once: true,
            ...extra,
        });

        $splitText.each((_, el) => {
            const $el = $(el);
            const $target = $el.find("p, a").get(0) || el;
            const hasClass = $el.hasClass.bind($el);

            const pxl_split = new SplitText($target, {
                type: "words, chars",
                lineThreshold: 0.5,
                linesClass: "split-line",
            });
            let splitSet = pxl_split.chars;

            gsap.set($target, { perspective: 400 });

            // Base settings
            const settings = {
                scrollTrigger: makeScrollTrigger($target),
                duration: 0.9,
                stagger: 0.02,
                ease: "power3.out",
            };

            if (hasClass("effect-fade")) {
                Object.assign(settings, { opacity: 0 });
            }
            if (hasClass("effect-right")) {
                Object.assign(settings, { opacity: 0, x: 50 });
            }
            if (hasClass("effect-left")) {
                Object.assign(settings, { opacity: 0, x: -50 });
            }
            if (hasClass("effect-up")) {
                Object.assign(settings, { opacity: 0, y: 20 });
            }
            if (hasClass("effect-down")) {
                Object.assign(settings, { opacity: 0, y: -80 });
            }
            if (hasClass("effect-rotate")) {
                Object.assign(settings, { opacity: 0, rotateX: "50deg" });
            }
            if (hasClass("effect-scale")) {
                Object.assign(settings, { opacity: 0, scale: 0.5 });
            }
            if (
                hasClass("split-lines-transform") ||
                hasClass("split-lines-rotation-x")
            ) {
                pxl_split.split({
                    type: "lines",
                    lineThreshold: 0.5,
                    linesClass: "split-line",
                });
                splitSet = pxl_split.lines;
                Object.assign(settings, { opacity: 0, stagger: 0.2 });

                if (hasClass("split-lines-rotation-x")) {
                    Object.assign(settings, {
                        rotationX: -120,
                        transformOrigin: "top center -50",
                    });
                } else {
                    Object.assign(settings, { yPercent: 100, autoAlpha: 0 });
                }
            }
            if (hasClass("split-words-scale")) {
                pxl_split.split({ type: "words" });
                splitSet = pxl_split.words;

                splitSet.forEach((elw, i) => {
                    gsap.set(elw, {
                        opacity: 0,
                        scale: i % 2 === 0 ? 0 : 2,
                        force3D: true,
                    });
                });

                gsap.to(splitSet, {
                    scrollTrigger: makeScrollTrigger(el),
                    rotateX: 0,
                    scale: 1,
                    opacity: 1,
                    ease: "power3.out",
                    stagger: 0.05,
                });
                return;
            }

            // Blur fade
            if (hasClass("effect-blur-fade")) {
                pxl_split.split({ type: "words" });
                splitSet = pxl_split.words;

                gsap.fromTo(
                    splitSet,
                    { opacity: 0, filter: "blur(10px)", y: 20 },
                    {
                        opacity: 1,
                        filter: "blur(0px)",
                        y: 0,
                        duration: 1,
                        stagger: 0.1,
                        ease: "power3.out",
                        scrollTrigger: makeScrollTrigger($target),
                    }
                );
                return;
            }
            gsap.from(splitSet, settings);
        });
    };

    /* scrollTransform
    -------------------------------------------------------------------------------------*/
    const scrollTransform = () => {
        document
            .querySelectorAll(".scroll-transform")
            .forEach(function (element) {
                const direction = element.dataset.direction || "up";
                const distance = element.dataset.distance || "10%";
                const rotateValue = element.dataset.rotate;
                const rotateOnly = element.dataset.rotateOnly === "true";

                let animationProperty;
                switch (direction.toLowerCase()) {
                    case "left":
                        animationProperty = { x: `-${distance}` };
                        break;
                    case "right":
                        animationProperty = { x: `${distance}` };
                        break;
                    case "up":
                        animationProperty = { y: `-${distance}` };
                        break;
                    case "down":
                        animationProperty = { y: `${distance}` };
                        break;
                    default:
                        animationProperty = { y: `-${distance}` };
                }

                if (!rotateOnly) {
                    gsap.to(element, {
                        ...animationProperty,
                        scrollTrigger: {
                            trigger: element,
                            start: "top bottom",
                            end: "bottom top",
                            scrub: 3,
                        },
                    });
                }

                if (rotateValue !== undefined) {
                    gsap.to(element, {
                        rotate: rotateValue,
                        scrollTrigger: {
                            trigger: element,
                            start: "top 60%",
                            end: "bottom top",
                            scrub: 2,
                        },
                    });
                }
            });
    };

    /* scrollBanners
    -------------------------------------------------------------------------------------*/
    const scrollBanners = () => {
        var st = $(".banner-stripe .text-container");
        st.each(function () {
            const settings = {
                scrollTrigger: {
                    trigger: this,
                    start: "top bottom",
                    end: "bottom top",
                    scrub: 1,
                    markers: false,
                },
                ease: "none",
            };
            if ($(this).hasClass("effect-left")) {
                settings.x = "-7%";
            }
            if ($(this).hasClass("effect-right")) {
                settings.x = "7%";
            }
            gsap.to(this, settings);
        });
    };

    /* effectScaleImg
    -------------------------------------------------------------------------------------*/
    const effectScaleImg = () => {
        if ($(".scale-up-img").length > 0) {
            document.querySelectorAll(".scale-up-img").forEach((section) => {
                let tl = gsap.timeline({
                    scrollTrigger: {
                        trigger: section,
                        start: "top bottom",
                        end: "bottom center",
                        scrub: 1,
                        markers: false,
                    },
                });

                tl.to(section.querySelector(".scale-up"), {
                    scale: 1.15,
                    duration: 1,
                });
            });
        }
    };

    /* scrollEffectTransformItem
    -------------------------------------------------------------------------------------*/
    const scrollEffectTransformItem = () => {
        if ($(".sticky-section").length > 0) {
            window.addEventListener("load", () => {
                const cards = gsap.utils.toArray(".image-card");
                const imagesWrapper = document.querySelector(".images-wrapper");

                const wrapperRect = imagesWrapper.getBoundingClientRect();
                const centerX = wrapperRect.width / 2;
                const centerY = wrapperRect.height / 2;

                const tl = gsap.timeline({
                    scrollTrigger: {
                        trigger: ".sticky-section",
                        start: "top top",
                        end: "bottom bottom",
                        scrub: 1,
                    },
                });

                cards.forEach((card, index) => {
                    const rect = card.getBoundingClientRect();
                    const wrapperOffset = imagesWrapper.getBoundingClientRect();

                    const startX =
                        rect.left - wrapperOffset.left + rect.width / 2;
                    const startY =
                        rect.top - wrapperOffset.top + rect.height / 2;

                    const deltaX = centerX - startX;
                    const deltaY = centerY - startY;

                    const delay = index * 0.15;

                    tl.to(
                        card,
                        {
                            opacity: 1,
                            duration: 0.3,
                            ease: "power2.out",
                        },
                        delay
                    );

                    tl.to(
                        card,
                        {
                            x: deltaX,
                            y: deltaY,
                            scale: 1.2,
                            duration: 0.5,
                            opacity: 0,
                            ease: "power2.inOut",
                        },
                        delay + 0.1
                    );

                    tl.to(
                        card,
                        {
                            opacity: 0,
                            scale: 0.8,
                            duration: 0.4,
                            ease: "power2.in",
                        },
                        delay + 0.5
                    );
                });

                gsap.to(".title-section", {
                    scrollTrigger: {
                        trigger: ".sticky-section",
                        start: "top top",
                        end: "50% top",
                        scrub: 1,
                    },
                    scale: 0.8,
                    ease: "power2.inOut",
                });
            });
        }
    };

    /* initRevealElements
    -------------------------------------------------------------------------------------*/
    const initRevealElements = () => {
        if ($("[data-ns-animate]").length > 0) {
            const elements = document.querySelectorAll("[data-ns-animate]");
            const Springer = window.Springer.default;
            elements.forEach((elem) => {
                const duration = elem.getAttribute("data-duration")
                    ? parseFloat(elem.getAttribute("data-duration"))
                    : 0.6;
                const delay = elem.getAttribute("data-delay")
                    ? parseFloat(elem.getAttribute("data-delay"))
                    : 0;
                const offset = elem.getAttribute("data-offset")
                    ? parseFloat(elem.getAttribute("data-offset"))
                    : 60;
                const instant =
                    elem.hasAttribute("data-instant") &&
                    elem.getAttribute("data-instant") !== "false";
                const start = elem.getAttribute("data-start") || "top 90%";
                const end = elem.getAttribute("data-end") || "top 50%";
                const direction = elem.getAttribute("data-direction") || "down";
                const useSpring = elem.hasAttribute("data-spring");
                const spring = useSpring ? Springer(0.2, 0.8) : null;
                const rotation = elem.getAttribute("data-rotation")
                    ? parseFloat(elem.getAttribute("data-rotation"))
                    : 0;
                const animationType =
                    elem.getAttribute("data-animation-type") || "from";
                elem.style.opacity = "1";
                elem.style.filter = "blur(0)";
                let animationProps;
                if (animationType === "to") {
                    animationProps = {
                        opacity: 1,
                        filter: "blur(0)",
                        duration,
                        delay,
                        ease: useSpring ? spring : "power2.out",
                    };
                    if (rotation !== 0) {
                        animationProps.rotation = rotation;
                    }
                } else {
                    animationProps = {
                        opacity: 0,
                        filter: "blur(16px)",
                        duration,
                        delay,
                        ease: useSpring ? spring : "power2.out",
                    };
                    if (rotation !== 0) {
                        animationProps.rotation = rotation;
                    }
                }
                if (!instant) {
                    animationProps.scrollTrigger = {
                        trigger: elem,
                        start,
                        end,
                        scrub: false,
                    };
                }
                switch (direction) {
                    case "left":
                        animationProps.x = -offset;
                        break;
                    case "right":
                        animationProps.x = offset;
                        break;
                    case "down":
                        animationProps.y = offset;
                        break;
                    case "up":
                    default:
                        animationProps.y = -offset;
                        break;
                }
                if (animationType === "to") {
                    gsap.to(elem, animationProps);
                } else {
                    gsap.from(elem, animationProps);
                }
            });
        }
    };

    /* changetext
    -------------------------------------------------------------------------------------*/
    const changetext = () => {
        if (!$(".text-change-color").length) return;
        const split = new SplitText(".text-change-color", { type: "lines" });
        gsap.registerPlugin(SplitText);
        split.lines.forEach((target) => {
            gsap.to(target, {
                backgroundPositionX: 0,
                ease: "none",
                scrollTrigger: {
                    trigger: target,
                    scrub: 1,
                    start: "top 85%",
                    end: "bottom center",
                },
            });
        });
    };

    /* imgaeParallax
    -------------------------------------------------------------------------------------*/
    const imageParallax = () => {
        if ($(".parallax-container").length) {
            const $ttPageHeader = $(".parallax-container");
            const $phBgMedia = $(".parallax-image, .parallax-video");
            if ($phBgMedia.length) {
                gsap.to(".image-inner, .video-inner", {
                    yPercent: 40,
                    ease: "none",
                    scrollTrigger: {
                        trigger: $ttPageHeader,
                        start: "top top",
                        end: "bottom top",
                        scrub: true,
                        markers: false,
                    },
                });
            }
        }
    };

    /* effectBounce
    -------------------------------------------------------------------------------------*/
    const effectBounce = () => {
        if ($(".effectBounce").length) {
            document.querySelectorAll(".effectBounce").forEach((el, i) => {
                const direction = el.dataset.direction || "up";
                const delay = parseFloat(el.dataset.delay) || "0";
                let fromVars = { opacity: 0 };

                switch (direction) {
                    case "up":
                        fromVars.y = 70;
                        break;
                    case "down":
                        fromVars.y = -70;
                        break;
                    case "left":
                        fromVars.x = -70;
                        break;
                    case "right":
                        fromVars.x = 70;
                        break;
                }

                gsap.fromTo(el, fromVars, {
                    x: 0,
                    y: 0,
                    opacity: 1,
                    duration: 1.3,
                    ease: "bounce.out",
                    delay: delay,
                    scrollTrigger: {
                        trigger: el,
                        start: "top 85%",
                        toggleActions: "play none none reverse",
                    },
                });
            });
        }
    };

    /* effectFlowCursor
    -------------------------------------------------------------------------------------*/
    const initCursorParallax = () => {
        const containers = document.querySelectorAll(".floating-images");

        if (!containers.length) return;

        containers.forEach((container) => {
            const cards = container.querySelectorAll(".floating-card");
            container.addEventListener("mousemove", (e) => {
                const rect = container.getBoundingClientRect();
                const moveX = (e.clientX - (rect.left + rect.width / 2)) * 0.05;
                const moveY = (e.clientY - (rect.top + rect.height / 2)) * 0.05;

                gsap.to(container, {
                    x: moveX,
                    y: moveY,
                    duration: 1,
                    ease: "power2.out",
                });
            });
            container.addEventListener("mouseleave", () => {
                gsap.to(container, {
                    x: 0,
                    y: 0,
                    duration: 1,
                    ease: "power2.out",
                });
            });

            cards.forEach((card, index) => {
                gsap.to(card, {
                    y: "+=20",
                    duration: 2 + index * 0.3,
                    repeat: -1,
                    yoyo: true,
                    ease: "sine.inOut",
                });

                gsap.to(card, {
                    rotation: index % 2 === 0 ? 2 : -2,
                    duration: 3 + index * 0.2,
                    repeat: -1,
                    yoyo: true,
                    ease: "sine.inOut",
                });
            });
        });
    };

    /* effectSectionTriger
    -------------------------------------------------------------------------------------*/
    const effectSectionTriger = () => {
        const triggerSlices = [...document.querySelectorAll(".section-triger")];
        triggerSlices.forEach((section) => {
            const slices = section.querySelectorAll(".uncover_slice");
            const image = section.querySelector(".image-inner");

            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: section,
                    start: "50% bottom",
                    markers: false,
                },
            });

            tl.to(
                slices,
                {
                    height: 0,
                    ease: "power6.inOut",
                    duration: 0.6,
                    stagger: { each: 0.3 },
                },
                "start"
            ).to(
                image,
                {
                    scale: 1.3,
                    duration: 1.5,
                    ease: "power6.inOut",
                },
                "start"
            );
        });
    };

    $(function () {
        effectScrollSmoother();
        fixedThumb();
        animateImgItem();
        animationScaleImg();
        effectHoverButton();
        stackElement();
        animation_text();
        changetext();
        scrollTransform();
        scrollBanners();
        effectScaleImg();
        scrollEffectTransformItem();
        initRevealElements();
        imageParallax();
        effectBounce();
        initCursorParallax();
        effectSectionTriger();
    });
})(jQuery);
