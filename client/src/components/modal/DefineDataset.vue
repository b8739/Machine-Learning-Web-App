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
          <v-row>
            <v-col>
              <v-text-field
                v-model="newTableName"
                :counter="10"
                label="Name of Dataset"
                required
              ></v-text-field></v-col
          ></v-row>
          <v-spacer></v-spacer>
          <v-row> <v-progress-linear :value="percentCompleted"></v-progress-linear></v-row>
          <v-row justify="center">
            <v-progress-circular
              v-show="percentCompleted == 100"
              indeterminate
              color="primary"
            ></v-progress-circular
          ></v-row>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="gray darken-1" @click="getDefaultState(), closeDialog()" text>
              Close
            </v-btn>
            <v-btn color="blue darken-1" @click.once="dataUpload()" text>
              Confirm
            </v-btn>
          </v-card-actions>

          <v-subheader class="red--text">{{ errorMessage }} </v-subheader>
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

  // data() {
  //   return {
  //     newTableName: "",
  //     formData: null,
  //     errorMessage: "",
  //     percentCompleted: 0
  //   };
  // },
  data() {
    return this.getDefaultState();
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
    ...mapMutations("initialData", ["setTableName"]),

    getDefaultState() {
      return {
        newTableName: "",
        formData: null,
        errorMessage: "",
        percentCompleted: 0
      };
    },
    closeDialog() {
      this.$emit("update:dialog", false);
      eventBus.$emit("removeFile", true);
    },
    async dataUpload() {
      let config = {
        onUploadProgress: progressEvent => {
          let percentage = (progressEvent.loaded * 100) / progressEvent.total;
          this.percentCompleted = Math.round(percentage);
        },
        headers: {
          "Content-Type": "multipart/form-data"
        },
        params: {
          tableName: this.newTableName,
          projectName: this.projectName
        }
      };

      axios
        .post("http://localhost:8000/datasets", this.formData, config)
        .then(res => {
          alert(res.data);
          this.$emit("onComplete", true);
          eventBus.$emit("removeFile", true);
        })
        .catch(ex => {
          this.errorMessage = ex;
          this.errorMessage += "\n새로고침 후 다른 데이터로 다시 시도해주세요";
          // eventBus.$emit("removeFile", true);
          alert("ERR!!!!! : ", ex);
          // this.$router.push('/preprocess'); //delete later
        })
        .finally(() => {
          Object.assign(this.$data, this.getDefaultState());
        });
    }
  },
  created() {
    eventBus.$on("formData", formData => {
      this.formData = formData;
    });
  }
};
</script>
