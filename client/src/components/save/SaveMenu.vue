<template>
  <div class="text-center">
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="" elevation="none" v-bind="attrs" v-on="on">
          <v-icon>mdi-content-save-outline</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in items"
          :key="index"
          :disabled="index == 1"
          link
          @click="clickSaveOptionEvent(index)"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <DefineDataset />
  </div>
</template>
<script>
import axios from "axios";
import { eventBus } from "@/main";
import DefineDataset from "@/components/modal/DefineDataset";
import { mapActions, mapState, mapGetters, mapMutations } from "vuex";

export default {
  data() {
    return {
      items: [{ title: "Overwrite" }, { title: "Save as New Dataset" }],
      dialog: false
    };
  },
  components: { DefineDataset },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      duplicatedColumns: state => state.summaryTableHandler.duplicatedColumns,
      tableName: state => state.initialData.tableName
    }),
    ...mapGetters("summaryTableHandler", ["summaryChangeFlag"]),
    ...mapGetters("dataTableHandler", ["tableChangeFlag"])
  },
  methods: {
    ...mapActions("summaryTableHandler", ["calculateTransaction"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapActions("initialData", ["loadColumns"]),
    ...mapActions("summaryTableHandler", ["cloneOriginalArray"]),

    clickSaveOptionEvent(index) {
      if (index == 0) {
        this.saveTableAxios("overwrite");
      } else {
        // this.saveTableAxios("newDataset");
        this.dialog = true;
        eventBus.$emit("saveNewFileMode", this.dialog);
      }
    },

    saveTableAxios(saveOption) {
      if (this.summaryChangeFlag) {
        //summary 변경 있을 때
        let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/changeColumnInfo";
        // axios
        this.$axios({
          method: "post",
          url: path,
          data: {
            duplicatedColumns: this.duplicatedColumns,
            columns: this.columns,
            tableName: this.tableName
          }
        })
          .then(res => {
            this.loadColumns();

            this.loadSummarizedData();
            this.selectionTimer = setTimeout(() => {
              this.cloneOriginalArray();
            }, 1000);
          })
          .catch(error => {
            console.error(error);
          });
      } else if (this.tableChangeFlag) {
        const path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/overwriteTable";
        axios
          .get(path, {
            params: {
              saveOption: saveOption
            }
          })
          .then(res => {
            console.log(res);
          })
          .catch(error => {
            console.error(error);
          });
      }
    }
  },
  created() {
    eventBus.$on("saveChanges", status => {
      this.saveTableAxios("overwrite");
    });
  }
};
</script>
