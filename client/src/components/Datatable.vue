<template>
  <div class="container">
    <!-- <h1>Data Table</h1> -->
    <!-- table -->
    <table class="dataTable">
      <!-- table head -->
      <thead>
        <tr>
          <!-- <th>Index</th> -->
          <th :class="{ visibility: isHidden }"></th>
          <th v-for="(headerValue, index) in header" :key="index" scope="">{{ header[index] }}</th>
          <th>Edit</th>
        </tr>
      </thead>
      <!-- table body -->
      <tbody>
        <tr v-for="(dataValue, trIndex) in dataSet[header[0]]" :key="trIndex">
          <!-- make row: csv파일의 1번째 열의 개수만큼 행을 만듦-->
          <!-- <td>{{ trIndex }}</td> -->
          <td>
            <input type="checkbox" :class="{ visibility: isHidden }" v-bind="rowIndex[trIndex]" />
          </td>
          <td v-for="(dataValue, tdIndex) in dataSet" :key="tdIndex">
            <textarea
              rows="1"
              v-model="dataSet[tdIndex][trIndex]"
              :class="{ dataEditable: rowIndex[trIndex] }"
            ></textarea>
          </td>
          <!-- make column: index는 0부터 5번이 맞고, 뒤에꺼는 엄청 많은 param-->
          <div class="" role="group">
            <!-- update button-->
            <button
              type="button"
              class=""
              v-b-modal.update-modal
              @click="getIndexForUpdate(trIndex)"
            >
              Update
            </button>
            <!-- delete button-->
            <button type="button" class="" @click="onDeleteData()">Delete</button>
          </div>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
//import 방식 참고

export default {
  name: "Datatable",
  props: ["header", "dataSet", "hadLoaded", "isHidden", "rowIndex"],

  data() {
    return {};
  },

  computed: {},

  components: {},

  methods: {},

  // --lifecycle
  created() {
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
  }
};
</script>

<style>
.container {
  max-width: 1200px;
}
textarea {
  border: none;
  background-color: transparent;
  resize: none !important;
  outline: none;
}
/* 테이블 레이아웃 */
.dataTable {
  overflow: scroll;
  margin: 0 auto;
  text-align: center;
  vertical-align: middle;
}
.dataTable th {
  width: 100px;
}
/* 테이블 색상 */
.dataTable tr:nth-child(odd) {
  background-color: #d9e1f2;
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

.dataTable th:first-child {
  display: inline;
}
/* 테이블 체크박스 체크 가능하도록 */
.dataTable td:first-child input {
  pointer-events: auto;
}
.dataTable .visibility {
  visibility: hidden;
}
.dataTable .dataEditable {
  background: #fff;
  pointer-events: auto;
}
textarea {
  max-width: 100px;
}
</style>
