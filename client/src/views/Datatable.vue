<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Data Table</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Data</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th v-for="(headerValue, index) in header" :key="index" scope="col">{{ header[index]}}</th>
            </tr>
          </thead>
          <!-- <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title}}</td>
              <td>{{ book.author }}</td>
              <td></td>
            </tr>
          </tbody> -->
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
      dataSet: [],
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
    let columnValues = Object.keys(this.$route.params.dataset);
    this.saveResponseData(columnValues);
    this.dataSet = this.$route.params.dataset;

    for (var key in this.dataSet){
    console.log(`뭘까: ${key}`);
  }
}}
</script>
