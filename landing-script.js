// GSAP Animations
gsap.from(".hero-title", { duration: 1.5, x: -100, opacity: 0, ease: "power3.out" });
gsap.from(".hero-subtitle", { duration: 1.5, x: -100, opacity: 0, ease: "power3.out", delay: 0.3 });
gsap.from(".cta-button", { duration: 1.5, y: 50, opacity: 0, ease: "bounce.out", delay: 0.6 });

gsap.from(".odds-item", {
    scrollTrigger: ".odds-item",
    duration: 1,
    y: 50,
    opacity: 0,
    stagger: 0.3,
    ease: "power2.out"
});

gsap.from(".testimonials p", {
    scrollTrigger: ".testimonials p",
    duration: 1,
    y: 50,
    opacity: 0,
    stagger: 0.3,
    ease: "power2.out"
});

// Scrolling Animation for Background Video
gsap.to(".background-video", {
    yPercent: 20, // Moves the video down by 20% as you scroll
    ease: "none",
    scrollTrigger: {
        trigger: ".hero",
        start: "top top", // When the top of the hero section reaches the top of the viewport
        end: "bottom top", // When the bottom of the hero section reaches the top of the viewport
        scrub: true // Smoothly animates in sync with scrolling
    }
});
