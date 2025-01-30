// Custom time JS dropdown...
const generateTimeOptions = () => {
    const timeOptions = [];
    for (let hour = 0; hour < 24; hour++) {
        for (let minute = 0; minute < 60; minute += 5) {
            const formattedHour = hour.toString().padStart(2, '0');
            const formattedMinute = minute.toString().padStart(2, '0');
            timeOptions.push(`${formattedHour}:${formattedMinute}`);
        }
    }
    return timeOptions;
};

const populateTimeDropdowns = (dropdownIds) => {
    const timeOptions = generateTimeOptions();
    dropdownIds.forEach(id => {
        const dropdown = document.getElementById(id);
        timeOptions.forEach(time => {
            dropdown.append(new Option(time, time));
        });
    });
};
