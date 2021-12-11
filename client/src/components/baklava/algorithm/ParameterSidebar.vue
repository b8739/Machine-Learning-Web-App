<template>
  <div class="node_sidebar">
    <v-card style="background-color:transparent" class="pt-2" elevation="0" dark>
      <v-btn @click="getParameters" small color="grey darken-1">Get Sample Parameters</v-btn>
      <v-btn @click="checkParameters"></v-btn>
      <v-container>
        <v-row
          align="center"
          justify="center"
          v-for="(parameter, index) in parameterKeys"
          :key="parameter"
        >
          <v-col> {{ parameter }}</v-col>
          <v-col>
            <div tabindex="0"></div>
            <input
              type="text"
              class="dark-input"
              v-on="listeners"
              v-model="parameterValues[parameter]"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>
<script>
import Vue from "vue";
import { InputOption } from "@baklavajs/plugin-options-vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  extends: InputOption,

  props: ["node"],
  watch: {
    parameterValues: function(data) {
      this.emitValue();
    }
  },

  data() {
    return {
      // parameterKeys: null,
      parameterValues: {},
      sampleParameters: {
        XGBoost: ["500", "0.08", "0.3", "0.04", "0.75", "0.5", "7"],
        SVR: ["rbf", "100", "0.1", "0.05"],
        RF: ["800", "3"]
      }
    };
  },
  methods: {
    ...mapMutations("modelingData", ["setParameterKeys"]),

    checkParameters() {
      console.log(this.parameterKeys); // 얘는 소실됨미

      console.log(this.node.getOptionValue("Parameter")); //근데 얘는 결국 값이 바뀌고
    },
    emitValue() {
      this.$emit("input", this.algorithmInfo);
    },
    getParameters() {
      this.parameterValues = {};
      this.sampleParameters[this.nodeName].forEach((element, index) => {
        // Vue.set(this.parameterValues,index,element);
        let key = this.parameterKeys[index];
        Vue.set(this.parameterValues, key, element);
      });
    }
  },
  computed: {
    ...mapState({
      parameterKeys: state => state.modelingData.parameterKeys
    }),
    nodeName() {
      return this.node.name;
    },
    algorithmInfo() {
      let algorithmInfo = { name: this.nodeName, parameters: this.parameterValues };
      return algorithmInfo;
    },
    listeners(ev) {
      return {
        ...this.$listeners,
        input: ev => this.$emit("input", this.algorithmInfo)
      };
    }
  },
  created() {
    console.log("created");
    if (this.parameterKeys == null) {
      this.setParameterKeys(this.value.parameterKeys);
    }
    // Sidebar이 닫혔다가 다시 달릴 때 re-created되기 때문에 value값을 가져와서 다시 넣어준다
    Object.keys(this.value.parameters).forEach(parameterKey => {
      console.log(parameterKey);
      console.log(this.value.parameters[parameterKey]);
      this.parameterValues[parameterKey] = this.value.parameters[parameterKey];
    });
  },
  mounted() {
    console.log(this.node.getOptionValue("Parameter"));
    console.log(this.value);
  }
};
</script>
