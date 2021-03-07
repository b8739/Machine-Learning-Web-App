<template>
  <div>
    <!-- update modal -->
    <b-modal ref="updateDataModal"
          id="update-modal"
          title="Update existing data"
          hide-footer>
  <!-- update form -->
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
    <!-- update form group -->
    <b-form-group id="form-title-update-group"
                  label-for="form-title-update-input"
                  v-for="(headerValue, index) in headerWithoutIndex" :key="index">
                  <label for=''>{{ headerWithoutIndex[index] }}</label>
        <b-form-input id="form-title-update-input"
                      type="text"
                      v-model="updateForm[headerWithoutIndex[index]]"
                      required
                      placeholder="Enter the Value">
        </b-form-input>
    </b-form-group>
    <!-- modal buttons -->
    <b-button type="submit" variant="primary">Update</b-button>
    <b-button type="reset" variant="danger">Cancel</b-button>
  </b-form>
</b-modal>
  </div>
</template>
