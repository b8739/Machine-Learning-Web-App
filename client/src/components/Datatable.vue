<template>
  <div class="container">
    <!-- <h1>Data Table</h1> -->
    <!-- <hr><br><br> -->
    <button type="button" v-b-modal.add-modal>Add Data</button>
    <button type="button" @click="visibilityToggle()" >Update Data</button>
    <br><br>
    <!-- table -->
    <table class="dataTable">
      <!-- table head -->
      <thead>
        <tr>
          <!-- <th>Index</th> -->
          <th :class="{ visibility: isHidden }"></th>
          <th v-for="(headerValue, index) in header" :key="index" scope="">{{ header[index]}}</th>
          <th>Edit</th>
        </tr>
      </thead>
      <!-- table body -->
      <tbody>
        <tr v-for="(dataValue, trIndex) in dataSet[header[0]]" :key="trIndex"> <!-- make row: csv파일의 1번째 열의 개수만큼 행을 만듦-->
          <!-- <td>{{ trIndex }}</td> -->
          <td ><input type='checkbox' 
                      :class="{ visibility: isHidden }" 
                      v-model = "rowIndex[trIndex]">
          </td>
          <td v-for="(dataValue, tdIndex) in dataSet" 
              :key="tdIndex"> 
              <textarea
                    rows="1" 
                      v-model = "dataSet [ tdIndex ][ trIndex ]" 
                    :class ="{dataEditable:rowIndex[trIndex]}"></textarea>
          </td> <!-- make column: index는 0부터 5번이 맞고, 뒤에꺼는 엄청 많은 param-->
              <div class="" role="group">
              <!-- update button-->
                <button
                  type="button"
                  class="" v-b-modal.update-modal
                  @click="getIndexForUpdate(trIndex)"> Update
                </button>
                <!-- delete button-->
                <button
                  type="button"
                  class=""
                  @click="onDeleteData()">Delete
                </button>
            </div>
        </tr>
      </tbody> 
    </table>

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
</template>

<script>
//import 방식 참고
import axios from 'axios';
import Sidebar from "../components/Sidebar.vue"
// import Alert from './Alert.vue';

export default {
  name: 'Datatable',
  // props: ['preHeader'],

  data() {
  return {
    header: [], //전달받은 df의 맨 상단 column
    addForm: {},//ex. sepal-width:' ' , sepal-length: ' ' ...
    updateForm: {},
    dataSet:{},
    hadLoaded: false,
    indexNum: '',
    isHidden:true,
    editable: false,
    rowIndex:[]
  };
},

  computed:{
  headerWithoutIndex(){
    const idIndex = this.header.indexOf("ID");
    let tempHeader;
    if(idIndex!=-1){ //처음엔 -1이라서 에러를 발생시킴, 때문에 if문으로 해당 경우의 수를 제거
      tempHeader = this.header.slice(); //copy by value
      tempHeader.splice(idIndex,1);
    }
    return tempHeader; 
  },
  nextIndexNum(){
    return this.indexNum+1;
  },
  compareIndex(){
    
  },
},
    
  components: {
    Sidebar,
  },
  methods: {
    loadData(){
      const path = 'http://localhost:5000/loadData';
      axios.get(path)
        .then((res) => {
          console.log(res.data);
          this.dataSet = res.data;
          // 데이터 추가 시 필요한 index number
          this.indexNum = Object.keys(this.dataSet['ID']).length-1;//149
          //'처음' 데이터를 받아올때만 Header를 받아오도록 처리
          if (this.hadLoaded==false)
          this.saveResponseData();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    saveResponseData () {
      let columnValues = Object.keys(this.dataSet);
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
    visibilityToggle(){
      this.isHidden = !this.isHidden;
      for(let i = 0; i<Object.keys(this.dataSet[this.header[0]]).length; i++){
        this.rowIndex.push(false);
      }
    },
    },

  // --lifecycle
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
  .container{
    max-width: 1200px;
  }
  textarea{
    border: none;
    background-color: transparent;
    resize: none !important;
    outline: none;
  }
  /* 테이블 레이아웃 */
  .dataTable{
    overflow:scroll;
    margin: 0 auto;
    text-align: center;
    vertical-align: middle;
  }
  .dataTable th{
    width:100px;
  }
  /* 테이블 색상 */
  .dataTable tr:nth-child(odd) {
    background-color: #D9E1F2;
    }
  .dataTable tr:nth-child(even) {
    background-color: #f0f8ff;
    }
  /* 테이블 이벤트 */
  .dataTable tr:hover {
    background-color: #8ab6ca;
    cursor: pointer;
}
  /* 테이블 셀 레이아웃 및 속성 */
  .dataTable tbody td textarea {
    text-align: center;
    vertical-align: middle;
    pointer-events: none;
  }
  
  .dataTable th:first-child{
     display:inline;
  }
  /* 테이블 체크박스 체크 가능하도록 */
  .dataTable td:first-child input{
    pointer-events: auto ;
  }
  .dataTable .visibility{
    visibility:hidden;
  }
  .dataTable .dataEditable{
    background:#fff;
    pointer-events: auto;
  }
  textarea{
    max-width:100px;
  }
</style>