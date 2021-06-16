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
            v-model="tableName"
            :counter="10"
            label="Name of Dataset"
            required
          ></v-text-field>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="gray darken-1" text @click="dialog = false">
              Close
            </v-btn>
            <v-btn color="blue darken-1" @click.once="eventHandler" text>
              Confirm
            </v-btn>
          </v-card-actions>
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
      tableName: "",
      formData: null,
      // flag
      dataUploadFlag: false,
      saveNewFileFlag: false
    };
  },
  methods: {
    ...mapMutations("initialData", ["loadSummarizedInfo"]),
    ...mapActions("initialData", ["loadFundamentalData"]),
    eventHandler() {
      if (this.dataUploadFlag == true) {
        this.dataUpload();
        this.dataUploadFlag = false;
      } else if (this.saveNewFileFlag == true) {
        this.saveNewFile(this.tableName);
        this.saveNewFileFlag = false;
      }
      this.dialog = false;
    },
    dataUpload() {
      axios
        .post("http://localhost:5000/dataupload", this.formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          params: {
            tableName: this.tableName
          }
        })
        .then(response => {
          this.result = response.data;
          this.loadSummarizedInfo(this.result);

          this.$router.push({ name: "preprocess" });
        })
        .catch(ex => {
          console.log("ERR!!!!! : ", ex);
          // this.$router.push('/preprocess'); //delete later
        });
    },
    saveNewFile(tableName) {
      let api = "http://localhost:5000/duplicateTable";
      axios
        .get(api, {
          params: {
            newTableName: tableName
          }
        })
        .then(response => {})
        .catch(ex => {
          console.log("ERR!!!!! : ", ex);
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
