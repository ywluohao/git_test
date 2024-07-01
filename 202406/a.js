<script>
export default {
    data() {
        return {
            maxRetries: 60,  // 10 minutes with a 10-second interval
            retryInterval: 10000,  // 10 seconds
            retryCount: 0,
        };
    },
    methods: {
        async downloadExcel() {
            try {
                const response = await fetch('/download-excel/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.status === 404) {
                    this.handleRetry();
                } else if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'data.xlsx';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                } else {
                    console.error('Failed to fetch the Excel file.');
                }
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
                this.handleRetry();
            }
        },
        handleRetry() {
            if (this.retryCount < this.maxRetries) {
                this.retryCount += 1;
                setTimeout(this.downloadExcel, this.retryInterval);
            } else {
                console.error('Max retries reached. The Excel file is not available.');
            }
        },
    },
};
</script>