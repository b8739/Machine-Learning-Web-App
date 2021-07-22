<template>
  <div class="node_sidebar">
    <v-card style="background-color:transparent" class="pt-2" elevation="0" dark>
      <!-- <v-btn @click="getValue">get value</v-btn> -->
      <v-row
        align="center"
        justify="center"
        v-for="(parameter, index) in parameterKeys"
        :key="index"
      >
        <v-col> {{ parameter }}</v-col>
        <v-col>
          <input
            :tabIndex="index"
            type="text"
            class="dark-input"
            v-on="listeners"
            v-model="parameterValues[parameter]"
          />
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>
<script>
import { InputOption } from "@baklavajs/plugin-options-vue";
export default {
  extends: InputOption,
  props: ["node"],
  data() {
    return {
      parameterKeys: null,
      parameterValues: {}
    };
  },
  methods: {
    getValue() {
      console.log(this.node.name);
    }
  },
  computed: {
    algorithmInfo() {
      let algorithmInfo = { name: this.node.name, parameters: this.parameterValues };
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
