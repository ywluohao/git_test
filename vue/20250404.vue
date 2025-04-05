<template>
  <div>
    <b-form-input
      type="text"
      v-model="displayValue"
      @input="formatInput"
      placeholder="Enter an integer"
    />
    <p>Raw Value: {{ rawValue }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rawValue: '',       // e.g. 1234567
      displayValue: ''    // e.g. "1,234,567"
    };
  },
  methods: {
    formatInput(event) {
      const input = event.target;
      const digitsOnly = input.value.replace(/\D/g, ''); // Strip non-digits

      this.rawValue = digitsOnly;

      // Format with commas
      const formatted = Number(digitsOnly).toLocaleString();
      this.displayValue = digitsOnly ? formatted : '';

      // Adjust cursor to end (optional: for more advanced cursor keeping, more logic needed)
      this.$nextTick(() => {
        const len = this.displayValue.length;
        input.setSelectionRange(len, len);
      });
    }
  }
};
</script>