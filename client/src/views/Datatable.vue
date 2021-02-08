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
            <tr v-for="(column, index) in df_columns" :key="index">
              <th scope="col">{{ df_columns.index}}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title}}</td>
              <td>{{ book.author }}</td>
              <td></td>
            </tr>
          </tbody>
        </table>
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
      dataUploadedFlag: false,
    };
  },
    watch: {
    dataUploadedFlag: function () {
      if (dataUploadedFlag === true){

      }
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
    //initialize 되었을 때 어떤 동작을 할 지 정의
  },
};
</script>
