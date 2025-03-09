(function() {
    const container = document.createElement("div");
    container.innerHTML = `
        
        <form id="appointment-form">
            <label for="name">Name:</label>
            <input type="text" id="name" required>

            <label for="phone">Phone Number:</label>
            <input type="tel" id="phone" required>

            <label for="date">Date:</label>
            <input type="date" id="date" required>

            <label for="time-slot">Time Slot:</label>
            <select id="time-slot" required></select>

            <button type="submit">Book Appointment</button>
        </form>
        <div id="message"></div>
    `;

    document.body.appendChild(container);

    const timeSlotSelect = document.getElementById("time-slot");

    // Fetching
    fetch('http://127.0.0.1:5000/api/slots')
        .then(response => response.json())
        .then(data => {
            data.forEach(slot => {
                const option = document.createElement("option");
                option.value = slot;
                option.textContent = slot;
                timeSlotSelect.appendChild(option);
            });
        });

    const form = document.getElementById("appointment-form");
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const phone = document.getElementById("phone").value;
        const date = document.getElementById("date").value;
        const timeSlot = document.getElementById("time-slot").value;

        const appointmentData = {
            name: name,
            phone: phone,
            date: date,
            time_slot: timeSlot
        };

        fetch('http://127.0.0.1:5000/api/book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(appointmentData)
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById("message");
            if (data.message) {
                messageElement.style.color = 'green';
                messageElement.textContent = data.message;
            } else if (data.error) {
                messageElement.style.color = 'red';
                messageElement.textContent = data.error;
            }
        });
    });
})();
