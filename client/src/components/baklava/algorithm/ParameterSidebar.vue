<template>
  <div class="node_sidebar">
    <v-card style="background-color:transparent" class="pt-2" elevation="0" dark>
      <v-btn @click="getParameters" small color="grey darken-1">Get Sample Parameters</v-btn>
      <v-container>
        <v-row
          align="center"
          justify="center"
          v-for="(parameter, index) in parameterKeys"
          :key="index"
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
      parameterKeys: null,
      parameterValues: {},
      sampleParameters: {
        XGBoost: ["500", "0.08", "0.3", "0.04", "0.75", "0.5", "7"],
        SVR: ["rbf", "100", "0.1", "0.05"],
        RF: ["800", "3"]
      }
    };
  },
  methods: {
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
  mounted() {
    this.parameterKeys = this.value.parameterKeys;
  }
};
</script>
