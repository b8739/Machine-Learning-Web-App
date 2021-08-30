<template>
  <v-container fluid id="wrapper mt-4">
    <v-card elevation="0" height="100vh">
      <v-row class="mx-0" align="center">
        <v-subheader>
          Search Filter:
        </v-subheader>

        <v-col cols="2">
          <v-select
            v-model="filterFeature"
            :items="columns"
            outlined
            label="Select Feature"
            dense
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="2">
          <v-text-field
            v-model="filterGreaterThan"
            outlined
            type="number"
            label="Greater than"
            dense
            hide-details
          ></v-text-field
        ></v-col>
        <v-icon x-small>mdi-tilde</v-icon>
        <v-col cols="2">
          <v-text-field
            outlined
            v-model="filterLessThan"
            type="number"
            label="Less than"
            dense
            hide-details
          ></v-text-field
        ></v-col>
        <v-spacer></v-spacer>
        <portal-target v-if="editMode" name="tableDeleteRow"> </portal-target>

        <!-- <v-btn color="error" v-show="editMode" @click="confirmEvent()">Cancel</v-btn> -->
      </v-row>

      <!-- toolbar -->
      <!-- {{ checkedRows }} -->
      <v-toolbar dense elevation="1">
        <div></div>
        <v-spacer></v-spacer>
        <span class="caption">
          <v-icon small @click="scrollTable('left')" class="px-1"> mdi-arrow-collapse-left</v-icon
          >Horizontal Slide
          <v-icon small @click="scrollTable('right')" class="px-1"
            >mdi-arrow-collapse-right</v-icon
          ></span
        >
        <v-spacer></v-spacer>

        <span class="caption py-2">
          {{ datasetItems.length }} of {{ fakeDatasetSize }}
          <v-icon small @click="scrollTable('top')" class="px-1">mdi-arrow-expand-up</v-icon></span
        >
      </v-toolbar>
      <!-- datatable -->
      <v-sheet>
        <v-data-table
          ref="dataTable"
          :headers="headers"
          :items="datasetItems"
          :show-select="true"
          fixed-header
          height="72vh"
          dense
          disable-pagination
          class="dataTable elevation-1"
          :item-key="columns[0]"
          :hide-default-footer="true"
        >
          <!-- checkbox -->
          <template v-slot:header.data-table-select="{ on, props }">
            <v-simple-checkbox
              :ripple="false"
              v-show="editMode"
              @input="checkAll()"
              v-bind="props"
              v-on="on"
            ></v-simple-checkbox>
          </template>
          <!-- Data Table items -->
          <template v-slot:body="{ items }">
            <tbody>
              <tr v-for="(item, itemIndex) in items" :key="itemIndex">
                <td>
                  <v-checkbox
                    v-show="editMode"
                    dense
                    v-model="checkedRowsInstance"
                    :value="itemIndex"
                    hide-details
                  />
                </td>
                <td style="min-width:70px">
                  <!-- ID index -->
                  {{ itemIndex }}
                </td>
                <!-- Feature Value -->
                <td
                  v-for="(column, columnIndex) in columns"
                  :key="columnIndex"
                  style="min-width:150px"
                >
                  {{ item[column] }}
                </td>
              </tr>
              <!-- insertedItems -->
              <tr
                v-for="(insertedItem, insertedItemIndex) in insertedItems"
                :key="insertedItemIndex"
              >
                <td></td>
                <td style="min-width:70px">
                  <!-- ID index -->
                  {{ datasetSize + insertedItemIndex + 1 }}
                </td>
                <!-- Feature Value -->
                <td
                  v-for="(column, insertedColumnIndex) in columns"
                  :key="insertedColumnIndex"
                  style="min-width:150px"
                >
                  {{ insertedItem[column] }}
                </td>
              </tr>
            </tbody>
            <infinite-loading
              ref="infiniteLoading"
              @infinite="infiniteHandler"
              spinner="waveDots"
            ></infinite-loading>
          </template>
        </v-data-table>
      </v-sheet>
      <SaveChange />
      <v-dialog v-model="dialog" max-width="500px">
        <v-card light min-height="500px">
          <v-container>
            <v-row>
              <v-col cols="5" v-for="(column, columnIndex) in columns" :key="columnIndex">
                <v-text-field dense :label="column" value="1" v-model="columnFieldInstance[column]">
                </v-text-field>
              </v-col>
            </v-row>
            <v-row justify="end">
              <portal-target name="tableInsertRow"> </portal-target>
            </v-row>
          </v-container>
        </v-card>
      </v-dialog>
    </v-card>
  </v-container>
</template>
<!-- :class="{ columnSelected: columnSelectedFlags[thIndex] && rowSelectedFlags[trIndex] }" -->
<script>
import Vue from "vue";
import { eventBus } from "@/main";
import InfiniteLoading from "vue-infinite-loading";
import axios from "axios";
import vClickOutside from "v-click-outside";
import SaveChange from "@/components/save/SaveChange";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  directives: {
    clickOutside: vClickOutside.directive
  },
  data() {
    return {
      dialog: false,
      // insertedItems: [],
      // numOfInsertion: 0,
      // columnField: {},
      dialog: false,
      activatedEvent: null,
      filterLessThan: "",
      filterGreaterThan: "",
      filterFeature: null,

      limit: 0,

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
      vListItemInputValue: false,
      // style
      checkAllFlag: false
    };
  },
  computed: {
    columnFieldInstance: {
      get() {
        return this.columnField;
      },
      set(value) {
        this.setColumnField(value);
      }
    },
    checkedRowsInstance: {
      get() {
        return this.checkedRows;
      },
      set(value) {
        this.setCheckedRows(value);
      }
    },
    // ...mapGetters("initialData", ["columns"]),
    ...mapState({
      datasetSize: state => state.initialData.datasetSize,
      columns: state => state.initialData.columns,
      tableName: state => state.initialData.tableName,
      // preprocessHandler
      editMode: state => state.preprocessHandler.editMode,
      editStatus: state => state.preprocessHandler.editStatus,
      preprocessStatus: state => state.preprocessHandler.preprocessStatus,
      // dataTableHandler
      checkedRows: state => state.dataTableHandler.checkedRows,
      datasetItems: state => state.dataTableHandler.datasetItems,
      columnField: state => state.dataTableHandler.columnField,
      numOfInsertion: state => state.dataTableHandler.numOfInsertion,
      insertedItems: state => state.dataTableHandler.insertedItems
    }),
    fakeDatasetSize() {
      return this.datasetSize + this.numOfInsertion;
    },

    dataTableWidth() {
      return this.$refs.dataTable.$el.querySelector(".v-data-table__wrapper").offsetWidth;
    },
    headers() {
      let headers = [];
      headers.push({ text: "ID", value: "ID" });
      this.columns.forEach(element => {
        let header = {
          text: element,
          value: element
        };
        if (element == this.filterFeature) {
          header["filter"] = value => {
            // 두 조건 모두 입력 안 된 경우, true를 반환해서 탈출
            if (!this.filterLessThan && !this.filterGreaterThan) return true;
            // 두 조건 모두 입력된 경우,
            if (this.filterLessThan && this.filterGreaterThan) {
              return (
                parseFloat(this.filterGreaterThan) < value &&
                value < parseFloat(this.filterLessThan)
              );
            }
            // 한 조건만 입력된 경우,
            else if (this.filterLessThan && !this.filterGreaterThan) {
              return value < parseFloat(this.filterLessThan);
            } else {
              return parseFloat(this.filterGreaterThan) < value;
            }
          };
        }

        headers.push(header);
      });
      return headers;
    }
  },
  props: ["xaxis", "selectedColumnIndex"],
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
    ...mapMutations("initialData", ["deleteDataFromGraph"]),
    ...mapMutations("dataTableHandler", ["setCheckedRows"]),
    ...mapMutations("dataTableHandler", ["addDatasetItems"]),
    // ...mapMutations("dataTableHandler", ["resetDatasetItems"]),
    ...mapMutations("dataTableHandler", ["setColumnField"]),
    ...mapActions("preprocessHandler", ["cancelEvent"]),
    ...mapMutations("dataTableHandler", ["resetDataTableVuex"]),
    ...mapMutations("preprocessHandler", ["resetPreprocessVuex"]),

    scrollTable(direction) {
      let obj = this.$refs.dataTable.$el.querySelector(".v-data-table__wrapper");
      if (direction == "top") {
        obj.scrollTo({ top: 0, behavior: "smooth" });
      } else if (direction == "right") {
        obj.scrollBy({ left: this.dataTableWidth * 0.5, top: 0, behavior: "smooth" });
      } else {
        obj.scrollBy({ left: -(this.dataTableWidth * 0.5), top: 0, behavior: "smooth" });
      }
    },
    checkAll() {
      this.checkedRows = [];
      if (!this.checkAllFlag) {
        // datasetItems 길이만큼 (scroll 되어있는 row)만 checkedRows에 집어넣음 (for performance)
        Object.keys(this.datasetItems).forEach(element => {
          this.checkedRows.push(parseInt(element));
        });
        console.log();
      }

      this.checkAllFlag = !this.checkAllFlag;
    },
    columnSearch(column, thIndex) {
      if (this.searchValueName != null) {
        // 대문자로 변형시켜서 대소문자 차이를 무시
        let targetColumn = column.toUpperCase();
        let searchColumn = this.searchValueName.toUpperCase();
        // 검색값과 일치하지 않을 때, 대상 hide
        if (targetColumn.indexOf(searchColumn) == -1) {
          this.tdVisibility[thIndex] = false;
          return false;
        }
        // 검색값과 일치할 때, 대상 show
        else {
          this.tdVisibility[thIndex] = true;
          return true;
        }
      } else {
        this.tdVisibility[thIndex] = true;
        return true;
      }
    },
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
          this.resetTableData();
          this.columns.splice(this.columnToDeleteInfo.index, 1);

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
          this.addDatasetItems(data);
        });
    },
    infiniteHandler($state) {
      // new
      let path = "http://localhost:5000/infiniteLoading";
      // axios
      this.$axios({
        method: "post",
        url: path,
        data: {
          tableName: this.tableName,
          limit: this.limit
        }
      })
        .then(({ data }) => {
          if (data.length) {
            this.limit += 45;
            this.addDatasetItems(data);
            $state.loaded();
          } else {
            $state.complete();
          }
        })
        .catch(error => {
          console.error(error);
        });
    },
    // infinteLoading

    // infiniteHandlerCustom($state) {
    //   // console.log(data);
    //   if (this.dataset.length) {
    //     for (let i = this.limit; i < this.limit + 50; i++) {
    //       // 원본 데이터셋의 길이와 같아지는 순간 종료
    //       if (i >= this.dataset.length) {
    //         $state.complete();
    //         break;
    //       }
    //       // 아니라면 계속 불러오기

    //       this.datasetItems.push(this.dataset[i]);
    //       if (this.checkAllFlag == true) {
    //         this.checkedRows.push(i);
    //       }
    //     }
    //     $state.loaded();
    //     this.limit += 50;
    //   } else {
    //     $state.complete();
    //   }
    // },
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
    },
    resetTableData() {
      this.datasetItems = [];
      this.limit = 0;
    }
  },
  created() {
    this.cancelEvent();
    // this.resetDatasetItems();
    this.resetDataTableVuex();
    this.resetPreprocessVuex();
    this.$root.$refs.DataTable = this;
    // this.infiniteLoadingCreated();
    eventBus.$on("reloadInfiniteTable", reloadStatus => {
      this.resetTableData();
      this.infiniteLoadingCreated();
    });
    // dataselected
    eventBus.$on("dataSelected", testArray => {
      console.log("eventbus");
      this.checkedRows.splice(0, this.checkedRows.length);
      testArray.forEach(element => {
        this.checkedRows.push(element);
      });
    });
    //deleteDataFromGraph

    eventBus.$on("deleteDataFromGraph", seriesName => {
      // vuex dataset에서 삭제
      this.payload = { featureName: seriesName, checkedRows: this.checkedRows };
      this.deleteDataFromGraph(this.payload);
      // infinite table 초기화
      this.checkedRows = [];
      // this.datasetItems.splice(45);
      this.limit = 0;
      this.$refs.infiniteLoading.stateChanger.reset();
    });
  },
  mounted() {},
  beforeUnmount() {},
  beforeDestroy() {}
};
</script>
<style scoped>
.wrapper {
  /* overflow-x: auto; */
}
.dataTable {
  overflow-x: auto;
  width: 100vw;
}
</style>
