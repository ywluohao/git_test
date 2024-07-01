<template>
    <div>
        <button @click="startExcelGeneration">Generate Excel</button>
        <p v-if="statusMessage">{{ statusMessage }}</p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            taskId: null,
            statusMessage: '',
            maxRetries: 60,  // 10 minutes with a 10-second interval
            retryInterval: 10000,  // 10 seconds
            retryCount: 0,
        };
    },
    methods: {
        async startExcelGeneration() {
            try {
                const response = await fetch('/start-excel-generation/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        param1: 'value1',
                        param2: 'value2',
                        param3: 'value3',
                        param4: 'value4',
                    }),
                });

                if (response.ok) {
                    const data = await response.json();
                    this.taskId = data.task_id;
                    this.checkExcelStatus();
                } else {
                    this.statusMessage = 'Failed to start Excel generation.';
                }
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
                this.statusMessage = 'Failed to start Excel generation.';
            }
        },
        async checkExcelStatus() {
            if (!this.taskId) return;

            try {
                const response = await fetch(`/check-excel-status/?task_id=${this.taskId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const data = await response.json();

                    if (data.status === 'success') {
                        this.downloadExcel(data.file_path);
                    } else if (data.status === 'processing') {
                        this.handleRetry();
                    } else {
                        this.statusMessage = 'Failed to generate Excel file.';
                    }
                } else {
                    this.handleRetry();
                }
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
                this.handleRetry();
            }
        },
        handleRetry() {
            if (this.retryCount < this.maxRetries) {
                this.retryCount += 1;
                setTimeout(this.checkExcelStatus, this.retryInterval);
            } else {
                this.statusMessage = 'Max retries reached. The Excel file is not available.';
            }
        },
        async downloadExcel(filePath) {
            try {
                const response = await fetch(`/download-excel/?file_path=${filePath}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'data.xlsx';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    this.statusMessage = 'Excel file downloaded successfully.';
                } else {
                    this.statusMessage = 'Failed to download Excel file.';
                }
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
                this.statusMessage = 'Failed to download Excel file.';
            }
        },
    },
};
</script>