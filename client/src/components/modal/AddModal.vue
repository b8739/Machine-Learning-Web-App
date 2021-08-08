<template>
  <div>
    <b-modal ref="addDataModal" id="add-modal" title="Add a new data" hide-footer>
      <!-- add form -->
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <!-- add form group -->
        <b-form-group
          id="form-title-group"
          label-for="form-title-input"
          v-for="(columnsValue, index) in columnsWithoutIndex"
          :key="index"
        >
          <label for="">{{ columnsWithoutIndex[index] }}</label>
          <b-form-input
            id="form-title-input"
            type="text"
            v-model="addForm[columnsWithoutIndex[index]]"
            required
            placeholder="Enter the Value"
          >
          </b-form-input>
        </b-form-group>
        <!-- modal buttons -->
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>
<!-- add modal -->
<script>
import axios from "axios";
export default {
  data() {
    return {
      loadDataStatus: true
    };
  },
  props: ["addForm", "columnsWithoutIndex", "indexNum"],
  methods: {
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addDataModal.hide();
      this.initForm();
    },

    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addDataModal.hide();
      this.addForm["ID"] = this.nextIndexNum; //add할 위치 (맨 밑 row)
      console.log(this.addForm["ID"]);
      this.addData(this.addForm);
      // this.initForm();
      // this.columns = []; //columns 여기서 초기화 (임시, 나중에 함수화할것임)
    },

    addData(payload) {
      const path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/addData";
      axios
        .post(path, payload)
        .then(() => {
          this.$emit("loadDataStatus", this.loadDataStatus);
          this.message = "Data added!";
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.loadData();
        });
    }
  },
  computed: {
    nextIndexNum() {
      return this.indexNum + 1;
    }
  }
};
</script>
