// 01- This is for toggle modal open and close **************************************
document.addEventListener("DOMContentLoaded", () => {
    const filterContainer = document.getElementById("filterContainer");
    const toggleFilterButton = document.getElementById("toggleFilter");
    const closeFilterButton = document.getElementById("closeFilter");
    const applyFiltersButton = document.getElementById("applyFilters");
    const resetFiltersButton = document.getElementById("resetFilters");
    // Open the filter modal
    toggleFilterButton.addEventListener("click", (e) => {
        e.preventDefault();
        filterContainer.classList.add("visible");
    });
    // Close the filter modal
    closeFilterButton.addEventListener("click", () => {
        closeModal();
    });
    // Close the modal when clicking outside the modal content
    filterContainer.addEventListener("click", (e) => {
        if (e.target === filterContainer) {
            closeModal();
        }
    });
    // Helper functions
    function closeModal() {
        filterContainer.classList.remove("visible");
    }
});



// 02- this is for dyanimc number counting **************************************
const counters = document.querySelectorAll('.count-digit');
counters.forEach(counter => {
    const updateCount = () => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;

        const increment = target / 200;

        if (count < target) {
            counter.innerText = Math.ceil(count + increment);
            setTimeout(updateCount, 20);
        } else {
            counter.innerText = target;
        }
    };
    updateCount();
});

//03- this is for show active tag **************************************
document.addEventListener("DOMContentLoaded", function () {
    const iconBoxes = document.querySelectorAll('.icon-box');
    const navLinks = document.querySelectorAll('.nav-link1');

    // Get the current URL path
    const currentPath = window.location.pathname; // e.g., /typeNews/Regulation%20Changes
    const activeType = decodeURIComponent(currentPath.split('/')[2] || ""); // Extract "Regulation Changes"

    iconBoxes.forEach(box => {
        const link = box.querySelector('.nav-link1');
        const linkType = link.getAttribute('data-type'); // Get the data-type from the link

        // If the link type matches the active type, add 'active' class to the box
        if (linkType === activeType) {
            box.classList.add('active');
        }

        // Add click event listener to handle dynamic class addition
        link.addEventListener('click', function () {
            // Remove active class from all icon-boxes
            iconBoxes.forEach(b => b.classList.remove('active'));

            // Add active class to the clicked box
            box.classList.add('active');
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll(".company-item");
    const loadMoreButton = document.getElementById("load-more");

    let visibleCount = 5; // Initially show 5 items
    const increment = 2; // Number of items to show per click

    loadMoreButton.addEventListener("click", function () {
      let displayed = 0;

      // Show hidden items incrementally
      items.forEach((item, index) => {
        if (index >= visibleCount && displayed < increment) {
          item.style.display = "block";
          displayed++;
        }
      });

      visibleCount += increment;

      // Hide the button if all items are visible
      if (visibleCount >= items.length) {
        loadMoreButton.style.display = "none";
      }
    });
  });



  document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll(".contry-item");
    const loadMoreButton = document.getElementById("load-more-country");

    let visibleCount = 5; // Initially show 5 items
    const increment = 2; // Number of items to show per click

    loadMoreButton.addEventListener("click", function () {
      let displayed = 0;

      // Show hidden items incrementally
      items.forEach((item, index) => {
        if (index >= visibleCount && displayed < increment) {
          item.style.display = "block";
          displayed++;
        }
      });

      visibleCount += increment;

      // Hide the button if all items are visible
      if (visibleCount >= items.length) {
        loadMoreButton.style.display = "none";
      }
    });
  });

  document.addEventListener("DOMContentLoaded", function () {
    const regItems = document.querySelectorAll(".reg-item");
    const loadMoreRegButton = document.getElementById("load-more-reg");

    let visibleRegCount = 5; // Initially show 5 items
    const incrementReg = 2; // Number of items to show per click

    loadMoreRegButton.addEventListener("click", function () {
      let displayed = 0;

      // Show hidden regulatory body items incrementally
      regItems.forEach((item, index) => {
        if (index >= visibleRegCount && displayed < incrementReg) {
          item.style.display = "block";
          displayed++;
        }
      });

      visibleRegCount += incrementReg;

      // Hide the button if all regulatory body items are visible
      if (visibleRegCount >= regItems.length) {
        loadMoreRegButton.style.display = "none";
      }
    });
  });

