<template>
  <div>
    <b-form-input
      type="text"
      ref="input"
      v-model="displayValue"
      @input="onInput"
      placeholder="Enter an integer"
    />
    <p>Raw Value: {{ rawValue }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      displayValue: '',
      rawValue: ''
    };
  },
  methods: {
    onInput(event) {
      const input = event.target;
      const cursor = input.selectionStart;

      // Just remove commas, no validation
      const digitsOnly = input.value.replace(/,/g, '');
      this.rawValue = digitsOnly;

      // Format it
      const formatted = Number(digitsOnly).toLocaleString();
      const diff = formatted.length - input.value.length;

      this.displayValue = formatted;

      // Restore cursor
      this.$nextTick(() => {
        const newCursor = cursor + diff;
        this.$refs.input.setSelectionRange(newCursor, newCursor);
      });
    }
  }
};
</script>