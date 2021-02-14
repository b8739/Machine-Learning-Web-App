<template>
  <div class="container">
    <div class="innerContainer">
      <div class="mainContents">
        <h1>Data Table</h1>
        <hr><br><br>
        <button type="button" class="" v-b-modal.add-modal>Add Data</button>
        <br><br>
        <!-- table -->
        <table class="dataTable">
          <!-- table head -->
          <thead>
            <tr>
              <th>Index</th>
              <th v-for="(headerValue, index) in header" :key="index" scope="">{{ header[index]}}</th>
              <th>Edit</th>
            </tr>
          </thead>
          <!-- table body -->
          <tbody>
            <tr v-for="(dataValue, trIndex) in newDataset[header[0]]" :key="trIndex"> <!-- make row: csv파일의 1번째 열의 개수만큼 행을 만듦-->
              <td>{{ trIndex }}</td> <!-- 0부터 시작하도록 수정해야 함-->
              <td v-for="(dataValue, tdIndex) in newDataset" :key="tdIndex"> {{ newDataset [ tdIndex ] [ trIndex ] }} </td> <!-- make column: index는 0부터 5번이 맞고, 뒤에꺼는 엄청 많은 param-->
                  <div class="" role="group">
                  <!-- update -->
                    <button
                      type="button"
                      class="" 
                      @click="editData()"> Update
                    </button>
                    <!-- delete -->
                    <button
                      type="button"
                      class=""
                      @click="onDeleteData()">Delete
                    </button>
                </div>
            </tr>
          </tbody> 
        </table>
      </div>
    <!-- add modal -->
    <b-modal ref="addDataModal"
             id="add-modal"
             title="Add a new data"
             hide-footer>
      <!-- add form -->
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <!-- add form group -->
        <b-form-group id="form-title-group"
                      label-for="form-title-input"
                      v-for="(headerValue, index) in header" :key="index">
                      <label for=''>{{ header[index] }}</label>
            <b-form-input id="form-title-input"
                          type="text"
                          v-model="addForm[header[index]]"
                          required
                          placeholder="Enter the Value">
            </b-form-input>
        </b-form-group>
        <!-- modal buttons -->
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    </div>
   </div>
</template>

<script>
//import 방식 참고
import axios from 'axios';
// import Alert from './Alert.vue';

export default {
    name: 'Datatable',
    props: ['dataset'],

    data() {
    return {
      header: [], //전달받은 df의 맨 상단 column
      addForm: {},//ex. sepal-width:' ' , sepal-length: ' ' ...
      newDataset:{}
    };
  },
    
  components: {
    //components 추가
  },
  methods: {
    preLoadData(){
      this.newDataset = this.dataset;
      // console.log(this.$route.params.dataset);
      let columnValues = Object.keys(this.newDataset); //route로 전달받은 params의 dataset의 key 값 (ex.sepal_width...)를 columnValue에 삽입
      this.saveResponseData(columnValues); //for문들 돌면서 data에 정의된 this.header에 차곡차곡 들어감
      // console.log(this.dataSet);
      
    },

    loadData(){
      const path = 'http://localhost:5000/loadData';
      axios.get(path)
        .then((res) => {
          this.newDataset = res.data;
          console.log(res);
          console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    saveResponseData (columnValues) {
      for (const columnValue of columnValues) {  
        this.header.push(columnValue); //add했을 때 다시 loaddata되는데 push 때문에 중복된는 문제 해결 필요
        this.addForm[columnValue]= "";
      }
    },

    // 변형시켜야 하는 메소드들
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addDataModal.hide();
      this.initForm();
    },

    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addDataModal.hide();                                     
      this.addData(this.addForm);
      this.initForm();
      // this.header = []; //header일단 여기서 초기화 (임시, 나중에 함수화할것임)
    },

    addData(payload) {
      const path = 'http://localhost:5000/addData';
      axios.post(path, payload)
        .then(() => {
          this.loadData();
          this.message = 'Data added!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
          this.loadData();
        });
    },

    initForm() {
      this.addForm = {};
      },
    },
  
  created() {
    console.log("Datatable created");
    this.preLoadData();
    console.log(this.newDataset);
  },
  beforeUpdate(){
    console.log("Datatable beforecreate");
  },
  updated() {
    console.log("Datatable updated");
  },
  mounted() {
    console.log("Datatable mounted");
  },


}
</script>









<style>
  .dataTable{
    margin: 0 auto;
  }
  .dataTable tr:nth-child(odd) {
    background-color: #D9E1F2;
    }
  .dataTable tr:nth-child(even) {
    background-color: #f0f8ff;
    }
  th{
    width: 115px;
  }
  .dataTable tr:hover {
    background-color: #8ab6ca;
    cursor: pointer;
}

</style>