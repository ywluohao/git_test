<template>
  <div>
    <button @click="startFileGeneration">Generate Excel File</button>
  </div>
</template>

<script>
export default {
  methods: {
    startFileGeneration() {
      fetch(`/start-file-generation/?param1=${this.param1}&param2=${this.param2}&param3=${this.param3}&param4=${this.param4}`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          const jobId = data.job_id;
          this.checkFileStatus(jobId);
        })
        .catch(error => {
          console.error('Error starting file generation:', error);
        });
    },
    checkFileStatus(jobId) {
      fetch(`/check-file-status/${jobId}/`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.blob();
        })
        .then(blob => {
          if (blob.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${jobId}.xlsx`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          } else {
            setTimeout(() => this.checkFileStatus(jobId), 10000);  // Poll every 10 seconds
          }
        })
        .catch(error => {
          console.error('Error checking file status:', error);
        });
    }
  }
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>