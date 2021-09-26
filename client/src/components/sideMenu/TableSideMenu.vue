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
        <!-- <v-list-item link disabled>
          <v-list-item-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Conditional Insert</v-list-item-title>
        </v-list-item> -->
      </v-list-group>
    </v-list>
    <v-list dense>
      <v-list-group v-model="updateState">
        <template v-slot:activator>
          <v-list-item-title active>Update</v-list-item-title>
        </template>
        <v-list-item link @click="activateUpdateRow()">
          <v-list-item-icon>
            <v-icon></v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Update Row</v-list-item-title>
        </v-list-item>
        <!-- <v-list-item link disabled>
          <v-list-item-icon>
            <v-icon></v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Conditional Update</v-list-item-title>
        </v-list-item> -->
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
        <!-- <v-list-item link disabled>
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
        </v-list-item> -->
      </v-list-group>
    </v-list>
    <v-list dense>
      <v-list-group v-model="deleteState">
        <template v-slot:activator>
          <v-list-item-title active>Search NA</v-list-item-title>
        </template>
        <v-list-item link disabled>
          <v-list-item-icon>
            <v-icon></v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Search NA</v-list-item-title>
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
    DataTable() {
      return this.$root.$refs.DataTable;
    },
    preprocessComp() {
      return this.$root.$refs.preprocessComp;
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
    ...mapMutations("preprocessHandler", ["setEvent"]),
    ...mapMutations("preprocessHandler", ["setAdditionalCancelEvent"]),
    ...mapActions("dataTableHandler", ["deleteRow"]),
    ...mapActions("dataTableHandler", ["insertRow"]),
    ...mapActions("dataTableHandler", ["updateRow"]),
    ...mapMutations("dataTableHandler", ["setDialog"]),

    // activation
    activateDeleteRow() {
      this.setPreprocessStatus("tableDeleteRow");
      this.setEditMode("delete");
      this.setEvent(this.deleteRow);
    },
    activateInsertRow() {
      this.setPreprocessStatus("tableInsertUpdateRow");
      this.setDialog(true);
      this.setEvent(this.insertRow);
      this.setAdditionalCancelEvent(() => {
        this.setDialog(false);
      });
    },
    activateUpdateRow() {
      this.setPreprocessStatus("tableInsertUpdateRow");
      this.setEditMode("update");
      this.setEvent(this.updateRow);

      this.setAdditionalCancelEvent(() => {
        this.setDialog(false);
      });
    }
  }
};
</script>
