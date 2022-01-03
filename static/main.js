// Handle form submit 
function handleFormSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    const formJSON = Object.fromEntries(data.entries());

    // for multi-selects, we need special handling
    formJSON.insurance = data.getAll('insurance');

    // Create tracking reference
    trackingReference = Math.floor(Math.random() * 1000000000)
    console.log('Tracking Reference', trackingReference)
        
    // Add tracking reference to JSON
    formJSON.tracking_reference = trackingReference
    console.log('formJSON', formJSON.tracking_reference)

    // Print the JSON which may be sent
    //   const results = document.querySelector('.results pre');
    //   results.innerText = JSON.stringify(formJSON, null, 2);

    //////////////
    //Validation//
    //////////////

    // Note: validation also takes places on backend

    // Get package value and insurance status
    const package_value = data.getAll('package_value')[0];
    const insurance_status = data.getAll('insurance')[0]

    // Get despatch date 
    const despatch_date = data.getAll('despatch_date')[0]

    // Get today's and tomorrow's date - formatted with '-' separating the numbers and double digits for month and day (to match Python format) 
    const today = new Date()
    // const formatted_today = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate(); // Without double digits
    const formatted_today = today.getFullYear()  + '-'
                         + ('0' + (today.getMonth()+1)).slice(-2) + '-'
                         + ('0' + today.getDate()).slice(-2) 
    console.log('todays date',formatted_today)
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    // const formatted_tomorrow = tomorrow.getFullYear()+'-'+(tomorrow.getMonth()+1)+'-'+tomorrow.getDate(); // Without double digits
    const formatted_tomorrow = tomorrow.getFullYear()  + '-'
                            + ('0' + (tomorrow.getMonth()+1)).slice(-2) + '-'
                            + ('0' + tomorrow.getDate()).slice(-2) 
    console.log('tomorrows date',formatted_tomorrow)

    // Validate that package: 
    //  1. Is eligible for insurance (check that the value is not too high)
    //  2. That the despatch date is today or tomorrow
    if (package_value > 10000 && insurance_status == 'y') {
        // Place error message in fail div
        console.log('Entered too high value condition')
        const fail = document.querySelector('.fail pre');
        fail.innerText = ' Package value too high. Packages worth more than £10,000 are not eligible for insurance.'
        //Show fail div
        document.getElementById("fail").hidden=false
    } else if (!(despatch_date == formatted_today || despatch_date == formatted_tomorrow) ) {
        // Place error message in fail div
        console.log('Entered invalid date condition')
        console.log(despatch_date)
        const fail = document.querySelector('.fail pre');
        fail.innerText = ' Despatch date must be today or tomorrow.'
        //Show fail message
        document.getElementById("success").hidden=true
        document.getElementById("fail").hidden=false
    } else {
        // Show success message and order reference
        console.log('Entered Success condition')
        const success = document.querySelector('.success pre');
        success.innerText = trackingReference
        document.getElementById("fail").hidden=true
        document.getElementById("success").hidden=false
    }

    // Validate that the package value field is a valid number 
    if (isNaN(package_value)) {
        console.log('Entered invalid package_value type condition - NAN')
        const fail = document.querySelector('.fail pre');
        fail.innerText = ' Package value must be a number.'
        document.getElementById("success").hidden=true
        document.getElementById("fail").hidden=false
    } else if (package_value < 0.01) {
        console.log('Entered invalid package_value type condition - Negative number')
        const fail = document.querySelector('.fail pre');
        fail.innerText = ' Package value must be a positive number.'
        document.getElementById("success").hidden=true
        document.getElementById("fail").hidden=false
    }

    // Collect form data as JSON
    const json = JSON.stringify(formJSON, null, 2);
    // Send form data to API
    var url = "http://127.0.0.1:5000/orders";
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", url, true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.send(json);
}

// Hide success and fail divs 
document.getElementById("success").hidden=true;
document.getElementById("fail").hidden=true;
const form = document.querySelector('.form');
form.addEventListener('submit', handleFormSubmit);