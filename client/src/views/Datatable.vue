<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Data Table</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Data</button>
        <br><br>
        <table class="table table-hover">
          <!-- table head -->
          <thead>
            <tr>
              <th v-for="(headerValue, index) in header" :key="index" scope="col">{{ header[index]}}</th>
            </tr>
          </thead>
          <!-- table body -->
          <tbody>
            <tr v-for="(dataValue, trIndex) in dataSet[header[0]]" :key="trIndex"> <!-- make row: csv파일의 1번째 열의 개수만큼 행을 만듦-->
              <td v-for="(dataValue, tdIndex) in dataSet" :key="tdIndex"> {{ dataSet[tdIndex][trIndex]}} </td> <!-- make column: index는 0부터 5번이 맞고, 뒤에꺼는 엄청 많은 param-->
            </tr>
          </tbody> 
        </table>
      </div>
    </div>
   </div>
</template>

<script>
//import 방식 참고
// import axios from 'axios';
// import Alert from './Alert.vue';

export default {
    data() {
    return {
      header: [],
      dataSet: 0,
      //dataUploadedFlag: false,
    };
  },
    // data() {
  //   return {
  //     books: [],
  //     addBookForm: {
  //       title: '',
  //       author: '',
  //       read: [],
  //     },
  //     message: '',
  //     showMessage: false,
  //     editForm: {
  //       id: '',
  //       title: '',
  //       author: '',
  //       read: [],
  //     },
  //   };
  // },
  components: {
    //components 추가
  },
  methods: {
    saveResponseData (columnValues) {
      for (const columnValue of columnValues) {  
        this.header.push(columnValue);
        //console.log(`this.header: ${this.header}`);
      }
    },
    // ***메소드 작성방식 참고***

    // getBooks() {
    //   const path = 'http://localhost:5000/books';
    //   axios.get(path)
    //     .then((res) => {
    //       this.books = res.data.books;
    //     })
    //     .catch((error) => {
    //       console.error(error);
    //     });
    // },
  },
  created() {
    // console.log(this.$route.params.dataset);
    // console.log(this.$route.params.dataset['petal_length']); // {0:...}
    // console.log(Object.keys(this.$route.params.dataset)); //columns

    //data: header에 데이터 삽입
    let columnValues = Object.keys(this.$route.params.dataset);
    this.saveResponseData(columnValues);
    this.dataSet = this.$route.params.dataset;
    console.log(this.dataSet);

}}
</script>
