<template>
  <div class="wrapper">
    <!-- v-menu -->
    <div class="tableOption" :style="tableOptionStyle">
      <ul>
        <li @click="deleteColumn">열 삭제</li>
      </ul>
    </div>
    <!-- dataTable -->
    <table class="dataTable">
      <thead @click="locateTableOption">
        <th
          v-for="(column, thIndex) in columns"
          :key="thIndex"
          @mouseover="assignHoveredIndex(thIndex)"
          @mouseleave="resetHoverEffect"
          @click="getColumnInfo(thIndex)"
          :class="{ columnHoverEffect: checkHoveredColumn(thIndex) }"
        >
          {{ columns[thIndex] }}
        </th>
      </thead>
      <tbody>
        <tr
          v-for="(data, trIndex) in dataSet"
          :key="trIndex"
          :class="{ rowSelected: rowSelectedFlags[trIndex] }"
        >
          <td
            v-for="(column, thIndex) in columns"
            :key="thIndex"
            @mouseover="assignHoveredIndex(thIndex)"
            @mouseleave="resetHoverEffect"
            :class="{ columnHoverEffect: checkHoveredColumn(thIndex) }"
          >
            {{ data[columns[thIndex]] }}
          </td>
        </tr>
      </tbody>
    </table>
    <!-- <v-data-table
      :headers="headers"
      :items="dataSet"
      class="elevation-1"
      disable-pagination="true"
      dense="true"
    ></v-data-table> -->
    <infinite-loading @infinite="infiniteHandler" spinner="waveDots"></infinite-loading>
  </div>
</template>
<!-- :class="{ columnSelected: columnSelectedFlags[thIndex] && rowSelectedFlags[trIndex] }" -->
<script>
import InfiniteLoading from "vue-infinite-loading";
import axios from "axios";
// vuex
import { mapActions } from "vuex";
export default {
  data() {
    return {
      // v-menu
      // selectedItem: 1,
      // items: [{ text: "열 삭제" }, { text: "열 복사" }],

      // InfiniteLoading
      limit: 0,
      // dataset
      dataSet: [],
      // hovering & selection
      rowSelectedFlags: [],
      columnSelectedFlags: [],
      hoveredColumn: null,
      // menu
      tableOptionStyle: {
        position: "absolute",
        top: 0,
        left: 0
      },
      columnToDelete: null
      // v-menu
      // items: [{ title: "열 삭제" }, { title: "열 복사" }],
      // closeOnClick: true
    };
  },
  computed: {
    headers() {
      let headers = [];
      this.columns.forEach(element => {
        let header = { text: element, value: element };
        headers.push(header);
      });
      return headers;
    }
  },
  props: ["xaxis", "columns", "date", "selectedColumnIndex"],
  components: {
    InfiniteLoading
  },
  watch: {
    xaxis: function(data) {
      this.toggleRowFlags(data);
      this.toggleColumnFlags(this.selectedColumnIndex);
    }
  },
  methods: {
    ...mapActions(["loadFundamentalData"]),
    deleteColumn() {
      let api = "http://localhost:5000/deleteColumn";
      console.log(this.columnToDelete);
      axios
        .get(api, {
          params: {
            columnToDelete: this.columnToDelete
          }
        })
        .then(res => {
          this.dataSet = [];
          this.limit = 0;
          this.infiniteLoadingCreated();
        })
        .catch(error => {});
    },
    locateTableOption(event) {
      this.tableOptionStyle.left = event.clientX - 320 + "px";
      this.tableOptionStyle.top = event.clientY - 60 + "px";

      // // screenX/Y gives the coordinates relative to the screen in device pixels.
      // console.log(event.screenX);
      // console.log(event.screenY);
    },
    getColumnInfo(thIndex) {
      this.columnToDelete = this.columns[thIndex];
    },
    showTableOption() {},
    // hovering Effect
    assignHoveredIndex(thIndex) {
      this.hoveredColumn = thIndex;
    },
    checkHoveredColumn(thIndex) {
      if (thIndex === this.hoveredColumn) {
        return true;
      } else {
        return false;
      }
    },
    resetHoverEffect() {
      this.hoveredColumn = null;
    },
    // infinteLoading
    infiniteLoadingCreated() {
      let api = "http://localhost:5000/infiniteLoading";
      axios
        .get(api, {
          params: {
            limit: this.limit
          }
        })
        .then(({ data }) => {
          this.limit += 25; //이 값을 app.py의 192줄의 값과 똑같게 해준다.
          this.dataSet.push(...data);
        });
    },
    infiniteHandler($state) {
      let api = "http://localhost:5000/infiniteLoading";
      axios
        .get(api, {
          params: {
            limit: this.limit
          }
        })
        .then(({ data }) => {
          // console.log(data);
          if (data.length) {
            this.limit += 10;
            this.dataSet.push(...data);
            $state.loaded();
          } else {
            $state.complete();
          }
        });
    },
    toggleRowFlags(xaxis) {
      let dateObjectLength = Object.keys(this.date).length;
      for (const key in this.date) {
        let dateTime = new Date(this.date[key]).getTime();
        if (xaxis.min <= dateTime && dateTime <= xaxis.max) {
          this.rowSelectedFlags[key] = true;
        }
      }
    },
    toggleColumnFlags(selectedColumnIndex) {
      this.columnSelectedFlags[selectedColumnIndex + 1] = true;
    }
  },
  created() {
    this.infiniteLoadingCreated();
  }
};
</script>
<style scoped>
.wrapper {
  min-height: 80vh;
  max-height: 85vh;
  overflow: scroll;
}
.dataTable {
  text-transform: capitalize;
  font-size: 11px;
  margin: 0 auto;
  margin-top: 50px;
  text-align: center;
  vertical-align: middle;
}
.dataTable tbody tr.rowSelected {
  background-color: rgba(154, 189, 243, 0.863);
}
.dataTable tbody tr td.columnSelected {
  background-color: rgba(57, 132, 243, 0.863);
}
/* .datatable */

.dataTable tr:hover {
  background-color: #b6b6b6;
  cursor: pointer;
}
.dataTable td:first-child {
  font-weight: 600;
}
.dataTable td {
  border: 0.5px solid rgba(212, 214, 213, 0.623);
}
.dataTable th {
  min-width: 70px;
  border: 0.5px solid rgba(212, 214, 213, 0.623);
  background-color: rgba(239, 239, 239, 0.907);
  padding: 5px 10px;
}

/* datatable odd,even */
.dataTable tr:nth-child(odd) {
  /* background-color: #d9e1f2; */
}
.dataTable tr:nth-child(even) {
  /* background-color: #f0f8ff; */
}
.columnHoverEffect {
  background-color: #b6b6b6;
  cursor: pointer;
}
/* options */
.tableOption {
  width: 100px;
  border: 1px solid gray;
  background-color: #fff;
}
</style>
