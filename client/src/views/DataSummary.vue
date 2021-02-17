<template>
  <div>
    <div class="sidebar">
      <div class="editData">
        <button type="button" v-b-modal.add-modal>Add Data</button>
        <button type="button" @click="visibilityToggle()">Update Data</button>
      </div>
    </div>
    <Datatable :header="header" :dataSet="dataSet" :indexNum="indexNum" :hadLoaded="hadLoaded" />
    <AddModal :header="header" :addForm="addForm" />
  </div>
</template>
<script>
import axios from "axios";
import Datatable from "../components/Datatable";
import Sidebar from "../components/Sidebar";
import AddModal from "../components/AddModal";

export default {
  data() {
    return {
      header: [],
      dataSet: {},
      indexNum: "",
      addForm: {}, //ex. sepal-width:' ' , sepal-length: ' ' ...
      updateForm: {},
      hadLoaded: false
    };
  },
  components: {
    Datatable,
    Sidebar,
    AddModal
  },
  methods: {
    loadData() {
      const path = "http://localhost:5000/loadData";
      axios
        .get(path)
        .then(res => {
          console.log(res.data);
          this.dataSet = res.data;
          // 데이터 추가 시 필요한 index number
          this.indexNum = Object.keys(this.dataSet["ID"]).length - 1; //149
          //'처음' 데이터를 받아올때만 Header를 받아오도록 처리
          if (this.hadLoaded == false) this.saveResponseData();
        })
        .catch(error => {
          console.error(error);
        });
    },
    saveResponseData() {
      let columnValues = Object.keys(this.dataSet);
      for (const columnValue of columnValues) {
        this.header.push(columnValue); //add했을 때 다시 loaddata되는데 push 때문에 중복된는 문제 해결 필요
        this.updateForm[columnValue] = "";
        this.addForm[columnValue] = "";
      }
    },

    // 변형시켜야 하는 메소드들

    getIndexForUpdate(targetIndex) {
      console.log(`targetIndex: ${targetIndex}`);
      this.updateForm["ID"] = targetIndex;
    },
    // for update
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.updateDataModal.hide();
      this.updateData(this.updateForm);

      // this.updateBook(payload, this.updateForm);
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.updateDataModal.hide();
      this.initForm();
      this.loadData(); // why?
    },
    updateData(payload) {
      console.log(payload);
      const path = `http://localhost:5000/updateData`;
      axios
        .put(path, payload)
        .then(() => {
          this.loadData();
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.loadData();
        });
    },
    initForm() {
      this.addForm = {};
    }
  },
  created() {
    this.loadData();
    console.log("created");
  },
  mounted() {
    console.log("mounted");
  },
  beforeUpdate() {
    console.log("beforecreate");
  },
  updated() {
    console.log("updated");
    this.hadLoaded = true;
  }
};
</script>
