async function fetchData() {
    const requests = [];
    for (let i = 0; i < 100; i++) {
        requests.push(fetch(`/api/data?page=${i}`)); // Adjust the endpoint as needed
    }
    
    try {
        const responses = await Promise.all(requests);
        const data = await Promise.all(responses.map(response => response.json()));
        // Process your data here
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
