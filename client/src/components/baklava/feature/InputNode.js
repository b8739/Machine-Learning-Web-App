import { NodeBuilder } from "@baklavajs/core";
import FeatureOption from "@/components/baklava/feature/FeatureOption.vue";
import store from "@/store/modules/fundamental/initialData";

const columns = store.state.columns;

export default new NodeBuilder("InputNode", {
  //   twoColumn: true,
  //   width: 200
})
  .setName("Input")
  .addOutputInterface("Out")
  // .addOption("FeatureOption", "FeatureOption")
  .addOption(
    "Features",
    "ButtonOption",
    () => {
      return { features: columns };
    },
    "FeatureSidebar"
  )
  .addOption(
    "Normalization",
    "ButtonOption",
    () => {
      return {};
    },
    "NormalizationSidebar"
  )
  // .addOption("ValueText", "TextOption")
  .onCalculate(n => {
    let inputs = n.getOptionValue("Features");
    let normalization = n.getOptionValue("Normalization");
    let nodeResult = { inputs: inputs, normalization: normalization };
    n.getInterface("Out").value = nodeResult;
    // n.setOptionValue("ValueText", result);
  })

  .build();
