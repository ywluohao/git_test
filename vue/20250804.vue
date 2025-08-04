<div class="d-flex flex-wrap">
  <b-list-group-item
    v-for="field in column.iaap"
    :key="field"
    class="w-50 d-flex justify-content-between"
  >
    <strong>{{ field }}</strong>
    <span>{{ df.iaap[0][field] }}</span>
  </b-list-group-item>
</div>