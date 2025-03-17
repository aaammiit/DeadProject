// 01 --*************************************************************
function filterCountries() {
    const searchInput = document.getElementById('countrySearch').value.toLowerCase(); // Get input value
    const checkboxes = document.querySelectorAll('#countryOptions .country-label'); // Get all checkbox labels
    const checkboxContainer = document.getElementById('countryOptions'); // Parent container for checkboxes
    const selectedCountriesContainer = document.getElementById('selectedCountries'); // Selected countries container
    const selectedCount = document.getElementById('selectedCount1');
    // Separate matched and unmatched checkboxes based on search input
    const matched = [];
    const unmatched = [];
    checkboxes.forEach(label => {
        const text = label.textContent.trim().toLowerCase(); // Get checkbox text
        if (text.includes(searchInput)) {
            matched.push(label); // Add to matched list
        } else {
            unmatched.push(label); // Add to unmatched list
        }
    });
    // Reorder checkboxes: matched first, then unmatched
    checkboxContainer.innerHTML = ''; // Clear current checkboxes
    matched.forEach(label => checkboxContainer.appendChild(label)); // Append matched first
    unmatched.forEach(label => checkboxContainer.appendChild(label)); // Append unmatched next
    // Handle selected checkboxes
    const selectedCheckboxes = document.querySelectorAll('#countryOptions input[type="checkbox"]:checked');
    selectedCountriesContainer.innerHTML = ''; // Clear the selected countries container
    let isAnySelected = false; // Flag to track if any checkbox is selected
    selectedCheckboxes.forEach(checkbox => {
        const countryName = checkbox.value;
        const selectedLabel = document.createElement('div');
        selectedLabel.classList.add('selected-country');
        selectedLabel.innerHTML = `${countryName} <button class="remove-btn" onclick="removeSelectedCountry('${countryName}')">X</button>`;
        selectedCountriesContainer.appendChild(selectedLabel);
        // Mark as selected
        isAnySelected = true;
    });
    selectedCount.textContent = selectedCheckboxes.length;
    // Toggle visibility of the selected countries section
    if (isAnySelected) {
        selectedCountriesContainer.style.display = 'flex'; // Show the section
    } else {
        selectedCountriesContainer.style.display = 'none'; // Hide the section
    }
}
// Function to remove selected country when "X" is clicked
function removeSelectedCountry(countryName) {
    const checkboxes = document.querySelectorAll('#countryOptions input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === countryName) {
            checkbox.checked = false; // Uncheck the checkbox
        }
    });
    filterCountries(); // Re-filter the countries after removal
}
// Ensure the function is called when page loads or when a checkbox is clicked
document.addEventListener('DOMContentLoaded', filterCountries);







// 02--*************************************************************
function filterRegulatory() {
    const searchInput = document.getElementById('regBodySearch').value.toLowerCase(); // Get input value
    const checkboxes = document.querySelectorAll('#regBodyOptions .regulatory-label'); // Get all checkbox labels
    const checkboxContainer = document.getElementById('regBodyOptions'); // Parent container for checkboxes
    const selectedCountriesContainer = document.getElementById('selectedRegulatory'); // Selected countries container
    const selectedCount = document.getElementById('selectedCount');
    // Separate matched and unmatched checkboxes
    const matched = [];
    const unmatched = [];
    checkboxes.forEach(label => {
        const text = label.textContent.trim().toLowerCase(); // Get checkbox text
        if (text.includes(searchInput)) {
            matched.push(label); // Add to matched list
        } else {
            unmatched.push(label); // Add to unmatched list
        }
    });
    // Reorder checkboxes: matched first, then unmatched
    checkboxContainer.innerHTML = ''; // Clear current checkboxes
    matched.forEach(label => checkboxContainer.appendChild(label)); // Append matched first
    unmatched.forEach(label => checkboxContainer.appendChild(label)); // Append unmatched next
    // Handle selected checkboxes
    const selectedCheckboxes = document.querySelectorAll('#regBodyOptions input[type="checkbox"]:checked');
    selectedCountriesContainer.innerHTML = ''; // Clear the selected countries container
    let isAnySelected = false; // Flag to track if any checkbox is selected
    selectedCheckboxes.forEach(checkbox => {
        const regName = checkbox.value;
        const selectedLabel = document.createElement('div');
        selectedLabel.classList.add('selected-regulatory');
        selectedLabel.innerHTML = `${regName} <button class="remove-btn1" onclick="removeSelectedreg('${regName}')">X</button>`;
        selectedCountriesContainer.appendChild(selectedLabel);
        // Mark as selected
        isAnySelected = true;
    });
    selectedCount.textContent = selectedCheckboxes.length;
    // Toggle visibility of the selected countries section
    if (isAnySelected) {
        selectedCountriesContainer.style.display = 'flex'; // Show the section
    } else {
        selectedCountriesContainer.style.display = 'none'; // Hide the section
    }
}

// Function to remove selected country when "X" is clicked
function removeSelectedreg(regName) {
    const checkboxes = document.querySelectorAll('#regBodyOptions input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === regName) {
            checkbox.checked = false; // Uncheck the checkbox
        }
    });
    filterRegulatory(); // Re-filter the countries after removal
}

// Add event listeners
document.addEventListener('DOMContentLoaded', filterRegulatory);
// document.getElementById('regBodyOptions').addEventListener('change', filterRegulatory); // Re-run filter on checkbox change






// 03--*************************************************************
function filterIndustry() {
    const searchInput = document.getElementById('industrySearch').value.toLowerCase(); // Get input value
    const checkboxes = document.querySelectorAll('#industryOptions .industry-label'); // Get all checkbox labels
    const checkboxContainer = document.getElementById('industryOptions'); // Parent container for checkboxes
    const selectedContainer = document.getElementById('selectedIndustry'); // Container for selected industries
    const selectedCount = document.getElementById('selectedIndustryCount'); // Element for selected count
    // Separate matched and unmatched checkboxes
    const matched = [];
    const unmatched = [];
    checkboxes.forEach(label => {
        const text = label.textContent.trim().toLowerCase(); // Get checkbox text
        if (text.includes(searchInput)) {
            matched.push(label); // Add to matched list
        } else {
            unmatched.push(label); // Add to unmatched list
        }
    });
    // Reorder checkboxes: matched first, then unmatched
    checkboxContainer.innerHTML = ''; // Clear current checkboxes
    matched.forEach(label => checkboxContainer.appendChild(label)); // Append matched first
    unmatched.forEach(label => checkboxContainer.appendChild(label)); // Append unmatched next
    // Handle selected checkboxes
    const selectedCheckboxes = document.querySelectorAll('#industryOptions input[type="checkbox"]:checked');
    selectedContainer.innerHTML = ''; // Clear the selected industries container
    if (selectedCheckboxes.length > 0) {
        selectedCheckboxes.forEach(checkbox => {
            const industryName = checkbox.value;
            const selectedLabel = document.createElement('div');
            selectedLabel.classList.add('selected-industry-item');
            selectedLabel.innerHTML = `
                ${industryName} 
                <button class="remove-btn" onclick="removeSelectedIndustry('${industryName}')">X</button>
            `;
            selectedContainer.appendChild(selectedLabel);
        });
        selectedContainer.style.display = 'flex'; // Show the container
    } else {
        selectedContainer.style.display = 'none'; // Hide the container if none selected
    }
    // Update the count of selected industries
    selectedCount.textContent = selectedCheckboxes.length;
}
// Function to remove selected industry when "X" is clicked
function removeSelectedIndustry(industryName) {
    const checkboxes = document.querySelectorAll('#industryOptions input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === industryName) {
            checkbox.checked = false; // Uncheck the checkbox
        }
    });
    filterIndustry(); // Re-filter the industries after removal
}
// Initialize the filter when the page loads
document.addEventListener('DOMContentLoaded', filterIndustry);







// 04--*************************************************************
function filterRegulation() {
    const searchInput = document.getElementById('regulationSearch').value.toLowerCase(); // Get search input value
    const checkboxes = document.querySelectorAll('#regulationOptions .regulation-label'); // Get all checkbox labels
    const checkboxContainer = document.getElementById('regulationOptions'); // Parent container for checkboxes
    const selectedContainer = document.getElementById('selectedRegulation'); // Container for selected regulations
    const selectedCount = document.getElementById('selectedRegulationCount'); // Element for selected count

    // Separate matched and unmatched checkboxes
    const matched = [];
    const unmatched = [];
    checkboxes.forEach(label => {
        const text = label.textContent.trim().toLowerCase(); // Get checkbox text
        if (text.includes(searchInput)) {
            matched.push(label); // Add to matched list
        } else {
            unmatched.push(label); // Add to unmatched list
        }
    });

    // Reorder checkboxes: matched first, then unmatched
    checkboxContainer.innerHTML = ''; // Clear current checkboxes
    matched.forEach(label => checkboxContainer.appendChild(label)); // Append matched first
    unmatched.forEach(label => checkboxContainer.appendChild(label)); // Append unmatched next

    // Handle selected checkboxes
    const selectedCheckboxes = document.querySelectorAll('#regulationOptions input[type="checkbox"]:checked');
    selectedContainer.innerHTML = ''; // Clear the selected regulations container

    if (selectedCheckboxes.length > 0) {
        selectedCheckboxes.forEach(checkbox => {
            const regName = checkbox.value;
            const selectedLabel = document.createElement('div');
            selectedLabel.classList.add('selected-regulation-item');
            selectedLabel.innerHTML = `
                ${regName} 
                <button class="remove-btn" onclick="removeSelectedRegulation('${regName}')">X</button>
            `;
            selectedContainer.appendChild(selectedLabel);
        });
        selectedContainer.style.display = 'flex'; // Show the container
    } else {
        selectedContainer.style.display = 'none'; // Hide the container if none selected
    }

    // Update the count of selected regulations
    selectedCount.textContent = selectedCheckboxes.length;
}

// Function to remove a selected regulation when "X" is clicked
function removeSelectedRegulation(regName) {
    const checkboxes = document.querySelectorAll('#regulationOptions input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === regName) {
            checkbox.checked = false; // Uncheck the checkbox
        }
    });
    filterRegulation(); // Re-filter the regulations after removal
}

// Initialize the filter when the page loads
document.addEventListener('DOMContentLoaded', filterRegulation);






// 05--*************************************************************
function filterNotice() {
    const searchInput = document.getElementById('NoticeSearch').value.toLowerCase(); // Get search input value
    const checkboxes = document.querySelectorAll('#NoticeOptions .notice-label'); // Get all checkbox labels
    const checkboxContainer = document.getElementById('NoticeOptions'); // Parent container for checkboxes
    const selectedContainer = document.getElementById('selectedNotice'); // Container for selected notices
    const selectedCount = document.getElementById('selectedNoticeCount'); // Element for selected count

    // Separate matched and unmatched checkboxes
    const matched = [];
    const unmatched = [];
    checkboxes.forEach(label => {
        const text = label.textContent.trim().toLowerCase(); // Get checkbox text
        if (text.includes(searchInput)) {
            matched.push(label); // Add to matched list
        } else {
            unmatched.push(label); // Add to unmatched list
        }
    });

    // Reorder checkboxes: matched first, then unmatched
    checkboxContainer.innerHTML = ''; // Clear current checkboxes
    matched.forEach(label => checkboxContainer.appendChild(label)); // Append matched first
    unmatched.forEach(label => checkboxContainer.appendChild(label)); // Append unmatched next

    // Handle selected checkboxes
    const selectedCheckboxes = document.querySelectorAll('#NoticeOptions input[type="checkbox"]:checked');
    selectedContainer.innerHTML = ''; // Clear the selected notices container

    if (selectedCheckboxes.length > 0) {
        selectedCheckboxes.forEach(checkbox => {
            const noticeName = checkbox.value;
            const selectedLabel = document.createElement('div');
            selectedLabel.classList.add('selected-notice-item');
            selectedLabel.innerHTML = `
                ${noticeName} 
                <button class="remove-btn" onclick="removeSelectedNotice('${noticeName}')">X</button>
            `;
            selectedContainer.appendChild(selectedLabel);
        });
        selectedContainer.style.display = 'flex'; // Show the container
    } else {
        selectedContainer.style.display = 'none'; // Hide the container if none selected
    }

    // Update the count of selected notices
    selectedCount.textContent = selectedCheckboxes.length;
}

// Function to remove a selected notice when "X" is clicked
function removeSelectedNotice(noticeName) {
    const checkboxes = document.querySelectorAll('#NoticeOptions input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === noticeName) {
            checkbox.checked = false; // Uncheck the checkbox
        }
    });
    filterNotice(); // Re-filter the notices after removal
}

// Initialize the filter when the page loads
document.addEventListener('DOMContentLoaded', filterNotice);






// 06--*************************************************************
function filterPenalty() {
    const searchInput = document.getElementById('PenaltySearch').value.toLowerCase(); // Get search input value
    const checkboxes = document.querySelectorAll('#PenaltyOptions .penalty-label'); // Get all checkbox labels
    const checkboxContainer = document.getElementById('PenaltyOptions'); // Parent container for checkboxes
    const selectedContainer = document.getElementById('selectedPenalty'); // Container for selected penalties
    const selectedCount = document.getElementById('selectedPenaltyCount'); // Element for selected count

    // Separate matched and unmatched checkboxes
    const matched = [];
    const unmatched = [];
    checkboxes.forEach(label => {
        const text = label.textContent.trim().toLowerCase(); // Get checkbox text
        if (text.includes(searchInput)) {
            matched.push(label); // Add to matched list
        } else {
            unmatched.push(label); // Add to unmatched list
        }
    });

    // Reorder checkboxes: matched first, then unmatched
    checkboxContainer.innerHTML = ''; // Clear current checkboxes
    matched.forEach(label => checkboxContainer.appendChild(label)); // Append matched first
    unmatched.forEach(label => checkboxContainer.appendChild(label)); // Append unmatched next

    // Handle selected checkboxes
    const selectedCheckboxes = document.querySelectorAll('#PenaltyOptions input[type="checkbox"]:checked');
    selectedContainer.innerHTML = ''; // Clear the selected penalties container

    if (selectedCheckboxes.length > 0) {
        selectedCheckboxes.forEach(checkbox => {
            const penaltyName = checkbox.value;
            const selectedLabel = document.createElement('div');
            selectedLabel.classList.add('selected-penalty-item');
            selectedLabel.innerHTML = `
                ${penaltyName} 
                <button class="remove-btn" onclick="removeSelectedPenalty('${penaltyName}')">X</button>
            `;
            selectedContainer.appendChild(selectedLabel);
        });
        selectedContainer.style.display = 'flex'; // Show the container
    } else {
        selectedContainer.style.display = 'none'; // Hide the container if none selected
    }

    // Update the count of selected penalties
    selectedCount.textContent = selectedCheckboxes.length;
}

// Function to remove a selected penalty when "X" is clicked
function removeSelectedPenalty(penaltyName) {
    const checkboxes = document.querySelectorAll('#PenaltyOptions input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === penaltyName) {
            checkbox.checked = false; // Uncheck the checkbox
        }
    });
    filterPenalty(); // Re-filter the penalties after removal
}

// Initialize the filter when the page loads
document.addEventListener('DOMContentLoaded', filterPenalty);





// 07--*************************************************************
function filterCompany() {
    const searchInput = document.getElementById('companySearch').value.toLowerCase(); // Get search input value
    const checkboxes = document.querySelectorAll('#companyOptions .company-label'); // Get all checkbox labels
    const checkboxContainer = document.getElementById('companyOptions'); // Parent container for checkboxes
    const selectedContainer = document.getElementById('selectedCompany'); // Container for selected companies
    const selectedCount = document.getElementById('selectedCompanyCount'); // Element for selected count

    // Separate matched and unmatched checkboxes
    const matched = [];
    const unmatched = [];
    checkboxes.forEach(label => {
        const text = label.textContent.trim().toLowerCase(); // Get checkbox text
        if (text.includes(searchInput)) {
            matched.push(label); // Add to matched list
        } else {
            unmatched.push(label); // Add to unmatched list
        }
    });

    // Reorder checkboxes: matched first, then unmatched
    checkboxContainer.innerHTML = ''; // Clear current checkboxes
    matched.forEach(label => checkboxContainer.appendChild(label)); // Append matched first
    unmatched.forEach(label => checkboxContainer.appendChild(label)); // Append unmatched next

    // Handle selected checkboxes
    const selectedCheckboxes = document.querySelectorAll('#companyOptions input[type="checkbox"]:checked');
    selectedContainer.innerHTML = ''; // Clear the selected companies container

    if (selectedCheckboxes.length > 0) {
        selectedCheckboxes.forEach(checkbox => {
            const companyName = checkbox.value;
            const selectedLabel = document.createElement('div');
            selectedLabel.classList.add('selected-company-item');
            selectedLabel.innerHTML = `
                ${companyName} 
                <button class="remove-btn" onclick="removeSelectedCompany('${companyName}')">X</button>
            `;
            selectedContainer.appendChild(selectedLabel);
        });
        selectedContainer.style.display = 'flex'; // Show the container
    } else {
        selectedContainer.style.display = 'none'; // Hide the container if none selected
    }

    // Update the count of selected companies
    selectedCount.textContent = selectedCheckboxes.length;
}

// Function to remove a selected company when "X" is clicked
function removeSelectedCompany(companyName) {
    const checkboxes = document.querySelectorAll('#companyOptions input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === companyName) {
            checkbox.checked = false; // Uncheck the checkbox
        }
    });
    filterCompany(); // Re-filter the companies after removal
}

// Initialize the filter when the page loads
document.addEventListener('DOMContentLoaded', filterCompany);



function filterCaseNumber() {
    const searchInput = document.getElementById('caseSearch').value.toLowerCase();
    const checkboxes = document.querySelectorAll('#caseOptions .case-label');
    const checkboxContainer = document.getElementById('caseOptions');
    const selectedContainer = document.getElementById('selectedCase');
    const selectedCount = document.getElementById('selectedcaseCount1');

    const matched = [];
    const unmatched = [];

    checkboxes.forEach(label => {
        const text = label.textContent.trim().toLowerCase();
        if (text.includes(searchInput)) {
            matched.push(label);
        } else {
            unmatched.push(label);
        }
    });

    checkboxContainer.innerHTML = '';
    matched.forEach(label => checkboxContainer.appendChild(label));
    unmatched.forEach(label => checkboxContainer.appendChild(label));

    updateSelectedCases();
}

function updateSelectedCases() {
    const selectedContainer = document.getElementById('selectedCase');
    const selectedCount = document.getElementById('selectedcaseCount1');
    const selectedCheckboxes = document.querySelectorAll('#caseOptions input[type="checkbox"]:checked');

    selectedContainer.innerHTML = '';

    if (selectedCheckboxes.length > 0) {
        selectedCheckboxes.forEach(checkbox => {
            const companyName = checkbox.value;
            const encodedCompanyName = encodeURIComponent(companyName);

            const selectedLabel = document.createElement('div');
            selectedLabel.classList.add('selected-cases');
            selectedLabel.innerHTML = `
                ${companyName} 
                <button type="button" class="remove-btn" data-company="${encodedCompanyName}">X</button>
            `;
            selectedContainer.appendChild(selectedLabel);
        });
        selectedContainer.style.display = 'flex';
    } else {
        selectedContainer.style.display = 'none';
    }

    selectedCount.textContent = selectedCheckboxes.length;
}

// Function to remove a selected case when "X" is clicked
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('remove-btn')) {
        event.preventDefault();  // Prevent form submission
        event.stopPropagation(); // Stop event bubbling

        const encodedCompanyName = event.target.getAttribute('data-company');
        const companyName = decodeURIComponent(encodedCompanyName);
        
        const checkboxes = document.querySelectorAll('#caseOptions input[type="checkbox"]');

        checkboxes.forEach(checkbox => {
            if (checkbox.value === companyName) {
                checkbox.checked = false;
            }
        });

        updateSelectedCases();
    }
});

// Initialize filtering when the page loads
document.addEventListener('DOMContentLoaded', filterCaseNumber);



function filterJuri() {
    const searchInput = document.getElementById('juriSearch').value.toLowerCase(); // Get search input value
    const checkboxes = document.querySelectorAll('#juriOptions .juri-label'); // Get all checkbox labels
    const checkboxContainer = document.getElementById('juriOptions'); // Parent container for checkboxes
    const selectedContainer = document.getElementById('selectedjuri'); // Container for selected companies
    const selectedCount = document.getElementById('selectedjuriCount'); // Element for selected count


    // Separate matched and unmatched checkboxes
    const matched = [];
    const unmatched = [];
    checkboxes.forEach(label => {
        const text = label.textContent.trim().toLowerCase(); // Get checkbox text
        if (text.includes(searchInput)) {
            matched.push(label); // Add to matched list
        } else {
            unmatched.push(label); // Add to unmatched list
        }
    });

    // Reorder checkboxes: matched first, then unmatched
    checkboxContainer.innerHTML = ''; // Clear current checkboxes
    matched.forEach(label => checkboxContainer.appendChild(label)); // Append matched first
    unmatched.forEach(label => checkboxContainer.appendChild(label)); // Append unmatched next

    // Handle selected checkboxes
    const selectedCheckboxes = document.querySelectorAll('#juriOptions input[type="checkbox"]:checked');
    selectedContainer.innerHTML = ''; // Clear the selected companies container

    if (selectedCheckboxes.length > 0) {
        selectedCheckboxes.forEach(checkbox => {
            const companyName = checkbox.value;
            const selectedLabel = document.createElement('div');
            selectedLabel.classList.add('selected-juris');
            selectedLabel.innerHTML = `
                ${companyName} 
                <button class="remove-btn" onclick="removeSelectedCompany('${companyName}')">X</button>
            `;
            selectedContainer.appendChild(selectedLabel);
        });
        selectedContainer.style.display = 'flex'; // Show the container
    } else {
        selectedContainer.style.display = 'none'; // Hide the container if none selected
    }

    // Update the count of selected companies
    selectedCount.textContent = selectedCheckboxes.length;
}

// Function to remove a selected company when "X" is clicked
function removeSelectedCompany(companyName) {
    const checkboxes = document.querySelectorAll('#juriOptions input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === companyName) {
            checkbox.checked = false; // Uncheck the checkbox
        }
    });
    filterJuri(); // Re-filter the companies after removal
}


// Initialize the filter when the page loads
document.addEventListener('DOMContentLoaded', filterJuri);





f// HTML structure assumed:
// <input type="text" id="newsFetch" placeholder="Search news...">
// <div id="newsOptions"> (contains all .filterable-card elements)

function fetchNews() {
    const searchInput = document.getElementById('newsFetch').value.toLowerCase(); // Get the search input value
    const cards = document.querySelectorAll('.filterable-card'); // Select all cards

    cards.forEach(card => {
        const title = card.getAttribute('data-title').toLowerCase();
        const country = card.getAttribute('data-country').toLowerCase();
        const regulatory = card.getAttribute('data-regulatory').toLowerCase();

        // Check if the search input matches any of the attributes
        if (title.includes(searchInput) || country.includes(searchInput) || regulatory.includes(searchInput)) {
            card.style.display = 'block'; // Show the card if it matches
        } else {
            card.style.display = 'none'; // Hide the card if it doesn't match
        }
    });
}

// Event listener for real-time search
const searchInput = document.getElementById('newsFetch');
searchInput.addEventListener('input', fetchNews);




