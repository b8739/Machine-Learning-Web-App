import { NodeBuilder } from "@baklavajs/core";
import FeatureOption from "@/components/baklava/feature/FeatureOption.vue";
// import store from "@/store/modules/fundamental/initialData";
import store from "@/store/modules/dataTable/aggrid";

const columnModel = store.state.columnModel;
const datasetToLoad = store.state.datasetToLoad;

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
      // return { features: columnModel[0][datasetToLoad[0]] };
      return;
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
