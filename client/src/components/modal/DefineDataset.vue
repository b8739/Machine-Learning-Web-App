<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="400px">
      <!-- <template v-slot:activator="{ on, attrs }">
        <v-btn color="" v-bind="attrs" v-on="on">
          Define Dataset
        </v-btn>
      </template> -->
      <v-card>
        <v-container fluid>
          <span class="headline">Define Dataset</span>
          <!-- 최상단 메뉴 탭 -->

          <v-text-field
            v-model="newTableName"
            :counter="10"
            label="Name of Dataset"
            required
          ></v-text-field>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="gray darken-1" text @click="dialog = false">
              Close
            </v-btn>
            <v-btn color="blue darken-1" @click="eventHandler" text>
              Confirm
            </v-btn>
          </v-card-actions>
          <v-subheader class="red--text">{{ errorMessage }}</v-subheader>
        </v-container>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import axios from "axios";
import { eventBus } from "@/main";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      dialog: false,
      newTableName: "",
      formData: null,
      // flag
      dataUploadFlag: false,
      saveNewFileFlag: false,
      errorMessage: ""
    };
  },
  computed: {
    ...mapState({
      tableName: state => state.initialData.tableName
    })
  },
  methods: {
    ...mapMutations("initialData", ["loadSummarizedInfo"]),
    ...mapMutations("initialData", ["resetState"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapMutations("initialData", ["setTableName"]),

    eventHandler() {
      if (this.dataUploadFlag == true) {
        this.dataUpload();
        this.dataUploadFlag = false;
      } else if (this.saveNewFileFlag == true) {
        this.saveNewFile();
        this.saveNewFileFlag = false;
        this.dialog = false;
      }
    },
    async dataUpload() {
      axios
        .post("http://localhost:5000/dataupload", this.formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          params: {
            tableName: this.newTableName
          }
        })
        .then(response => {
          this.resetState();
          this.setTableName(this.newTableName);
          this.loadSummarizedData();
          this.dialog = false;
        })
        .catch(ex => {
          this.errorMessage = ex;
          // eventBus.$emit("removeFile", true);
          console.log("ERR!!!!! : ", ex);
          // this.$router.push('/preprocess'); //delete later
        });
    },
    saveNewFile() {
      let path = "http://localhost:5000/saveAsNewTable";
      console.log(this.tableName);
      console.log(this.newTableName);
      axios;
      this.$axios({
        method: "post",
        url: path,
        data: {
          tableName: this.tableName,
          newTableName: this.newTableName
        }
      })
        .then(res => {
          this.updatePlot(featureName, res.data[featureName], axisType, tpIndex);
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    eventBus.$on("dataUploadMode", modalStatus => {
      this.dialog = modalStatus;
      this.dataUploadFlag = true;
    });
    eventBus.$on("saveNewFileMode", modalStatus => {
      this.dialog = modalStatus;
      this.saveNewFileFlag = true;
    });
    eventBus.$on("formData", formData => {
      this.formData = formData;
    });
  }
};
</script>
