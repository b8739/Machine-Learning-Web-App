import { NodeBuilder } from "@baklavajs/core";
import FeatureOption from "@/components/baklava/feature/FeatureOption.vue";
import store from "@/store/index";

const columns = store.getters["initialData/columns"];

export default new NodeBuilder("InputNode", {
  //   twoColumn: true,
  //   width: 200
})
  .setName("Input")
  .addOutputInterface("OUT")
  // .addOption("FeatureOption", "FeatureOption")
  .addOption(
    "Features",
    "ButtonOption",
    () => {
      return { features: columns };
    },
    "FeatureSidebar"
  )
  // .addOption("ValueText", "TextOption")
  .onCalculate(n => {
    let inputs = n.getOptionValue("Features");
    let nodeResult = { inputs: inputs };
    n.getInterface("OUT").value = nodeResult;
    // n.setOptionValue("ValueText", result);
  })

  .build();
