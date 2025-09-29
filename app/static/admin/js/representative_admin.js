document.addEventListener('DOMContentLoaded', function() {
    function toggleConstituencyFields() {
        const houseField = document.querySelector('#id_house');
        const proportionalField = document.querySelector('.field-proportional');
        const proportionalInput = document.querySelector('#id_proportional');
        const horField = document.querySelector('.field-hor_constituency');
        const provinceField = document.querySelector('.field-province_constituency');
        const orderField = document.querySelector('.field-order');
        const municipalityField = document.querySelector('.field-municipality');
        const localPositionInput = document.querySelector('#id_local_position');
        const localPositionField = document.querySelector('.field-local_position');
        const wardField = document.querySelector('.field-ward');
        const wardInput = document.querySelector('#id_ward');
        const districtField = document.querySelector('.field-district');

        const hor_input = document.querySelector('#id_hor_constituency');
        const province_input = document.querySelector('#id_province_constituency');
        const district_input = document.querySelector('#id_district');
        const municipality_input = document.querySelector('#id_municipality');

        if (!houseField || !proportionalField || !horField || !provinceField || !districtField || !orderField || !municipalityField || !localPositionField || !wardField) return;

        function updateVisibility() {
            const houseValue = houseField.value;
            const isProportional = proportionalInput.checked;
            const localPositionValue = localPositionInput.value;
            
            // If proportional is checked, hide both
            if (isProportional) {
                horField.style.display = 'none';
                provinceField.style.display = 'none';
                municipalityField.style.display = 'none';
                districtField.style.display = 'none';
                wardField.style.display = 'none';
                orderField.style.display = 'block';
                localPositionField.style.display = 'none';
            } else {
                orderField.style.display = 'none';
                // Show/hide based on house selection
                if(houseValue === 'NATIONAL_ASSEMBLY') {
                    horField.style.display = 'none';
                    proportionalInput.checked = false;
                    proportionalField.style.display = 'none';
                    proportionalInput.disabled = true;
                    provinceField.style.display = 'none';
                    municipalityField.style.display = 'none';
                    districtField.style.display = 'none';
                    wardField.style.display = 'none';
                    localPositionField.style.display = 'none';

                    wardInput.value = '';
                    localPositionInput.value = '';                    
                    hor_input.value = '';
                    province_input.value = '';
                    district_input.value = '';
                    municipality_input.value = '';
                } else if (houseValue === 'HOUSE_OF_REPRESENTATIVES') {
                    horField.style.display = 'block';
                    provinceField.style.display = 'none';
                    districtField.style.display = 'none';
                    municipalityField.style.display = 'none';
                    wardField.style.display = 'none';
                    localPositionField.style.display = 'none';
                    proportionalField.style.display = 'block';

                    wardInput.value = '';
                    localPositionInput.value = '';                    
                    province_input.value = '';
                    district_input.value = '';
                    municipality_input.value = '';
                } else if (houseValue === 'PROVINCE_ASSEMBLY') {
                    horField.style.display = 'none';
                    provinceField.style.display = 'block';
                    municipalityField.style.display = 'none';
                    districtField.style.display = 'none';
                    wardField.style.display = 'none';
                    localPositionField.style.display = 'none';
                    proportionalField.style.display = 'block';

                    wardInput.value = '';
                    localPositionInput.value = '';
                    hor_input.value = '';
                    district_input.value = '';
                    municipality_input.value = '';
                } else if (houseValue === 'LOCAL_LEVEL') {
                    horField.style.display = 'none';
                    provinceField.style.display = 'none';
                    proportionalInput.checked = false;
                    proportionalField.style.display = 'none';
                    proportionalInput.disabled = true;
                    municipalityField.style.display = 'block';
                    districtField.style.display = 'block';
                    localPositionField.style.display = 'block';
                    wardField.style.display = 'block';
                    
                    hor_input.value = '';
                    province_input.value = '';

                    // Show/hide ward field based on local position
                    if (localPositionValue === 'MAYOR' || localPositionValue === 'DEPUTY_MAYOR') {
                        districtField.style.display = 'block';
                        wardField.style.display = 'none';
                        municipalityField.style.display = 'none';

                        municipality_input.value = '';
                    } else {
                        districtField.style.display = 'none';
                        municipalityField.style.display = 'block';
                        wardField.style.display = 'block';

                        district_input.value = '';
                    }
                } else {
                    // Default case - show all
                    horField.style.display = 'block';
                    provinceField.style.display = 'block';
                    municipalityField.style.display = 'block';
                    districtField.style.display = 'block';
                    localPositionField.style.display = 'block';
                    wardField.style.display = 'block';
                    proportionalField.style.display = 'block';
                }
            }
        }
        
        // Initial update
        updateVisibility();
        
        // Add event listeners
        houseField.addEventListener('change', updateVisibility);
        proportionalField.addEventListener('change', updateVisibility);
        localPositionField.addEventListener('change', updateVisibility);
    }
    
    toggleConstituencyFields();
});