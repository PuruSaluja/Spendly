// main.js — students will add JavaScript here as features are built

// ------------------------------------------------------------------ //
// Landing page: "See how it works" video modal                        //
// ------------------------------------------------------------------ //
(function () {
    var openBtn = document.getElementById("how-it-works-btn");
    var modal = document.getElementById("video-modal");
    if (!openBtn || !modal) return; // not on the landing page

    var closeBtn = modal.querySelector(".modal-close");
    var videoBox = modal.querySelector(".modal-video");
    var videoUrl = modal.getAttribute("data-video-url");

    function openModal() {
        // The iframe is created only while the modal is open, so the
        // video never loads (or plays) in the background.
        var frame = document.createElement("iframe");
        frame.src = videoUrl + "?autoplay=1&rel=0";
        frame.title = "Spendly walkthrough video";
        frame.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
        frame.allowFullscreen = true;
        videoBox.appendChild(frame);

        modal.classList.add("is-open");
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-open");
        closeBtn.focus();
    }

    function closeModal() {
        // Removing the iframe from the page stops the video completely.
        videoBox.innerHTML = "";

        modal.classList.remove("is-open");
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
        openBtn.focus();
    }

    openBtn.addEventListener("click", openModal);
    closeBtn.addEventListener("click", closeModal);

    // Click on the dark backdrop (but not on the video box) closes it.
    modal.addEventListener("click", function (event) {
        if (event.target === modal) closeModal();
    });

    // Escape key closes it too.
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && modal.classList.contains("is-open")) {
            closeModal();
        }
    });
})();
