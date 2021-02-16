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
              <!-- <th>Index</th> -->
              <th v-for="(headerValue, index) in header" :key="index" scope="">{{ header[index]}}</th>
              <th>Edit</th>
            </tr>
          </thead>
          <!-- table body -->
          <tbody>
            <tr v-for="(dataValue, trIndex) in newDataset[header[0]]" :key="trIndex"> <!-- make row: csv파일의 1번째 열의 개수만큼 행을 만듦-->
              <!-- <td>{{ trIndex }}</td> -->
              <td v-for="(dataValue, tdIndex) in newDataset" :key="tdIndex"> {{ newDataset [ tdIndex ] [ trIndex ] }} </td> <!-- make column: index는 0부터 5번이 맞고, 뒤에꺼는 엄청 많은 param-->
                  <div class="" role="group">
                  <!-- update -->
                    <button
                      type="button"
                      class="" v-b-modal.update-modal
                      @click="getIndexForUpdate(trIndex)"> Update
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
                      v-for="(headerValue, index) in headerWithoutIndex" :key="index">
                      <label for=''>{{ headerWithoutIndex[index] }}</label>
            <b-form-input id="form-title-input"
                          type="text"
                          v-model="addForm[headerWithoutIndex[index]]"
                          required
                          placeholder="Enter the Value">
            </b-form-input>
        </b-form-group>
        <!-- modal buttons -->
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

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
   </div>
</template>

<script>
//import 방식 참고
import axios from 'axios';
import Vue from 'vue'
// import Alert from './Alert.vue';

export default {
    name: 'Datatable',
    // props: ['preHeader'],

    data() {
    return {
      header: [], //전달받은 df의 맨 상단 column
      addForm: {},//ex. sepal-width:' ' , sepal-length: ' ' ...
      updateForm: {},
      newDataset:{},
      hadLoaded: false,
      indexNum: ''
    };
  },
  computed:{
  headerWithoutIndex(){
    const idIndex = this.header.indexOf("ID");
    let tempHeader;
    if(idIndex!=-1){
      tempHeader = this.header.slice();
      tempHeader.splice(idIndex,1);
      // console.log(tempHeader);
    }
    return tempHeader; 
  },
  nextIndexNum(){
    return this.indexNum+1;
  }
},
    
  components: {
    //components 추가
  },
  methods: {
    loadData(){
      const path = 'http://localhost:5000/loadData';
      axios.get(path)
        .then((res) => {
          console.log(res.data);
          this.newDataset = res.data;
          this.indexNum = Object.keys(this.newDataset['ID']).length-1;//149
          if (this.hadLoaded==false)
          this.saveResponseData();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    saveResponseData () {
      let columnValues = Object.keys(this.newDataset);
      for (const columnValue of columnValues) {  
        this.header.push(columnValue); //add했을 때 다시 loaddata되는데 push 때문에 중복된는 문제 해결 필요
        this.updateForm[columnValue]= "";
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
      this.addForm['ID'] = this.nextIndexNum;  
      for (const addvalue in this.addForm){
        console.log(addvalue);
      }                     
      this.addData(this.addForm);
      // this.initForm();
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
    getIndexForUpdate(targetIndex){ 
      console.log(`targetIndex: ${targetIndex}`);
      this.updateForm['ID'] = targetIndex;
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
      axios.put(path, payload)
        .then(() => {
          this.loadData();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.loadData();
        });
    },
    initForm() {
      this.addForm = {};
      },
    },
  
  created() {
    this.loadData();
  console.log("created");
  },
  mounted() {
    console.log("mounted");
  },
  beforeUpdate(){
    console.log("beforecreate");
  },
  updated() {
    console.log("updated");
    this.hadLoaded = true;
  }



}
</script>

<style>
  .dataTable{
    margin: 0 auto;
    text-align: center;
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