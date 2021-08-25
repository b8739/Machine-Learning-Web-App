<template>
  <div>
    <v-list dense>
      <v-list-group v-model="insertState">
        <template v-slot:activator>
          <v-list-item-title active>Insert</v-list-item-title>
        </template>
        <v-list-item link @click="activateInsertRow">
          <v-list-item-icon>
            <!-- <v-icon>mdi-plus</v-icon> -->
          </v-list-item-icon>
          <v-list-item-title draggable label>Insert Row</v-list-item-title>
        </v-list-item>
        <v-list-item link disabled>
          <v-list-item-icon>
            <!-- <v-icon>mdi-plus</v-icon> -->
          </v-list-item-icon>
          <v-list-item-title draggable label>Conditional Insert</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
    <v-list dense>
      <v-list-group v-model="updateState">
        <template v-slot:activator>
          <v-list-item-title active>Update</v-list-item-title>
        </template>
        <v-list-item link disabled>
          <v-list-item-icon>
            <v-icon></v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Update a Row</v-list-item-title>
        </v-list-item>
        <v-list-item link disabled>
          <v-list-item-icon>
            <v-icon></v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Conditional Update</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
    <v-list dense>
      <v-list-group v-model="deleteState">
        <template v-slot:activator>
          <v-list-item-title active>Delete</v-list-item-title>
        </template>
        <v-list-item link @click="activateDeleteRow()">
          <v-list-item-icon>
            <v-icon></v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Delete Row</v-list-item-title>
        </v-list-item>
        <v-list-item link disabled>
          <v-list-item-icon>
            <v-icon></v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Delete a Column</v-list-item-title>
        </v-list-item>
        <v-list-item link disabled>
          <v-list-item-icon>
            <v-icon></v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Conditional Delete</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
  </div>
</template>
<script>
import Vue from "vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      insertState: true,
      updateState: true,
      deleteState: true
    };
  },
  computed: {
    infiniteTable() {
      return this.$root.$refs.infiniteTable;
    },

    ...mapState({
      tableName: state => state.initialData.tableName,
      preprocessStatus: state => state.preprocessHandler.preprocessStatus,
      datasetSize: state => state.initialData.datasetSize
    })
  },
  methods: {
    ...mapMutations("initialData", ["setDatasetSize"]),
    ...mapMutations("preprocessHandler", ["setPreprocessStatus"]),
    ...mapMutations("preprocessHandler", ["setEditMode"]),
    ...mapMutations("preprocessHandler", ["setEditStatus"]),
    activateDeleteRow() {
      this.setPreprocessStatus("table-delete-row");
      this.setEditMode(true);
      // event assign
      let path = "http://localhost:5000/addData";
      this.infiniteTable.activatedEvent = () => {
        this.$axios({
          method: "post",
          url: path,
          data: {
            tableName: this.tableName,
            idNumbers: this.infiniteTable.checkedRows
          }
        })
          .then(res => {
            let numOfRows = this.infiniteTable.checkedRows.length;
            this.infiniteTable.checkedRows.forEach(element => {
              console.log(element);
              Vue.delete(this.infiniteTable.datasetItems, element);
            });
            this.infiniteTable.checkedRows = []; //체크 초기화
            alert(`Total ${numOfRows} row(s) Successfully Deleted!`); //삭제 알림
            this.setDatasetSize(this.datasetSize - numOfRows);
            this.setEditMode(false);
          })
          .catch(error => {
            console.error(error);
          });
      };
    },
    activateInsertRow() {
      this.infiniteTable.dialog = true;
      this.setPreprocessStatus("table-insert-row");
      this.setEditStatus(true);
      let path = "http://localhost:5000/deleteSingleRow";
      this.infiniteTable.activatedEvent = () => {
        this.$axios({
          method: "post",
          url: path,
          data: {
            tableName: this.tableName,
            newRow: this.infiniteTable.columnField
          }
        })
          .then(res => {
            // Vue.set(
            //   this.infiniteTable.datasetItems,
            //   this.datasetSize,
            //   this.infiniteTable.columnField
            // );
            this.infiniteTable.numOfInsertion = this.infiniteTable.numOfInsertion + 1;
            // this.infiniteTable.datasetItems.push(this.infiniteTable.columnField);
            this.infiniteTable.insertedItems.push(this.infiniteTable.columnField);
            this.infiniteTable.dialog = false;
          })
          .catch(error => {
            console.error(error);
          });

        alert(`Data Added`); //삭제 알림
      };
    }
  }
};
</script>
