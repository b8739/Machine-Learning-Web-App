<template>
  <div>
    <b-modal ref="addDataModal" id="add-modal" title="Add a new data" hide-footer>
      <!-- add form -->
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <!-- add form group -->
        <b-form-group
          id="form-title-group"
          label-for="form-title-input"
          v-for="(headerValue, index) in headerWithoutIndex"
          :key="index"
        >
          <label for="">{{ headerWithoutIndex[index] }}</label>
          <b-form-input
            id="form-title-input"
            type="text"
            v-model="addForm[headerWithoutIndex[index]]"
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
  props: ["addForm", "header", "indexNum"],
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
      // this.header = []; //header일단 여기서 초기화 (임시, 나중에 함수화할것임)
    },

    addData(payload) {
      const path = "http://localhost:5000/addData";
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
    headerWithoutIndex() {
      const idIndex = this.header.indexOf("ID");
      let tempHeader;
      if (idIndex != -1) {
        //처음엔 -1이라서 에러를 발생시킴, 때문에 if문으로 해당 경우의 수를 제거
        tempHeader = this.header.slice(); //copy by value
        tempHeader.splice(idIndex, 1);
      }
      return tempHeader;
    },
    nextIndexNum() {
      return this.indexNum + 1;
    }
  }
};
</script>
