<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" @click:outside="closeDialog()" persistent max-width="400px">
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
            <v-btn color="blue darken-1" @click="dataUpload()" text>
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
  props: ["dialog"],

  data() {
    return {
      newTableName: "",
      formData: null,
      errorMessage: ""
    };
  },
  computed: {
    ...mapState({
      tableName: state => state.initialData.tableName,
      projectName: state => state.initialData.projectName
    })
  },
  methods: {
    ...mapMutations("initialData", ["loadSummarizedInfo"]),
    ...mapMutations("initialData", ["resetState"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapMutations("initialData", ["setTableName"]),
    closeDialog() {
      this.$emit("update:dialog", false);
    },
    async dataUpload() {
      axios
        .post("http://localhost:5000/dataupload", this.formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          params: {
            tableName: this.newTableName,
            projectName: this.projectName
          }
        })
        .then(response => {
          // this.resetState();

          this.dialog = false;
          this.$emit("onComplete", true);
        })
        .catch(ex => {
          this.errorMessage = ex;
          // eventBus.$emit("removeFile", true);
          console.log("ERR!!!!! : ", ex);
          // this.$router.push('/preprocess'); //delete later
        });
      this.newTableName = "";
    }
  },
  created() {
    eventBus.$on("formData", formData => {
      this.formData = formData;
    });
  }
};
</script>
