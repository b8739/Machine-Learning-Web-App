<template>
  <div class="wrapper">
    <!-- <SaveChange /> -->
    <!-- v-menu -->
    <div class="tableOption" :style="tableOptionStyle">
      <v-card v-if="showTableOption" class="mx-auto" max-width="300" tile>
        <v-list dense dark>
          <v-list-item-group>
            <v-list-item active-class="white" color="#fff">열 삽입</v-list-item>
            <v-list-item color="#fff" @click="deleteColumn">열 삭제</v-list-item>
            <v-list-item color="#fff">열 정보</v-list-item>
          </v-list-item-group>
        </v-list>
      </v-card>
    </div>
    <!-- dataTable -->
    <table class="dataTable">
      <thead @click="locateTableOption" v-click-outside="onClickOutside">
        <th
          v-for="(column, thIndex) in columns"
          :key="thIndex"
          :class="{ grayBackground: thCompareClickedColumns(thIndex) }"
          @click="getColumnInfo(thIndex)"
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
            :class="{ grayBackground: tdCompareClickedColumns(trIndex, thIndex) }"
            @click="saveClickedColumnInfo(trIndex, thIndex)"
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
    <SaveChange />
  </div>
</template>
<!-- :class="{ columnSelected: columnSelectedFlags[thIndex] && rowSelectedFlags[trIndex] }" -->
<script>
import { eventBus } from "@/main";
import InfiniteLoading from "vue-infinite-loading";
import axios from "axios";
import vClickOutside from "v-click-outside";
import SaveChange from "@/components/save/SaveChange";
export default {
  directives: {
    clickOutside: vClickOutside.directive
  },
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
      clickedColumnInfo: { rowIndex: null, columnIndex: null },

      // menu
      tableOptionStyle: {
        position: "absolute",
        top: 0,
        left: 0
      },
      showTableOption: false,
      columnToDeleteInfo: { name: null, index: null },
      deleteDetector: 0,
      vListItemInputValue: false
      // style
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
    InfiniteLoading,
    SaveChange
  },
  watch: {
    xaxis: function(data) {
      this.toggleRowFlags(data);
      this.toggleColumnFlags(this.selectedColumnIndex);
    }
  },
  methods: {
    saveClickedColumnInfo(rowIndex, columnIndex) {
      this.clickedColumnInfo.rowIndex = rowIndex;
      this.clickedColumnInfo.columnIndex = columnIndex;
    },
    tdCompareClickedColumns(trIndex, thIndex) {
      if (
        (trIndex == this.clickedColumnInfo.rowIndex &&
          thIndex == this.clickedColumnInfo.columnIndex) ||
        (thIndex == 0 && trIndex == this.clickedColumnInfo.rowIndex)
      ) {
        return true;
      } else return false;
    },
    thCompareClickedColumns(thIndex) {
      if (thIndex == this.clickedColumnInfo.columnIndex) {
        return true;
      }
    },
    onClickOutside() {
      this.showTableOption = false;
    },
    deleteColumn() {
      let api = "http://localhost:5000/deleteColumn";
      console.log(this.columnToDeleteInfo.name);
      axios
        .get(api, {
          params: {
            columnToDelete: this.columnToDeleteInfo.name
          }
        })
        .then(res => {
          //초기화 해주어야 v-for가 반응해서 화면이 변경됨
          this.dataSet = [];
          this.limit = 0;
          this.columns.splice(this.columnToDeleteInfo.index, 1);
          this.deleteDetector++;
          this.infiniteLoadingCreated();
        })
        .catch(error => {});
      this.showTableOption = !this.showTableOption;
    },
    locateTableOption(event) {
      this.showTableOption = true;
      this.tableOptionStyle.left = event.clientX - 320 + "px";
      this.tableOptionStyle.top = event.clientY - 60 + "px";
      // // screenX/Y gives the coordinates relative to the screen in device pixels.
      // console.log(event.screenX);
      // console.log(event.screenY);
    },
    getColumnInfo(thIndex) {
      this.columnToDeleteInfo.name = this.columns[thIndex];
      this.columnToDeleteInfo.index = thIndex;
    },
    // hovering Effect
    assignClickColumn(thIndex) {
      this.clickedColumn = thIndex;
    },
    // checkClickedColumn(tdIndex) {
    //   if (tdIndex != this.clickedColumn) {
    //     return true;
    //   } else {
    //     return false;
    //   }
    // },
    resetHoverEffect() {
      this.clickedColumn = null;
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
          this.limit += 45; //이 값을 app.py의 192줄의 값과 똑같게 해준다.
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
            this.limit += 45;
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
    },
    openSaveChangeDialog: function(event) {
      eventBus.$emit("openSaveChange", true);
    }
  },
  created() {
    this.infiniteLoadingCreated();
  },
  mounted() {},
  beforeUnmount() {},
  beforeDestroy() {}
};
</script>
<style scoped>
.wrapper {
  min-width: 95%;
  min-height: 50vh;
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

/* row hovering effect */

/* .dataTable tr:hover {
  background-color: #b6b6b6;
  cursor: pointer;
} */
.dataTable td:first-child {
  font-weight: 600;
}
.dataTable td {
  border: 0.5px solid rgba(212, 214, 213, 0.623);
}
.dataTable th {
  min-width: 70px;
  max-width: 75px;
  border: 0.5px solid rgba(212, 214, 213, 0.623);
  /* background-color: rgba(239, 239, 239, 0.907); */
  padding: 5px 10px;
}
/* datatable odd,even */
.dataTable tr:nth-child(odd) {
  /* background-color: #d9e1f2; */
}
.dataTable tr:nth-child(even) {
  /* background-color: #f0f8ff; */
}
.grayBackground {
  background-color: #b6b6b6;
  cursor: pointer;
}
.blueBackground {
  background-color: #7390ee;
  cursor: pointer;
}
/* options */
.tableOption {
}
.white {
  background-color: rgb(0, 0, 0);
}
</style>
